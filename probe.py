import requests
import re
import urllib3
urllib3.disable_warnings()

r = requests.get('https://resultadospreccongreso2026.registraduria.gov.co/assets/index-QNJ0IV9k.js', verify=False)
js_content = r.text

print("JSON files found:")
paths = re.findall(r'([\'"])(/[a-zA-Z0-9_\-\/]+\.json)\1', js_content)
for p in set(paths):
    print(p[1])

print("\nAPI paths found:")
paths_api = re.findall(r'([\'"])(/api/[^\1]*?)\1', js_content)
for p in set(paths_api):
    print(p[1])
