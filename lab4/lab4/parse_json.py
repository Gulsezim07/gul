import json

# Открытие и чтение файла
with open("sample-data.json", "r") as openfile:
    y = json.load(openfile)

s = """Interface Status
================================================================================
DN                                                 Description           Speed    MTU  
-------------------------------------------------- --------------------  ------  ------"""


for el in y["imdata"]:
    
    dn = el["l1PhysIf"]["attributes"].get("dn", "N/A")
    speed = el["l1PhysIf"]["attributes"].get("speed", "N/A")
    mtu = el["l1PhysIf"]["attributes"].get("mtu", "N/A") 
    s += f"\n{dn:<71}  {speed:<8} {mtu:<6}"


print(s)