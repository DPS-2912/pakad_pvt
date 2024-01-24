import pyshark
import subprocess
import os
import sys
import copy
import pickle
import multiprocessing
from collections import defaultdict

directory = '/share/p299sing/psingh_imp/big_data/data/fiber_data/captures/simple/firefox'
type_data = 'firefox_fiber'

def get_data_per_webpage(pcap_file):
    timing_webpage = {}
    length_webpage = {}
    direction_webpage = {}
    retransmission_webpage = {}

    # Iterate over each PCAP file
    if 1==1:
        seq_number = 0
        ips = {}
        timing_packets = []
        direction_packets = []
        length_packets = []
        retransmission_packets = []

        delta = pcap_file.split('_')[0]
        if 1==1:
            try:
                cap = pyshark.FileCapture(os.path.join(directory, pcap_file))
                time_zero = cap[0].sniff_timestamp
            except:
                print(pcap_file + " Error")
                cap.close()
                return ()
            # finding max_ip
            try:
                for packet in cap:
                    if 'IP' in packet:
                        src_ip = str(packet.ip.src)
                        dst_ip = str(packet.ip.dst)
                        if src_ip in ips:
                            ips[src_ip] = ips[src_ip] + 1
                        if dst_ip in ips:
                            ips[dst_ip] = ips[dst_ip] + 1
                        if src_ip not in ips:
                            ips[src_ip] = 1
                        if dst_ip not in ips:
                            ips[dst_ip] = 1
                max_ip = ''
                max_packets = 0
                for key, value in ips.items():
                    if value > max_packets and key != '172.17.0.2':
                        max_packets = value
                        max_ip = key

                #print(max_ip + " for " + pcap_file)

                for packet in cap:
                    if 'IP' in packet:
                        src_ip = str(packet.ip.src)
                        dst_ip = str(packet.ip.dst)
                        if src_ip ==  max_ip or dst_ip == max_ip:
                            seq_number = seq_number + 1
                            timing_packets.append(float(packet.sniff_timestamp) - float(time_zero))
                            length_packets.append(int(packet.length))
                            if src_ip == '172.17.0.2':
                                direction_packets.append(1)
                            if dst_ip == '172.17.0.2':
                                direction_packets.append(-1)
                            if 'TCP' in packet:
                                if hasattr(packet.tcp, 'analysis_retransmission') or hasattr(packet.tcp, 'analysis_fast_retransmission'):
                                    retransmission_packets.append(1)
                                else:
                                    retransmission_packets.append(0)
                            else:
                                retransmission_packets.append(0)

                cap.close()

                if delta not in timing_webpage:
                    timing_webpage[delta] = []

                timing_webpage[delta].append(timing_packets)

                if delta not in direction_webpage:
                    direction_webpage[delta] = []

                direction_webpage[delta].append(direction_packets)

                if delta not in length_webpage:
                    length_webpage[delta] = []

                length_webpage[delta].append(length_packets)

                if delta not in retransmission_webpage:
                    retransmission_webpage[delta] = []

                retransmission_webpage[delta].append(retransmission_packets)

            except Exception as e:
                print("Error occured " + str(e))
                return ()

    return (delta, timing_webpage, direction_webpage, length_webpage, retransmission_webpage)

def get_data_all():

    pcap_files = os.listdir(directory)

    results_tim = defaultdict(list)
    results_dir = defaultdict(list)
    results_length = defaultdict(list)
    results_retrans = defaultdict(list)

    # Create a pool of workers equal to the number of CPU cores
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        # Map the function to the websites and collect results
        all_results = pool.map(get_data_per_webpage, pcap_files)

    # Aggregate results into the four final_results dictionaries
    for result in all_results:
        if result:
            website, data1, data2, data3, data4 = result
            results_tim[website].append(data1)
            results_dir[website].append(data2)
            results_length[website].append(data3)
            results_retrans[website].append(data4)

    print(len(results_tim))
    print(len(results_dir))
    print(len(results_length))
    print(len(results_retrans))

    with open(type_data + '_timing.pkl', 'wb') as file:
        pickle.dump(results_tim, file)

    with open(type_data + '_direction.pkl', 'wb') as file:
        pickle.dump(results_dir, file)

    with open(type_data + '_length.pkl', 'wb') as file:
        pickle.dump(results_length, file)

    with open(type_data + '_retransmissions.pkl', 'wb') as file:
        pickle.dump(results_retrans, file)

    print(type_data + ' done !!')

if __name__ == "__main__":
    get_data_all()
