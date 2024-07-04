import deep_translator # type: ignore
import json

of = input("origin file (default: './en_en')> ")
if len(of) < 1: of = "./en_en.json"
tl = input("target language> ")
fn = input("file name> ")

data = json.load(open(of, "r", encoding="utf-8"))

progress = 0
for d in data:
    data[d]=deep_translator.GoogleTranslator(source="auto", target=tl).translate(data[d]) # type: ignore
    print(f"[{progress} / {len(data)}] {d}", end="\r")
    progress+=1

json.dump(data, open(f"./{fn}.json", "w", encoding="utf-8"), indent=4)