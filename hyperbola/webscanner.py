import requests
import re
def scan(site, flag=r'flag\{\S*?\}'):
    base = site.replace(r'((?:https?:\/\/)?.*?)\/.*', '\1')
    scan_file(flag, site)
    scan_robots(flag, base)
        
def scan_file(flag, url, rec=0):
    r = requests.get(url)
    for i in r.cookies:
        for j in re.findall(flag, i.value): print('flag found:', j)
        for j in re.findall(flag, i.name): print('flag found:', j)
    for i in re.findall(flag, r.text): print('flag found:', i)
    for i in re.findall(r'\/\*.*?\*\/', r.text): print('comment:', i)
    for i in re.findall(r'\/\/.*?[\n$]', r.text): print('comment:', i)
    for i in re.findall(r'((?:https?:\/\/)?[^\s/]*?\.[^\s/]*?)\/\S*', r.text): print('link:', i)
    for i in re.findall(r'((?:https?:\/\/)?[^\s/]*?\.[^\s/]*?)\/\S*', r.text): print('link:', i)
    base = url.replace(r'((?:https?:\/\/)?.*?)\/.*', '\1')
    if rec<3:
        for x,z,h in re.findall(r'(href|src)\s*?=\s*?(["\'])(.*?)\2', r.text): 
            if h[0]=='/': nurl = base + h
            else: nurl = base + '/' + h
            scan_file(flag, nurl, rec+1)

def scan_robots(flag, base):
    url = base+'/robots.txt'
    r = requests.get(url)
    for i in r.cookies:
        for j in re.findall(flag, i.value): print('flag found:', j)
        for j in re.findall(flag, i.name): print('flag found:', j)
    for i in re.findall(flag, r.text): print('flag found:', i)
    for i in re.findall(r'(?<=[aA]llow: )(\/.*?)$', r.text, flags = re.MULTILINE): 
        scan_file(flag, base+i)

scan('http://mercury.picoctf.net:21485/',r'picoCTF\{\S*\}')