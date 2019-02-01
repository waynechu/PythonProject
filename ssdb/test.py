import os, sys
from sys import stdin, stdout

from SSDB import SSDB
try:
	pass
	ssdb = SSDB('104.199.145.233', 4001)
except Exception as e:
	pass
	print(e)
	sys.exit(0)

ssdb.request("auth", ["sa23891odi1@8hfn!0932aqiomc9AQjiHH"])

syncmap = dict()

sync_resp =  ssdb.request("hgetall", ["DNS-Agent-Sync"])
status_resp = ssdb.request("hgetall", ["DNS-Agent-Status"])

sync_keys = sync_resp.data.keys()
status_keys = status_resp.data.keys()

print(list(sync_keys))
for syncitem in sync_keys:
    print(syncitem)

for statusitem in sync_keys:
    print(statusitem)