import pickle
import numpy as np
import sys

number_instances = 80

def get_number_tor_cells(data_dict):
	final_list = []
	std_dev_list = []
	for webpage in valid_list:
		temp = 0
		i = 0
		error = 0
		temp_list = []
		while i < number_instances + error:
			try:
				if len(data_dict[webpage][i]) == 0:
					i += 1
					error += 1
					continue
				temp = temp + len(data_dict[webpage][i])
				temp_list.append(len(data_dict[webpage][i]))
				i += 1
			except Exception as e:
				print(webpage)
				print("This is number of websites available : " + str(len(data_dict[webpage])))
				print(i)
				print(i-error)
				break
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

valid_list = ['adobe.com', 'amazon.co.jp', 'amazon.in', 'apache.org', 'apple.com', 'azure.com', 'bbc.co.uk', 'bbc.com', 'bing.com', 'bit.ly', 'booking.com', 'cdc.gov', 'cnn.com', 'digicert.com', 'dnsmadeeasy.com', 'doubleclick.net', 'dropbox.com', 'ebay.com', 'etsy.com', 'facebook.com', 'fandom.com', 'fastly.net', 'fbcdn.net', 'flickr.com', 'force.com', 'gandi.net', 'github.com', 'github.io', 'google-analytics.com', 'googledomains.com', 'icloud.com', 'instagram.com', 'intuit.com', 'issuu.com', 'linode.com', 'live.com', 'mail.ru', 'microsoft.com', 'mozilla.org', 'msn.com', 'naver.com', 'netflix.com', 'nytimes.com', 'office365.com', 'opera.com', 'oracle.com', 'outlook.com', 'paypal.com', 'pornhub.com', 'reddit.com', 'reuters.com', 'salesforce.com', 'salesforceliveagent.com', 'skype.com', 'soundcloud.com', 'sourceforge.net', 'spotify.com', 'stackoverflow.com', 't.me', 'telegram.org', 'theguardian.com', 'tiktok.com', 'tumblr.com', 'twitch.tv', 'vimeo.com', 'w3.org', 'weebly.com', 'wellsfargo.com', 'whatsapp.com', 'wikimedia.org', 'wikipedia.org', 'xvideos.com', 'yahoo.co.jp', 'youtube.com', 'zemanta.com']

print("Number of valid websites : " + str(len(valid_list)))

with open('tor_cell_data/fiber_data_tiktok.pkl', 'rb') as file:
    fiber_firefox_dict = pickle.load(file)

print("tor_fiber")
get_number_tor_cells(fiber_firefox_dict)

with open('tor_cell_data/satlink_data_tiktok.pkl', 'rb') as file:
    sat_firefox_dict = pickle.load(file)

print("tor_sat")
get_number_tor_cells(sat_firefox_dict)
