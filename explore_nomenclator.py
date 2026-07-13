import requests
import json
import urllib3
urllib3.disable_warnings()

# 1. Fetch Nomenclator
url_nom = 'https://resultadospreccongreso2026.registraduria.gov.co/json/nomenclator.json'
r = requests.get(url_nom, verify=False)
nom = r.json()

# Look for Boyaca (level 2) and its municipalities (level 3)
boyaca_id = None
municipios_target = ['TUNJA', 'PAIPA', 'SOGAMOSO', 'DUITAMA']
muni_info = {}

# The structure might be nested in 'amb' array. Let's dump a part of it.
for elec_data in nom.get('amb', []):
    if elec_data['elec'] == 2: # Camara
        for amb in elec_data['ambitos']:
            if amb['l'] == 2 and 'BOYACA' in amb['s']:
                print("Found Boyaca:", amb['n'], amb['c'])
                boyaca_id = amb['c']
                
            if amb['l'] == 3 and amb['s'] in municipios_target:
                print("Found Municipio:", amb['n'], amb['c'])
                muni_info[amb['s']] = amb['c']

print("Muni info:", muni_info)
