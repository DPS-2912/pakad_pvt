import pickle
import numpy as np
import sys

# Check if there are enough arguments
"""
if len(sys.argv) < 2:
    print("Input how many valid instances per website needed !!")
    sys.exit(1)

valid_inst = int(sys.argv[1])
"""

def get_length_data(data_dict):
	final_list = []
	std_dev_list = []
	for webpage in valid_list:
		temp = 0
		i = 0
		error = 0
		temp_list = []
		while i < number_instances + error:
			if len(data_dict[webpage][i]) == 0:
				i += 1
				error += 1
				continue
			data_sum = 0
			for j in range(len(data_dict[webpage][i])):
				data_sum = data_sum + data_dict[webpage][i][j]
			data_sum = data_sum * 1.0 / len(data_dict[webpage][i])
			temp = temp + data_sum
			temp_list.append(data_sum)
			i += 1
		if i - error != number_instances:
			print("Error in : " + webpage)
		temp = temp * 1.0/ number_instances
		std_dev = np.std(temp_list)
		std_dev_list.append(std_dev)
		final_list.append(temp)
	print(len(final_list))
	print(final_list)
	print(len(std_dev_list))
	print(std_dev_list)

number_instances = 80

#valid_list = ['adobe.com', 'amazon.co.jp']

valid_list = ['adobe.com', 'amazon.co.jp', 'amazon.in', 'apache.org', 'apple.com', 'azure.com', 'bbc.co.uk', 'bbc.com', 'bing.com', 'bit.ly', 'booking.com', 'cdc.gov', 'cnn.com', 'digicert.com', 'dnsmadeeasy.com', 'doubleclick.net', 'dropbox.com', 'ebay.com', 'etsy.com', 'facebook.com', 'fandom.com', 'fastly.net', 'fbcdn.net', 'flickr.com', 'force.com', 'gandi.net', 'github.com', 'github.io', 'google-analytics.com', 'googledomains.com', 'icloud.com', 'instagram.com', 'intuit.com', 'issuu.com', 'linode.com', 'live.com', 'mail.ru', 'microsoft.com', 'mozilla.org', 'msn.com', 'naver.com', 'netflix.com', 'nytimes.com', 'office365.com', 'opera.com', 'oracle.com', 'outlook.com', 'paypal.com', 'pornhub.com', 'reddit.com', 'reuters.com', 'salesforce.com', 'salesforceliveagent.com', 'skype.com', 'soundcloud.com', 'sourceforge.net', 'spotify.com', 'stackoverflow.com', 't.me', 'telegram.org', 'theguardian.com', 'tiktok.com', 'tumblr.com', 'twitch.tv', 'vimeo.com', 'w3.org', 'weebly.com', 'wellsfargo.com', 'whatsapp.com', 'wikimedia.org', 'wikipedia.org', 'xvideos.com', 'yahoo.co.jp', 'youtube.com', 'zemanta.com']

print("Number of valid websites : " + str(len(valid_list)))

with open('ip_data/firefox_fiber_length.pkl', 'rb') as file:
    fiber_firefox_dict = pickle.load(file)

print("fiber_firefox")
get_length_data(fiber_firefox_dict)

with open('ip_data/firefox_satlink_length.pkl', 'rb') as file:
    sat_firefox_dict = pickle.load(file)

print("satlink_firefox")
get_length_data(sat_firefox_dict)

with open('ip_data/tor_fiber_length.pkl', 'rb') as file:
    fiber_tor_dict = pickle.load(file)

print("fiber_tor")
get_length_data(fiber_tor_dict)

with open('ip_data/tor_satlink_length.pkl', 'rb') as file:
    sat_tor_dict = pickle.load(file)

print("satlink_tor")
get_length_data(sat_tor_dict)

"""
print(len(fiber_firefox_dict.keys()))
print(len(sat_firefox_dict.keys()))
print(len(fiber_tor_dict.keys()))
print(len(sat_tor_dict.keys()))

temp_list = []
for webpage in valid_list:
	if len(fiber_firefox_dict[webpage]) >= valid_inst and len(sat_firefox_dict[webpage]) >= valid_inst and len(fiber_tor_dict[webpage]) >= valid_inst and len(sat_tor_dict[webpage]) >= valid_inst:
		print (webpage + " : " + str(len(fiber_firefox_dict[webpage]) + len(sat_firefox_dict[webpage]) + len(fiber_tor_dict[webpage]) + len(sat_tor_dict[webpage])))
		temp_list.append(len(fiber_firefox_dict[webpage]) + len(sat_firefox_dict[webpage]) + len(fiber_tor_dict[webpage]) + len(sat_tor_dict[webpage]))
	else:
		print("Error webpage : " + webpage)

temp_list.sort()
print(temp_list)
"""
