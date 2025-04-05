import os
import re

def filter_pcap_files(root_folder):
    for website_folder in os.listdir(root_folder):
        website_path = os.path.join(root_folder, website_folder)
        if not os.path.isdir(website_path):
            continue

        files = os.listdir(website_path)
        
        screenshot_indices = set()
        for file in files:
            match = re.match(r'screenshot_(\d+)\.png', file)
            if match:
                screenshot_indices.add(match.group(1))
        
        for file in files:
            match = re.match(r'trace_(\d+)\.pcap', file)
            if match:
                index = match.group(1)
                if index not in screenshot_indices:
                    os.remove(os.path.join(website_path, file))
                    print(f"Deleted unmatched pcap: {file} in {website_folder}")

        for file in files:
            if file.startswith('screenshot_') and file.endswith('.png'):
                os.remove(os.path.join(website_path, file))
                print(f"Deleted screenshot: {file} in {website_folder}")


filter_pcap_files("F:\captures")
