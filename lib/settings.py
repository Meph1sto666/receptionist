import json

sPath: str = "./data/invitesettings.json"


def get_setting(name: str) -> int:
    return dict(json.load(open(sPath, "r"))).get(name, None)


def set_setting(name: str, val: int) -> None:
    s = json.load(open(sPath, "r"))
    s[name] = val
    json.dump(s, open(sPath, "w"))
