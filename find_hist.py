import requests
import re
import urllib3
urllib3.disable_warnings()

js_url = 'https://resultadospreccongreso2026.registraduria.gov.co/assets/index-QNJ0IV9k.js'
js = requests.get(js_url, verify=False).text

print("Looking for /json/HIST/...")
# e.g. /json/HIST/:departmentCode/:electionSiglas/:advance/:scopeCode.json
patterns = re.findall(r'\/json\/HIST.*?[`\'"]', js)
for p in set(patterns):
    print(p)

print("\nLooking for /json/...")
# Use a very generic pattern to catch the exact URL string structure
patterns = re.findall(r'\/json\/[a-zA-Z0-9_\-\/\$\{\}\.]+', js)
for p in set(patterns):
    print(p)
