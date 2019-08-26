import os
import sys
import json
from bs4 import BeautifulSoup

def parse_xml(npc_dir):
    npc_files = []
    for file in os.listdir(npc_dir):
        if file.endswith(".xml"):
            npc_files.append(file)

    drop_data = {}
    for file in npc_files:
        with open(os.path.join(npc_dir, file), "r") as f:
            contents = f.read()
        soup = BeautifulSoup(contents, features="html.parser")

        npcs = soup.find_all("npc")

        for npc in npcs:
            npc_id = eval(npc["id"])
            npc_name = npc["name"]
            drop_list = npc.find("drops")

            if drop_list is None:
                continue

            drop_data[npc_id] = {"npc_name": npc_name, "npc_file": file,
                                 "drop": [], "spoil": []}
            categories = drop_list.find_all("category")
            for category in categories:
                drops = category.find_all("drop")
                for drop in drops:

                    id = eval(drop["itemid"])
                    min_amt = eval(drop["min"])
                    max_amt = eval(drop["max"])
                    chance = eval(drop["chance"])/1e6

                    if eval(category["id"]) != -1:
                        drop_data[npc_id]["drop"].append([id, min_amt, max_amt, chance])
                    else:
                        # id == -1 means spoil
                        drop_data[npc_id]["spoil"].append([id, min_amt, max_amt, chance])

    return drop_data

if __name__ == "__main__":
    npc_dir = os.path.join(os.getcwd(), "npcs")
    out_file = "drop_data_xml.json"
    drop_data = parse_xml(npc_dir)
    json.dump(drop_data, open(out_file, 'w'))
