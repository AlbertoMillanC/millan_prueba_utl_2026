import sqlite3
import json
import os

DB_PATH = 'db/puestos_2026.db'
OUT_PATH = 'dashboard/data.json'

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    data = {
        'totales_ca_mun': [],
        'top10_ca': {},
        'lider_se': {},
        'arrastre_verde': {}
    }
    
    # 1. Votos CA totales por municipio
    rows = c.execute('''
        SELECT m.nombre as municipio, SUM(r.votos) as votos
        FROM resultados_mesa r
        JOIN municipios m ON r.codmun = m.codmun
        WHERE r.corporacion = 'CA'
        GROUP BY m.nombre
        ORDER BY votos ASC
    ''').fetchall()
    data['totales_ca_mun'] = [dict(r) for r in rows]
    
    # 1.5 Votos SE totales por municipio (para UX)
    rows_se = c.execute('''
        SELECT m.nombre as municipio, SUM(r.votos) as votos
        FROM resultados_mesa r
        JOIN municipios m ON r.codmun = m.codmun
        WHERE r.corporacion = 'SE'
        GROUP BY m.nombre
    ''').fetchall()
    data['totales_se_mun'] = [dict(r) for r in rows_se]
    
    # Obtener municipios
    municipios = [r['municipio'] for r in data['totales_ca_mun']]
    
    for mun in municipios:
        # 2. Top 10 candidatos CA por municipio
        rows = c.execute('''
            SELECT c.nombre as candidato, p.nombre as partido, SUM(r.votos) as votos
            FROM resultados_mesa r
            JOIN municipios m ON r.codmun = m.codmun
            JOIN candidatos c ON r.codcan = c.codcan AND r.corporacion = c.corporacion AND r.codpar = c.codpar
            JOIN partidos p ON r.codpar = p.codpar
            WHERE r.corporacion = 'CA' AND m.nombre = ?
            GROUP BY c.codcan, c.nombre, p.nombre
            ORDER BY votos DESC
            LIMIT 10
        ''', (mun,)).fetchall()
        data['top10_ca'][mun] = [dict(r) for r in rows]
        
        # 3. Partido lider SE por municipio
        lider = c.execute('''
            SELECT p.nombre as partido, SUM(r.votos) as votos
            FROM resultados_mesa r
            JOIN municipios m ON r.codmun = m.codmun
            JOIN partidos p ON r.codpar = p.codpar
            WHERE r.corporacion = 'SE' AND m.nombre = ?
            GROUP BY p.codpar, p.nombre
            ORDER BY votos DESC
            LIMIT 1
        ''', (mun,)).fetchone()
        data['lider_se'][mun] = dict(lider) if lider else None
        
        # 4. Arrastre Verde CA->SE por puesto en este municipio
        arrastre_rows = c.execute('''
            WITH verde_ca AS (
                SELECT puesto, SUM(votos) as votos_ca
                FROM resultados_mesa r
                JOIN municipios m ON r.codmun = m.codmun
                WHERE corporacion = 'CA' AND codpar = '5' AND m.nombre = ?
                GROUP BY puesto
            ),
            verde_se AS (
                SELECT puesto, SUM(votos) as votos_se
                FROM resultados_mesa r
                JOIN municipios m ON r.codmun = m.codmun
                WHERE corporacion = 'SE' AND codpar = '57' AND m.nombre = ?
                GROUP BY puesto
            )
            SELECT 
                se.puesto,
                COALESCE(se.votos_se, 0) AS votos_se,
                COALESCE(ca.votos_ca, 0) AS votos_ca,
                CAST(COALESCE(se.votos_se, 0) AS FLOAT) / NULLIF(ca.votos_ca, 0) AS ratio
            FROM verde_se se
            JOIN verde_ca ca ON se.puesto = ca.puesto
            ORDER BY ratio DESC
        ''', (mun, mun)).fetchall()
        data['arrastre_verde'][mun] = [dict(r) for r in arrastre_rows if dict(r)['ratio'] is not None]

    # --- NUEVO: Extraer Top 5 por Mesa ---
    mesas_data = {}
    rows_mesas = c.execute('''
        SELECT m.nombre as muni, r.puesto, r.mesa, c.nombre as can, p.nombre as par, SUM(r.votos) as votos
        FROM resultados_mesa r
        JOIN municipios m ON r.codmun = m.codmun
        JOIN candidatos c ON r.codcan = c.codcan AND r.corporacion = c.corporacion AND r.codpar = c.codpar
        JOIN partidos p ON r.codpar = p.codpar
        WHERE r.corporacion = 'CA'
        GROUP BY m.nombre, r.puesto, r.mesa, c.nombre, p.nombre
        HAVING SUM(r.votos) > 0
    ''').fetchall()

    for row in rows_mesas:
        muni, puesto, mesa, can, par, votos = row
        if muni not in mesas_data:
            mesas_data[muni] = {}
        if puesto not in mesas_data[muni]:
            mesas_data[muni][puesto] = {}
        if mesa not in mesas_data[muni][puesto]:
            mesas_data[muni][puesto][mesa] = []
        
        mesas_data[muni][puesto][mesa].append({'candidato': can, 'partido': par, 'votos': votos})

    # Filtrar solo el top 5
    for muni in mesas_data:
        for puesto in mesas_data[muni]:
            for mesa in mesas_data[muni][puesto]:
                mesas_data[muni][puesto][mesa].sort(key=lambda x: x['votos'], reverse=True)
                mesas_data[muni][puesto][mesa] = mesas_data[muni][puesto][mesa][:5]

    # --- NUEVO: Extraer Votos Totales CA por Puesto (Para Data Bars) ---
    puestos_data = {}
    rows_puestos = c.execute('''
        SELECT m.nombre as muni, r.puesto, SUM(r.votos) as votos
        FROM resultados_mesa r
        JOIN municipios m ON r.codmun = m.codmun
        WHERE r.corporacion = 'CA'
        GROUP BY m.nombre, r.puesto
        ORDER BY votos DESC
    ''').fetchall()

    for row in rows_puestos:
        muni, puesto, votos = row
        if muni not in puestos_data:
            puestos_data[muni] = []
        puestos_data[muni].append({'puesto': puesto, 'votos': votos})

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    # INYECTAR LA DATA DIRECTAMENTE EN EL HTML PARA QUE SEA AUTOCONTENIDO (Sin Servidor)
    html_path = 'dashboard/index.html'
    if os.path.exists(html_path):
        import re
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        json_str = json.dumps(data, ensure_ascii=False)
        mesas_json_str = json.dumps(mesas_data, ensure_ascii=False)
        puestos_json_str = json.dumps(puestos_data, ensure_ascii=False)
        
        html_content = re.sub(
            r"let dashboardData = .*?;",
            f"let dashboardData = {json_str};",
            html_content,
            flags=re.DOTALL
        )
        
        # Inyectar mesasData
        if 'let mesasData =' in html_content:
            html_content = re.sub(
                r"let mesasData = .*?;",
                f"let mesasData = {mesas_json_str};",
                html_content,
                flags=re.DOTALL
            )
        else:
            # Añadir después de dashboardData
            html_content = html_content.replace(
                f"let dashboardData = {json_str};",
                f"let dashboardData = {json_str};\nlet mesasData = {mesas_json_str};"
            )

        # Inyectar puestosData
        if 'let puestosData =' in html_content:
            html_content = re.sub(
                r"let puestosData = .*?;",
                f"let puestosData = {puestos_json_str};",
                html_content,
                flags=re.DOTALL
            )
        else:
            # Añadir después de mesasData
            html_content = html_content.replace(
                f"let mesasData = {mesas_json_str};",
                f"let mesasData = {mesas_json_str};\nlet puestosData = {puestos_json_str};"
            )
        
        # Removemos el fetch si aun existe (primera vez)
        html_content = html_content.replace(
            "const res = await fetch('data.json');",
            "// fetch removido para ser autocontenido"
        ).replace(
            "dashboardData = await res.json();",
            "// data inyectada directamente"
        )
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("Data inyectada en dashboard/index.html para funcionamiento local.")
        
    print("Datos exportados a dashboard/data.json")

if __name__ == '__main__':
    main()
