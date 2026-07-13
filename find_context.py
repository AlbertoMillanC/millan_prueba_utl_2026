import requests
import re
import urllib3
urllib3.disable_warnings()

js_url = 'https://resultadospreccongreso2026.registraduria.gov.co/assets/index-QNJ0IV9k.js'
js = requests.get(js_url, verify=False).text

# Look around /json/ACT/
idx = js.find('/json/ACT/')
if idx != -1:
    print(js[max(0, idx-100):min(len(js), idx+200)])
    
print("\nLook around departmentCode:")
idx = js.find(':departmentCode')
if idx != -1:
    print(js[max(0, idx-100):min(len(js), idx+200)])
