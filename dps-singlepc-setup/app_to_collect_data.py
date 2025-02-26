import os
import subprocess
import time
import socket
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

# Base directory for packet captures
BASE_DIR = "/home/dps/captures"

subprocess.Popen(["Xvfb", ":99", "-screen", "0", "1024x768x24"])
os.environ["DISPLAY"] = ":99"

# List of websites to visit
websites = [
    "https://w3schools.com",
    "https://www.thapar.edu",
    "https://www.github.com"
]

# Number of times to repeat the sequence
NUM_REPEATS = 1

# Path to GeckoDriver for Firefox
GECKODRIVER_PATH = "/usr/bin/geckodriver"

# Function to dynamically get the active network interface
def get_network_interface():
    try:
        output = subprocess.check_output(["ip", "route"]).decode("utf-8")
        for line in output.split("\n"):
            if "default via" in line:
                return line.split("dev")[1].split()[0]  # Extract interface name
        return "any"  # Fallback to capturing all interfaces
    except subprocess.CalledProcessError:
        return "any"

# Get the active network interface (should return "enp0s8" in your case)
NETWORK_INTERFACE = "enp0s8"
print(f"🌐 Using network interface: {NETWORK_INTERFACE}")

# Function to start tshark and capture all network traffic (NO FILTERING)
def start_packet_capture(output_file):
    return subprocess.Popen([
        "tshark",
        "-i", NETWORK_INTERFACE,
        "-T", "fields",
        "-e", "frame.time",
        "-e", "ip.src",
        "-e", "ip.dst",
        "-e", "ip.proto",
        "-e", "frame.len",
        "-w", output_file  # Save as a PCAP file
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Function to visit a website using Firefox
def visit_website(url):
    service = Service(GECKODRIVER_PATH)
    driver = webdriver.Firefox(service=service)
    driver.get(url)
    time.sleep(10)  # Wait for page to load
    driver.quit()

# Start capturing packets for each website
for repeat in range(NUM_REPEATS):
    print(f"\n🔄 Starting sequence {repeat + 1}/{NUM_REPEATS}")

    for site in websites:
        folder_name = site.replace("https://", "").replace(".", "_")
        folder_path = os.path.join(BASE_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # Naming PCAP file
        pcap_file = os.path.join(folder_path, f"trace_{repeat+1}.pcap")
        print(f"  📌 Visiting: {site} (Trace {repeat + 1})")

        # Start capturing packets (NO FILTERING)
        tshark_process = start_packet_capture(pcap_file)

        # Visit website using Firefox
        visit_website(site)

        # Stop tshark
        tshark_process.terminate()
        print(f"  ✅ Saved: {pcap_file}")

        # Wait before next website
        print("  ⏳ Waiting 10 seconds before next website...\n")
        time.sleep(10)

print("\n🎯 Packet capture complete! Check your /app/captures folder.")
