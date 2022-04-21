import requests
import re
site = 'http://finally-make-a-decision-inator.heyguy__.repl.co/decide'
base = re.search(r'^(https?://)?.*?(?=/)', site).group(0)
flag = r'flag\{[^ ]*?\}'
r = requests.get(site)
for i in re.findall(flag, r.text): print('flag found:', i)
for x,z,h in re.findall(r'(href|src)\s*?=\s*?(["\'])(.*?)\2', r.text): 
    if h[0]=='/': nurl = base + h
    else: nurl = base + '/' + h
    r = requests.get(nurl)
    for i in re.findall(flag, r.text): print('flag found:', i)