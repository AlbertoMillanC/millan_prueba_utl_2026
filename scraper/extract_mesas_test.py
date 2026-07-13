import json
data = json.load(open('sample_data/nomenclator.json', encoding='utf-8'))
ambitos = data['amb'][0]['ambitos']

# Find Boyaca (0700)
boyaca = None
for a in ambitos:
    if a and a.get('c') == '0700':
        boyaca = a
        break

mesas_list = []
munis = ['0700001', '0700181', '0700277', '0700079'] # Tunja, Paipa, Sogamoso, Duitama

for muni_idx in boyaca.get('h', [])[0].get('p', []):
    muni = ambitos[muni_idx]
    if muni.get('c') in munis:
        print(f"Municipio: {muni['n']} ({muni['c']})")
        # Go to Zonas
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
                            mesas_list.append(mesa_code)
        
print(f'Total mesas generated: {len(mesas_list)}')
print('Sample 5 mesas:', mesas_list[:5])
