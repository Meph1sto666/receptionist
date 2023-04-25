import os

def addExts(path:str) -> None:
    if os.path.isdir(path):
        for p in os.listdir(path):
            addExts(f"{path}/{p}")
    else:
        print(path)
addExts("./cogs")