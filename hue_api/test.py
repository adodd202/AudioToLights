import requests as r
import json
import sys
addr = "https://www.meethue.com/api/nupnp"
response = r.get(addr).json()[0]
bridge_ip = response["internalipaddress"]
addr = "http://{}/api".format(bridge_ip)
message = {"devicetype":"HueApp"}
#username = r.post(addr, json=message).json()[0]["success"]["username"]
username = "6pgyicc6fL1OZa6rggfVS9RWoZzpv4qkrJ0TaVck"
addr = "http://{}/api/{}".format(bridge_ip, username)
response = r.get(addr)
print(response.raise_for_status())
lights = response.json()["lights"]
groups = response.json()["groups"]
print("SUCCESS")
#class Test:
#    def __init__(self, name):
#        self.name = name
#        print(self.name)
#C = Test("x")
addr += "/lights/2/state"
message = {"on":False, "transitiontime":1, "bri":254}
res = r.put(addr, json=message).json()
#res = r.get(addr).json()["state"]["on"]
print(res)
