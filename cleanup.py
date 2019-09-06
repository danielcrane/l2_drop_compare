import os
from bs4 import BeautifulSoup

def cleanup(old_xml_dir, new_xml_dir):
    npc_files = []
    for file in os.listdir(old_xml_dir):
        if file.endswith(".xml"):
            with open(os.path.join(old_xml_dir, file), "r") as f:
                contents = f.read()
                soup = BeautifulSoup(contents, "xml")
                npcs = soup.find_all("npc")

                for npc in npcs:
                    dropblock = npc.find("drops")
                    drops = npc.find_all("drop")
                    if dropblock and not drops:
                        npc_id = eval(npc["id"])
                        print npc_id
                        dropblock.decompose()

            with open(os.path.join(new_xml_dir, file), "w") as f:
                f.write(soup.prettify())
cleanup('npcs_new', 'npcs_final')
