import pickle

def transform_everything(type_data):
	init_str = 'tcp_ip_data/' + type_data
	final_str = 'ip_data/' + type_data
	with open(init_str, 'rb') as file:
		init_dict = pickle.load(file)
	final_dict = {}
	for key_big in init_dict.keys():
		for data in init_dict[key_big]:
			for key in data.keys():
				print(len(data[key]))
				for lists in data[key]:
					if len(lists) != 0:
						if key not in final_dict.keys():
							final_dict[key] = []
						if key in final_dict.keys():
							final_dict[key].append(lists)
	with open(final_str, 'wb') as file:
		pickle.dump(final_dict, file)
	print("Done with " + type_data)

transform_everything('firefox_fiber_timing.pkl')
transform_everything('firefox_satlink_timing.pkl')
transform_everything('firefox_fiber_direction.pkl')
transform_everything('firefox_satlink_direction.pkl')
transform_everything('firefox_fiber_length.pkl')
transform_everything('firefox_satlink_length.pkl')
transform_everything('firefox_fiber_retransmissions.pkl')
transform_everything('firefox_satlink_retransmissions.pkl')

transform_everything('tor_fiber_timing.pkl')
transform_everything('tor_satlink_timing.pkl')
transform_everything('tor_fiber_direction.pkl')
transform_everything('tor_satlink_direction.pkl')
transform_everything('tor_fiber_length.pkl')
transform_everything('tor_satlink_length.pkl')
transform_everything('tor_fiber_retransmissions.pkl')
transform_everything('tor_satlink_retransmissions.pkl')
