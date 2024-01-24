import pickle
import numpy as np
import sys

# Check if there are enough arguments
if len(sys.argv) < 2:
    print("Input how many valid instances per website needed !!")
    sys.exit(1)

valid_inst = int(sys.argv[1])

with open('tor_cell_data/fiber_data_tiktok.pkl', 'rb') as file:
    fiber_tor_dict = pickle.load(file)

with open('tor_cell_data/satlink_data_tiktok.pkl', 'rb') as file:
    sat_tor_dict = pickle.load(file)

print(len(fiber_tor_dict.keys()))
print(len(sat_tor_dict.keys()))

final_tor_websites_list = []

for key in fiber_tor_dict.keys():
    if len(fiber_tor_dict[key]) >= valid_inst:
        counter = 0
        for val in fiber_tor_dict:
            if len(val) > 0:
                counter += 1
        if counter >= valid_inst:
            if key in sat_tor_dict.keys() and len(sat_tor_dict[key]) >= valid_inst:
                counter_two = 0
                for val in sat_tor_dict:
                    if len(val) > 0:
                        counter_two += 1
                if counter_two >= valid_inst:
                    final_tor_websites_list.append(key)

print("For tor cell data : " + str(len(final_tor_websites_list)))
print(final_tor_websites_list)

"""=============================================================================================="""

with open('ip_data/firefox_fiber_timing.pkl', 'rb') as file:
    fiber_tor_dict = pickle.load(file)

with open('ip_data/firefox_satlink_timing.pkl', 'rb') as file:
    sat_tor_dict = pickle.load(file)

print(len(fiber_tor_dict.keys()))
print(len(sat_tor_dict.keys()))

final_tor_websites_list_2 = []

for key in fiber_tor_dict.keys():
    if len(fiber_tor_dict[key]) >= valid_inst:
        counter = 0
        for val in fiber_tor_dict:
            if len(val) > 0:
                counter += 1
        if counter >= valid_inst:
            if key in sat_tor_dict.keys() and len(sat_tor_dict[key]) >= valid_inst:
                counter_two = 0
                for val in sat_tor_dict:
                    if len(val) > 0:
                        counter_two += 1
                if counter_two >= valid_inst:
                    final_tor_websites_list_2.append(key)

print("For firefox tcp/ip data : " + str(len(final_tor_websites_list_2)))
print(final_tor_websites_list_2)

"""=============================================================================================="""

with open('ip_data/tor_fiber_timing.pkl', 'rb') as file:
    fiber_tor_dict = pickle.load(file)

with open('ip_data/tor_satlink_timing.pkl', 'rb') as file:
    sat_tor_dict = pickle.load(file)

print(len(fiber_tor_dict.keys()))
print(len(sat_tor_dict.keys()))

final_tor_websites_list_3 = []

for key in fiber_tor_dict.keys():
    if len(fiber_tor_dict[key]) >= valid_inst:
        counter = 0
        for val in fiber_tor_dict:
            if len(val) > 0:
                counter += 1
        if counter >= valid_inst:
            if key in sat_tor_dict.keys() and len(sat_tor_dict[key]) >= valid_inst:
                counter_two = 0
                for val in sat_tor_dict:
                    if len(val) > 0:
                        counter_two += 1
                if counter_two >= valid_inst:
                    final_tor_websites_list_3.append(key)

print("For tor tcp/ip data : " + str(len(final_tor_websites_list_3)))
print(final_tor_websites_list_3)

"""=============================================================================================="""

final_tor_websites_list.extend(final_tor_websites_list_2)
final_tor_websites_list.extend(final_tor_websites_list_3)

print(len(final_tor_websites_list))

dict_final = {}

for val in final_tor_websites_list:
    if val not in dict_final.keys():
        dict_final[val] = 1
    else:
        dict_final[val] = dict_final[val] + 1

final_list = []
for key in dict_final.keys():
    if dict_final[key] == 3:
        final_list.append(key)

print(len(final_list))
final_list.sort()
print(final_list)
