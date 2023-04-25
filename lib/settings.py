import json
sPath:str = "./data/invitesettings.json"

def getSetting(name:str) -> int:
    return dict(json.load(open(sPath, "r"))).get(name, None)

def setSetting(name:str, val:int) -> None:
    s = json.load(open(sPath, "r"))
    s[name] = val
    json.dump(s, open(sPath, "w"))