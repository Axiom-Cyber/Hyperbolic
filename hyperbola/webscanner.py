import requests
import re
site = 'http://texasholdem-v2.heyguy__.repl.co/play.a'
base = site.split('/')
if base[0] in ('http:','https:'): base = '/'.join(base[0:3])
flag = r'flag\{.*?\}?'
r = requests.get(site)
print(r.text)