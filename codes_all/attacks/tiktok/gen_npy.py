import pickle
import numpy as np
import sys

# Check if there are enough arguments
if len(sys.argv) < 3:
    print("Please provide an argument.")
    sys.exit(1)

argument = sys.argv[1]

arg_2 = sys.argv[2]
arg_2_list = sys.argv[2].split('_')

with open('tor_cell_data/' + arg_2 , 'rb') as file:
    loaded_dict = pickle.load(file)

valid_list = ['adobe.com', 'amazon.co.jp', 'amazon.in', 'apache.org', 'apple.com', 'azure.com', 'bbc.co.uk', 'bbc.com', 'bing.com', 'bit.ly', 'booking.com', 'cdc.gov', 'cnn.com', 'digicert.com', 'dnsmadeeasy.com', 'doubleclick.net', 'dropbox.com', 'ebay.com', 'etsy.com', 'facebook.com', 'fandom.com', 'fastly.net', 'fbcdn.net', 'flickr.com', 'force.com', 'gandi.net', 'github.com', 'github.io', 'google-analytics.com', 'googledomains.com', 'icloud.com', 'instagram.com', 'intuit.com', 'issuu.com', 'linode.com', 'live.com', 'mail.ru', 'microsoft.com', 'mozilla.org', 'msn.com', 'naver.com', 'netflix.com', 'nytimes.com', 'office365.com', 'opera.com', 'oracle.com', 'outlook.com', 'paypal.com', 'pornhub.com', 'reddit.com', 'reuters.com', 'salesforce.com', 'salesforceliveagent.com', 'skype.com', 'soundcloud.com', 'sourceforge.net', 'spotify.com', 'stackoverflow.com', 't.me', 'telegram.org', 'theguardian.com', 'tiktok.com', 'tumblr.com', 'twitch.tv', 'vimeo.com', 'w3.org', 'weebly.com', 'wellsfargo.com', 'whatsapp.com', 'wikimedia.org', 'wikipedia.org', 'xvideos.com', 'yahoo.co.jp', 'youtube.com', 'zemanta.com']

len_inp = int(argument)
X_all = np.zeros((6000,len_inp))
Y_all = np.zeros(6000)

overall_counter = 0
for key in loaded_dict.keys():
    try:
        index = valid_list.index(key)
        counter = 0
        for instances in loaded_dict[key]:
            if len(instances) == 0:
                continue
            if counter == 80:
                break
            i = 0
            while i < len(instances) and i < len_inp:
                X_all[overall_counter][i] = instances[i]
                i += 1
            Y_all[overall_counter] = index
            counter += 1
            overall_counter += 1
    except:
        continue

print(X_all[5620])
print(Y_all[5620])
print(X_all.shape)
print(Y_all.shape)
print(Y_all[0:160])
#print(beta)
np.save('X_' + arg_2_list[0] + '_' + arg_2_list[1] + '.npy', X_all)
np.save('Y_' + arg_2_list[0] + '_' + arg_2_list[1] + '.npy', Y_all)
print('done')
