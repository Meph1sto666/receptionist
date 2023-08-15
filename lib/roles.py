import json

rolesPath:str = "./data/roles.json"

def getRole(role:str) -> int:
    return dict(json.load(open(rolesPath))).get(role, -1)

def getRoles(roles:list[str]) -> list[int]:
    rData:dict[str, int] = dict(json.load(open(rolesPath)))
    return sum([rData.get(r, -1) for r in roles], []) # type: ignore