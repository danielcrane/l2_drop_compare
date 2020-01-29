import os
from bs4 import BeautifulSoup

def load(xml_dir):
    npcdata = {}
    for file in os.listdir(xml_dir):
        if file.endswith(".xml"):
            with open(os.path.join(xml_dir, file), "r") as f:
                contents = f.read()
                soup = BeautifulSoup(contents, "xml")
                npcs = soup.find_all("npc")

                for npc in npcs:
                    npc_id = int(npc['id'])
                    radius = npc.find("set", {"name": "radius"})['val']
                    height = npc.find("set", {"name": "height"})['val']
                    mtype = npc.find("set", {"name": "type"})['val']
                    npcdata[npc_id] = {"radius": radius, "height": height, "type": mtype}

    return npcdata

def update(old_xml_dir, new_xml_dir, npcdata):
    npc_files = []
    for file in os.listdir(old_xml_dir):
        if file.endswith(".xml"):
            with open(os.path.join(old_xml_dir, file), "r") as f:
                contents = f.read()
                soup = BeautifulSoup(contents, "xml")
                npcs = soup.find_all("npc")

                for npc in npcs:
                    npc_id = int(npc['id'])
                    if npc_id in npcdata:
                        npc.find("set", {"name": "radius"})['val'] = npcdata[npc_id]['radius']
                        npc.find("set", {"name": "height"})['val'] = npcdata[npc_id]['height']
                        npc.find("set", {"name": "type"})['val'] = npcdata[npc_id]['type']

            with open(os.path.join(new_xml_dir, file), "w") as f:
                f.write(soup.prettify())


npcdata = load('aCis_datapack/data/xml/npcs/')
#print npcdata
update('npcs_fixed', 'npcs_final', npcdata)
