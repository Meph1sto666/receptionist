import json
dta = json.load(open("./errorcodes.json", "r", encoding="utf-8"))

langdict = {}

for k in dta:
    langdict[f"errcode_{k}_res_head"] = dta[k]["response"]["head"]
    langdict[f"errcode_{k}_res_desc"] = dta[k]["response"]["desc"]
    for o in range(len(dta[k]["options"])):
        langdict[f"errcode_{k}_option_{o}"] = dta[k]["options"][o]
json.dump(langdict, open("errcode_keys_dmp", "w", encoding="utf-8"), indent=4)