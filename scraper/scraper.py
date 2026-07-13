import requests
import json
import argparse
import time
import os
import urllib3
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_BASE_URL = 'https://resultadospreccongreso2026.registraduria.gov.co/json/ACT/'

MUNICIPIOS_BOYACA = {
    'TUNJA': '0700001',
    'PAIPA': '0700181',
    'SOGAMOSO': '0700277',
    'DUITAMA': '0700079'
}

ELECCIONES = {
    'CA': 'CA',
    'SE': 'SE'
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://resultadospreccongreso2026.registraduria.gov.co"
}

def fetch_with_retry(url, max_retries=3):
    """Realiza un request GET con retry y backoff."""
    backoff = 1
    for attempt in range(max_retries):
        try:
            r = requests.get(url, headers=HEADERS, verify=False, timeout=10)
            if r.status_code == 200:
                try:
                    return r.json()
                except json.JSONDecodeError:
                    return None
            elif r.status_code == 404:
                return None # No data for this mesa
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(backoff)
        backoff *= 2
    return None

def get_mesas_from_nomenclator(municipios_names):
    """Parsea el nomenclator y extrae las mesas de los municipios solicitados."""
    try:
        with open('sample_data/nomenclator.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        logging.error(f"Error cargando nomenclator.json: {e}")
        return []

    ambitos = data['amb'][0]['ambitos']
    
    boyaca = None
    for a in ambitos:
        if a and a.get('c') == '0700':
            boyaca = a
            break
            
    if not boyaca:
        return []

    target_codes = [MUNICIPIOS_BOYACA.get(m.upper()) for m in municipios_names if MUNICIPIOS_BOYACA.get(m.upper())]
    mesas_list = []

    for muni_idx in boyaca.get('h', [])[0].get('p', []):
        muni = ambitos[muni_idx]
        if muni.get('c') in target_codes:
            if 'h' in muni and len(muni['h']) > 0:
                for zona_idx in muni['h'][0].get('p', []):
                    zona = ambitos[zona_idx]
                    if 'h' in zona and len(zona['h']) > 0:
                        for puesto_idx in zona['h'][0].get('p', []):
                            puesto = ambitos[puesto_idx]
                            puesto_code = puesto['c']
                            num_mesas = puesto.get('m', 0)
                            for m_num in range(1, num_mesas + 1):
                                mesa_code = f"{puesto_code}{m_num:06d}"
                                mesas_list.append((muni['n'], mesa_code))
    return mesas_list

def preflight(municipios):
    logging.info("Iniciando Preflight...")
    mesas = get_mesas_from_nomenclator(municipios)
    logging.info(f"PREFLIGHT TOTAL: Se estima procesar {len(mesas)} mesas (x2 elecciones). Total requests: {len(mesas)*2}")

def download_mesa(args):
    elec_name, elec_code, muni_name, mesa_code, out_dir = args
    url = f"{API_BASE_URL}{elec_code}/{mesa_code}.json"
    data = fetch_with_retry(url)
    if data:
        # Save exact mesa data
        out_path = os.path.join(out_dir, f"{elec_name}_{mesa_code}.json")
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        return (True, mesa_code)
    return (False, mesa_code)

def extract_and_save(municipios):
    """Extrae datos mesa a mesa de la API y los guarda temporalmente."""
    out_dir = 'sample_data/mesas'
    os.makedirs(out_dir, exist_ok=True)
    
    mesas = get_mesas_from_nomenclator(municipios)
    if not mesas:
        logging.error("No se encontraron mesas para procesar.")
        return

    tasks = []
    for muni_name, mesa_code in mesas:
        for elec_name, elec_code in ELECCIONES.items():
            tasks.append((elec_name, elec_code, muni_name, mesa_code, out_dir))
            
    logging.info(f"Descargando {len(tasks)} archivos JSON de mesas concurrentemente...")
    
    exitos = 0
    fallos = 0
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(download_mesa, task): task for task in tasks}
        
        for idx, future in enumerate(as_completed(futures)):
            success, mesa_code = future.result()
            if success:
                exitos += 1
            else:
                fallos += 1
                
            if (idx + 1) % 100 == 0:
                logging.info(f"Progreso: {idx + 1}/{len(tasks)} (Exitos: {exitos}, Fallos: {fallos})")
                
    logging.info(f"Extraccion finalizada. Exitos: {exitos}, Fallos: {fallos}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scraper de resultados electorales UTL 2026 (Real Data)')
    parser.add_argument('--municipios', nargs='+', default=['TUNJA', 'PAIPA', 'SOGAMOSO', 'DUITAMA'],
                        help='Lista de municipios a extraer (TUNJA PAIPA SOGAMOSO DUITAMA)')
    parser.add_argument('--preflight', action='store_true', help='Muestra conteo de mesas sin descargar')
    
    args = parser.parse_args()
    
    if args.preflight:
        preflight(args.municipios)
    else:
        extract_and_save(args.municipios)
        logging.info("Extraccion completada. Ejecuta db/etl.py para cargar a SQLite.")
