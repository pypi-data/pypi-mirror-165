#!/usr/bin/env python3
# vim: expandtab:ts=4:sw=4:noai
from LogP import Version

with open('docs/source/conf.py-template','r',encoding='utf-8') as f:
    Template = f.readlines()

Config = []
for l in Template:
    if l.startswith('##@Version@##'):
        Config.append(f"Version = '{Version}'\n")
    else:
        Config.append(l)
with open('docs/source/conf.py','w',encoding='utf-8') as f:
    f.writelines(Config)

with open('docs/source/index.rst-template','r',encoding='utf-8') as f:
    Template = f.readlines()

Index = []
for l in Template:
    if l.startswith('|version|'):
        Index.append(f"{Version}\n")
    else:
        Index.append(l)
with open('docs/source/index.rst','w',encoding='utf-8') as f:
    f.writelines(Index)
print(f"Set Version: {Version}")

