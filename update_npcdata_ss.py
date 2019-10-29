import os
import codecs
import csv
from bs4 import BeautifulSoup

def load(filepath):
    npcdata = {}
    with open(filepath, "r") as ins:
        for line in ins:
            if line.startswith("("):
                data = line.split(",")
                if len(data) > 44:
                    #print data[1]
                    #print data[2]
                    if not data[2].endswith("'") and not data[2].endswith('"'):
                        #print "Fix npc name with comma"
                        del data[3]

                    #print data[41]
                    #print data[42]
                    #print data[43]
                    #print data[44]
                    npcdata[int(data[1])] = {"ss": int(data[42]), "bss": int(data[43]), "ss_rate": int(data[44])}
                    #print npcdata[data[1]]
                    #break
                #else:
                    # ignore
                    #print line
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
                        ai = npc.find("ai")
                        if (ai['spsCount'] > 0  and npcdata[npc_id]['bss'] == 0) or  (ai['ssCount'] > 0 and npcdata[npc_id]['ss'] == 0):
                            print 'old', ai

                        ai['spsCount']= npcdata[npc_id]['bss']
                        ai['spsRate']=0 if npcdata[npc_id]['bss'] == 0 else ai['spsRate']
                        ai['ssCount']=npcdata[npc_id]['ss']
                        ai['ssRate'] =npcdata[npc_id]['ss_rate']

                        # sanity check
                        if int(ai['ssCount']) == 0:
                            ai['ssRate'] = 0

                        if int(ai['spsCount']) == 0:
                            ai['spsRate'] = 0

                        if int(ai['spsCount']) > 0 and int(ai['spsRate']) == 0:
                            ai['spsRate'] = npcdata[npc_id]['ss_rate']


                        print 'new', ai
                    else:
                        print("Npc data not found, removing ss for ", npc_id)
                        ai['spsCount']= 0
                        ai['spsRate']=0
                        ai['ssCount']=0
                        ai['ssRate'] = 0

            with open(os.path.join(new_xml_dir, file), "w") as f:
                f.write(soup.prettify())


npcdata = load('npc.sql')
#for npc in npcdata:
#    if npcdata[npc]['ss'] > 0 or npcdata[npc]['bss'] > 0:
#        print npc, npcdata[npc]
update('aCis_datapack/data/xml/npcs/', 'npcs_final', npcdata)
