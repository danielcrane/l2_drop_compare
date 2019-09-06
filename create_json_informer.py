import pandas_access as mdb
import json

db_filename = 'l2.mdb'

# Listing the tables.
#for tbl in mdb.list_tables(db_filename):
#  print(tbl)

# Read a small table.
df = mdb.read_table(db_filename, "drops").sort_values(by=['npc_id', 'item_id']).to_dict()

result = {}
current = None
drops = []
spoil = []
for k, v in df['npc_id'].iteritems():
	if current != v:
		if current:
			#print sorted(drops, key = lambda x: int(x[0]))
			result[current] = {"drop": drops, "spoil": spoil}
		print "New mob: %s " % v
		current = v
		drops = []
		spoil = []
	print v
	#print k
#	print "Item id: {} percentage: {} is_sweep: {} min: {} max: {}".format(v, drops_list['percentage'][k], drops_list['sweep'][k], drops_list['min'][k], drops_list['max'][k])
	data = [df['item_id'][k], df['min'][k], df['max'][k], df['percentage'][k] / 100.0]
	if df['sweep'][k] == "1":
		spoil.append(data)
	else:
		drops.append(data)
	#if k > 1500:
	#	break
file_object = open('drop_data_l2informer.json', 'w')
json.dump(result, file_object)

"""
{"18001": {"drop": [[57, 765, 1528, 0.7], [2397, 1, 1, 1.2000048000192e-05], [2402, 1, 1, 1.899984800121599e-05], [2406, 1, 1, 8e-06], [4069, 1, 1, 0.0021008403361344537], [4070, 1, 1, 0.003194888178913738], [4071, 1, 1, 0.0016155088852988692], [1419, 1, 1, 0.2], [1864, 1, 1, 0.178349], [1866, 1, 1, 0.05945], [1878, 1, 1, 0.03567], [1885, 1, 1, 0.007407407407407408], [1889, 1, 1, 0.005952380952380952], [4197, 1, 1, 6.799945600435197e-05]], "spoil": [[1806, 1, 1, 0.010868]]}, 
"""
#
#drops = df[df['npc_id']==18001]
#
#
#print drops[drops['sweep']==0]#.loc[:, "item_id"]
#print drops[drops['sweep']==1]#.loc[:, "item_id"]
##print drops.loc[:, "id"]
#
#adena = drops[drops['item_id']==57]
#print adena['min']
#print adena['max']
#
#drops_list = drops.to_dict()
#print drops_list
#for k, v in drops_list['item_id'].iteritems():
#	print "Item id: {} percentage: {} is_sweep: {} min: {} max: {}".format(v, drops_list['percentage'][k], drops_list['sweep'][k], drops_list['min'][k], drops_list['max'][k])

