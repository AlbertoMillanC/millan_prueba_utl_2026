import requests
import re
import urllib3
urllib3.disable_warnings()

r = requests.get('https://resultadospreccongreso2026.registraduria.gov.co/assets/index-QNJ0IV9k.js', verify=False)
js_content = r.text

strings = re.findall(r'([\'"])(.*?json.*?)\1', js_content)
for s in set(strings):
    print(s[1])

# Also look for patterns like 'json/elec'
strings2 = re.findall(r'([\'"])(.*?elec.*?)\1', js_content)
for s in set(strings2):
    print("elec pattern:", s[1])
