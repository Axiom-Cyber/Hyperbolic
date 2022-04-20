import requests
import re
site = 'http://texasholdem-v2.heyguy__.repl.co/play.1'
base = '/'.join(site.split('/')[0:3])
flag = r''
print(base)
r = requests.get(site)
print(r.text)