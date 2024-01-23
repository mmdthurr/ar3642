import os
import json


STATIC = '../public_html/static'
PUBHTML = '../public_html'

priv = {}
with open('priv.json', 'rb')as f:
    priv = json.load(f)
   


for i in os.listdir(STATIC):
    if i not in priv['static']:
        os.system(f'scp {STATIC}/{i} root@107.172.140.38:/var/www/ar3642/static')
        priv['static'].append(i)

with open('priv.json', 'w') as f:
    json.dump(priv,f, indent=6)

os.system(f'scp {PUBHTML}/*.html root@107.172.140.38:/var/www/ar3642')
