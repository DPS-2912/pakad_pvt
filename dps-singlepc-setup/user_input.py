import os
import subprocess
import time
import csv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

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
    return websites[:75]  # Use top 75 websites

websites = load_websites(TRANCO_CSV_PATH)

# Get user inputs
start_repeat = int(input("Enter the repeat iteration to start from (e.g., 4): "))
start_website_index = int(input("Enter the website index to start from in the first iteration (0-74): "))

# Number of times to repeat the sequence
NUM_REPEATS = 25

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
print(f"\U0001F310 Using network interface: {NETWORK_INTERFACE}")

# Function to start packet capture (NO FILTERING)
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

# Function to visit a website and take a screenshot (WITHOUT SCROLLING)
def visit_website(url, screenshot_path):
    try:
        print(f"  \U0001F4CC Visiting: {url}")
        service = Service(GECKODRIVER_PATH)
        driver = webdriver.Firefox(service=service)
        driver.get(url)

        time.sleep(10)  # Wait for the page to load
        driver.save_screenshot(screenshot_path)
        print(f"  \U0001F4F8 Screenshot saved: {screenshot_path}")

        time.sleep(10)  # Additional wait time for capturing network traffic
        driver.quit()
    except Exception as e:
        print(f"  ❌ Error while visiting {url}: {e}")
        return False
    
    return True

# Start capturing packets for each website
for repeat in range(start_repeat, NUM_REPEATS):
    print(f"\n🔄 Starting sequence {repeat + 1}/{NUM_REPEATS}")
    
    # First iteration starts from user-specified index; others visit all 75 websites
    site_list = websites[start_website_index:] if repeat == start_repeat else websites

    for site in site_list:
        folder_name = site.replace("https://", "").replace(".", "_")
        folder_path = os.path.join(BASE_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # Naming PCAP file and screenshot file
        pcap_file = os.path.join(folder_path, f"trace_{repeat+1}.pcap")
        screenshot_file = os.path.join(folder_path, f"screenshot_{repeat+1}.png")
        
        # Start packet capture
        tshark_process = start_packet_capture(pcap_file)

        # Visit website and capture screenshot
        if visit_website(site, screenshot_file):
            # Stop tshark after successful visit
            tshark_process.terminate()
            print(f"  ✅ Saved: {pcap_file}")
        else:
            print(f"  ⚠ Skipping website due to error.")

        # Wait before next website
        print("  ⏳ Waiting 5 seconds before next website...\n")
        time.sleep(5)

print("\n🎯 Packet capture complete!! Check your /app/captures folder.")
