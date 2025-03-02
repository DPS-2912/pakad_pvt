import os
import subprocess
import time
import csv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Base directory for packet captures and screenshots
BASE_DIR = "/app/captures"
subprocess.Popen(["Xvfb", ":99", "-screen", "0", "1024x768x24"])
os.environ["DISPLAY"] = ":99"

# Path to Tranco CSV file
TRANCO_CSV_PATH = "websites.csv"

# Load websites from the Tranco CSV file
def load_websites(csv_path):
    websites = []
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                websites.append("https://" + row[0].strip())
    return websites[:75]  # Ensure only top 50 websites are used

websites = load_websites(TRANCO_CSV_PATH)

# Number of times to repeat the sequence
NUM_REPEATS = 2

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

# Get the active network interface
NETWORK_INTERFACE = get_network_interface()
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

# Function to visit a website, take a screenshot, and scroll slowly
def visit_website(url, screenshot_path):
    service = Service(GECKODRIVER_PATH)
    driver = webdriver.Firefox(service=service)
    driver.get(url)
    
    time.sleep(10)  # Wait 10 seconds to ensure the page loads fully
    driver.save_screenshot(screenshot_path)
    print(f"  📸 Screenshot saved: {screenshot_path}")
    
    # Scroll the page slowly
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    scroll_step = scroll_height // 10  # Scroll in 10 steps
    for i in range(10):
        driver.execute_script(f"window.scrollBy(0, {scroll_step})")
        time.sleep(4)  # Pause between scrolls
    
    time.sleep(10)  # Additional wait time to capture network traffic
    driver.quit()

# Start capturing packets for each website
for repeat in range(NUM_REPEATS):
    print(f"\n🔄 Starting sequence {repeat + 1}/{NUM_REPEATS}")

    for site in websites:
        folder_name = site.replace("https://", "").replace(".", "_")
        folder_path = os.path.join(BASE_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # Naming PCAP file and screenshot file
        pcap_file = os.path.join(folder_path, f"trace_{repeat+1}.pcap")
        screenshot_file = os.path.join(folder_path, f"screenshot_{repeat+1}.png")
        print(f"  📌 Visiting: {site} (Trace {repeat + 1})")

        # Start capturing packets (NO FILTERING)
        tshark_process = start_packet_capture(pcap_file)

        # Visit website, take a screenshot, and scroll
        visit_website(site, screenshot_file)

        # Stop tshark
        tshark_process.terminate()
        print(f"  ✅ Saved: {pcap_file}")

        # Wait before next website
        print("  ⏳ Waiting 5 seconds before next website...\n")
        time.sleep(5)

print("\n🎯 Packet capture complete! Check your /app/captures folder.")
