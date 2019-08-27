import json

drop_file_xml = 'drop_data_xml.json'
drop_file_l2portal = 'drop_data_l2portal.json'

key_str2int = lambda d: {int(k) if k.lstrip("-").isdigit() else k: v for k, v in d.items()}

drop_data_xml = json.load(open(drop_file_xml, "r"), object_hook=key_str2int)
drop_data_l2portal = json.load(open(drop_file_l2portal, "r"), object_hook=key_str2int)
