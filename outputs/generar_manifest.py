import sqlite3
import json
import os
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

# SECCION META (EDITAR AQUI)
META = {
    "nombre": "ALBERTO MILLÁN",
    "email": "carlosalbertomillanc@gmail.com",
    "repo_url": "https://github.com/AlbertoMillanC/millan_prueba_utl_2026"
}

DB_PATH = 'db/puestos_2026.db'

def run_sql_file(conn, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        query = f.read()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        # Fetch up to 10 rows for manifest
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchmany(10)]
        logging.info(f"{os.path.basename(file_path)}: SQL OK")
        return results
    except Exception as e:
        logging.error(f"ERROR en {file_path}: {e}")
        return {"error": str(e)}

def main():
    if not os.path.exists(DB_PATH):
        logging.error("No se encontró la base de datos.")
        return

    conn = sqlite3.connect(DB_PATH)
    
    # 1. Verificar municipios
    mun = conn.execute("SELECT COUNT(DISTINCT codmun) FROM resultados_mesa").fetchone()[0]
    logging.info(f"{mun}/4 municipios")

    manifest = {
        "meta": META,
        "database": {
            "municipios_presentes": mun,
            "filas_resultados": conn.execute("SELECT COUNT(*) FROM resultados_mesa").fetchone()[0],
            "filas_candidatos": conn.execute("SELECT COUNT(*) FROM candidatos").fetchone()[0],
        },
        "reto3": {
            "tarea_3_1": run_sql_file(conn, 'sql/tarea_3_1.sql'),
            "tarea_3_2": run_sql_file(conn, 'sql/tarea_3_2.sql'),
            "tarea_3_3": run_sql_file(conn, 'sql/tarea_3_3.sql')
        }
    }
    
    # 2. Capturar output del scatter.py
    try:
        scatter_out = subprocess.check_output(['python', 'viz/scatter.py'], text=True)
        # Buscar la linea: r=... | pendiente=... | n_mesas=...
        for line in scatter_out.split('\n'):
            if 'r=' in line and 'pendiente=' in line:
                manifest['reto5'] = line.strip()
    except Exception as e:
        logging.warning("No se pudo capturar output de scatter.py")
        
    # Guardar manifest
    with open('outputs/evaluation_manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    logging.info("Manifest guardado en outputs/evaluation_manifest.json")

if __name__ == '__main__':
    main()
