import requests
import re
import urllib3
urllib3.disable_warnings()

r = requests.get('https://resultadospreccongreso2026.registraduria.gov.co/assets/index-QNJ0IV9k.js', verify=False)
js_content = r.text

patterns = re.findall(r'([\'"\`])(.*?\.json)\1', js_content)
for p in set(patterns):
    print(p[1].encode('ascii', 'ignore').decode('ascii'))
