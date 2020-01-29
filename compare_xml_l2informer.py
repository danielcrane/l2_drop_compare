import json
import numpy as np

drop_file_xml = "drop_data_xml.json"
drop_file_l2portal = "drop_data_l2informer.json"

key_str2int = lambda d: {int(k) if k.lstrip("-").isdigit() else k: v for k, v in d.items()}

drop_data_xml = json.load(open(drop_file_xml, "r"), object_hook=key_str2int)
drop_data_l2portal = json.load(open(drop_file_l2portal, "r"), object_hook=key_str2int)

has_additional = []
for npc_id in drop_data_xml.keys():
    #print npc_id
    d1 = np.array(drop_data_xml[npc_id]["drop"])
    if not npc_id in drop_data_l2portal:
	print ("Mob %s have no drops in l2informer" % npc_id)
	continue
    d2 = np.array(drop_data_l2portal[npc_id]["drop"])

    if d1.shape[0] == 0 and d2.shape[0] != 0:
        has_additional.append([npc_id, 1, 0, 0])
        continue

    if d2.shape[0] == 0 and d1.shape[0] != 0:
        num_cats = len(np.unique(d1[:, -1]))
        has_additional.append([npc_id, 1, num_cats])
        continue

    num_cats = len(np.unique(d1[:, -1]))
    d1s = set(d1[:, 0])
    d2s = set(d2[:, 0])
    if d1s != d2s:
        has_additional.append([npc_id, 1, num_cats])
        continue

    has_additional.append([npc_id, 0, num_cats])

has_additional = np.array(has_additional)
no_diff = np.where(has_additional[:, 1] == 0)[0]
has_diff = np.where(has_additional[:, 1] == 1)[0]
print("# mobs with no diff: " + str(no_diff.shape[0]) + ", with diff:" + str(has_diff.shape[0]))

cats = {}
for npc_id in drop_data_xml.keys():
    for drop_type in ["drop", "spoil"]:
        for drop in drop_data_xml[npc_id][drop_type]:
            if drop[-1] not in cats:
                cats[drop[-1]] = 0
            cats[drop[-1]] += 1

print cats
