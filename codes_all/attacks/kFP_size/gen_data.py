import pickle
import numpy as np
import sys

# Check if there are enough arguments
if len(sys.argv) < 2:
    print("Please provide an argument.")
    sys.exit(1)

arg_2 = sys.argv[1]
arg_2_list = sys.argv[1].split('_')

with open('ip_data/' + arg_2 , 'rb') as file:
    dict2 = pickle.load(file)

with open('ip_data/' + arg_2_list[0] + '_' + arg_2_list[1] + '_timing.pkl', 'rb') as file:
    dict1 = pickle.load(file)

with open('ip_data/' + arg_2_list[0] + '_' + arg_2_list[1] + '_length.pkl', 'rb') as file:
    dict3 = pickle.load(file)

valid_list = ['adobe.com', 'amazon.co.jp', 'amazon.in', 'apache.org', 'apple.com', 'azure.com', 'bbc.co.uk', 'bbc.com', 'bing.com', 'bit.ly', 'booking.com', 'cdc.gov', 'cnn.com', 'digicert.com', 'dnsmadeeasy.com', 'doubleclick.net', 'dropbox.com', 'ebay.com', 'etsy.com', 'facebook.com', 'fandom.com', 'fastly.net', 'fbcdn.net', 'flickr.com', 'force.com', 'gandi.net', 'github.com', 'github.io', 'google-analytics.com', 'googledomains.com', 'icloud.com', 'instagram.com', 'intuit.com', 'issuu.com', 'linode.com', 'live.com', 'mail.ru', 'microsoft.com', 'mozilla.org', 'msn.com', 'naver.com', 'netflix.com', 'nytimes.com', 'office365.com', 'opera.com', 'oracle.com', 'outlook.com', 'paypal.com', 'pornhub.com', 'reddit.com', 'reuters.com', 'salesforce.com', 'salesforceliveagent.com', 'skype.com', 'soundcloud.com', 'sourceforge.net', 'spotify.com', 'stackoverflow.com', 't.me', 'telegram.org', 'theguardian.com', 'tiktok.com', 'tumblr.com', 'twitch.tv', 'vimeo.com', 'w3.org', 'weebly.com', 'wellsfargo.com', 'whatsapp.com', 'wikimedia.org', 'wikipedia.org', 'xvideos.com', 'yahoo.co.jp', 'youtube.com', 'zemanta.com']

for key_index, key in enumerate(valid_list):
    list_of_lists_1 = dict1[key]
    list_of_lists_2 = dict2[key]
    list_of_lists_3 = dict3[key]

    for sublist_index, (sublist1, sublist2, sublist3) in enumerate(zip(list_of_lists_1, list_of_lists_2, list_of_lists_3)):
        if sublist_index > 79:  # Break the loop if index exceeds 79
            break

        file_name = f"{key_index}-{sublist_index}"
        with open(arg_2_list[0] + '_' + arg_2_list[1] + '/' + file_name, 'w') as file:
            for a, b, c in zip(sublist1, sublist2, sublist3):
                file.write(f"{a} {b} {c}\n")
