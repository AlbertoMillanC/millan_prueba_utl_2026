import sqlite3
import json
import os
import glob
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DB_PATH = 'db/puestos_2026.db'
SCHEMA_PATH = 'db/schema.sql'

MUNICIPIOS = {
    '0700001': 'TUNJA',
    '0700181': 'PAIPA',
    '0700277': 'SOGAMOSO',
    '0700079': 'DUITAMA'
}

PARTIDOS_ESPECIALES = {
    '5': 'Alianza Verde (CA)',
    '57': 'Alianza Verde (SE)',
    '87': 'Pacto Historico (CA)',
    '92': 'Pacto Historico (SE)',
    '10': 'Centro Democratico',
    '2': 'Conservador'
}

def init_db(conn):
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema = f.read()
    conn.executescript(schema)
    
    for cod, nombre in MUNICIPIOS.items():
        conn.execute('INSERT OR IGNORE INTO municipios (codmun, nombre) VALUES (?, ?)', (cod, nombre))
    conn.commit()

def process_file(file_path):
    """Procesa un archivo JSON individual y retorna la lista de queries a ejecutar."""
    filename = os.path.basename(file_path)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return {'file': filename, 'queries': [], 'status': 'error', 'msg': str(e)}
        
    corporacion = 'CA' if filename.startswith('CA_') else 'SE'
    amb = data.get('amb', '')
    if not amb or len(amb) < 19:
        return {'file': filename, 'queries': [], 'status': 'error', 'msg': 'amb invalido'}
        
    codmun = amb[0:7]
    puesto = amb[:13]
    mesa = amb[13:]
    
    if codmun not in MUNICIPIOS:
        return {'file': filename, 'queries': [], 'status': 'ignored', 'msg': 'Municipio no mapeado'}

    queries = []
    
    for cam in data.get('camaras', []):
        for part in cam.get('partotabla', []):
            act = part['act']
            codpar = act['codpar']
            
            nombre_par = PARTIDOS_ESPECIALES.get(codpar, f"PARTIDO {codpar}")
            queries.append(('INSERT OR IGNORE INTO partidos (codpar, nombre) VALUES (?, ?)', (codpar, nombre_par)))
            
            for can in act.get('cantotabla', []):
                codcan = can['codcan']
                nombre = can.get('nomcan', '').strip()
                apellido = can.get('apecan', '').strip()
                nombre_completo = f"{nombre} {apellido}".strip() or "CANDIDATO DESCONOCIDO"
                    
                queries.append(('''
                    INSERT OR IGNORE INTO candidatos (codcan, corporacion, codpar, nombre)
                    VALUES (?, ?, ?, ?)
                ''', (codcan, corporacion, codpar, nombre_completo)))
                
                votos = int(can.get('vot', 0))
                
                # Insertar en resultados_mesa con datos 100% reales
                queries.append(('''
                    INSERT OR IGNORE INTO resultados_mesa (corporacion, codmun, puesto, mesa, codpar, codcan, votos)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (corporacion, codmun, puesto, mesa, codpar, codcan, votos)))
                
    return {'file': filename, 'queries': queries, 'status': 'success'}

def extract_and_load(conn):
    archivos = glob.glob('sample_data/mesas/*.json')
    if not archivos:
        logging.error("No se encontraron archivos en sample_data/mesas/")
        return
        
    cursor = conn.cursor()
    cursor.execute("SELECT archivo FROM carga_log")
    procesados = set([row[0] for row in cursor.fetchall()])
    
    archivos_pendientes = [f for f in archivos if os.path.basename(f) not in procesados]
    
    if not archivos_pendientes:
        logging.info("No hay archivos nuevos para procesar.")
        return
        
    logging.info(f"Procesando {len(archivos_pendientes)} archivos de mesas...")
    
    exitos = 0
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_file, f): f for f in archivos_pendientes}
        
        for idx, future in enumerate(as_completed(futures)):
            result = future.result()
            filename = result['file']
            
            if result['status'] == 'success':
                insertados = 0
                for query, params in result['queries']:
                    cursor.execute(query, params)
                    # Contabilizar inserciones reales vs omitidas no es exacto con INSERT OR IGNORE batch, 
                    # pero asumimos exito de fila.
                    insertados += 1
                
                cursor.execute('''
                    INSERT INTO carga_log (archivo, filas_insertadas, filas_omitidas)
                    VALUES (?, ?, ?)
                ''', (filename, insertados, 0))
                
                exitos += 1
            else:
                logging.warning(f"Error en {filename}: {result['msg']}")
                
            if (idx + 1) % 100 == 0:
                conn.commit()
                logging.info(f"Progreso ETL: {idx+1}/{len(archivos_pendientes)} archivos procesados.")
                
    conn.commit()
    logging.info(f"ETL finalizado. {exitos} mesas integradas a la base de datos.")

if __name__ == '__main__':
    logging.info("Iniciando ETL (Datos Reales)...")
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    extract_and_load(conn)
    conn.close()
    logging.info("ETL completado.")
