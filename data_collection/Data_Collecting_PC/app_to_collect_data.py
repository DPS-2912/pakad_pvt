import sys
import logging
from loguru import logger
import time
import datetime
import csv
import os
import psutil
import signal
import subprocess as sub
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from tbselenium.tbdriver import TorBrowserDriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from stem.control import Controller
from stem import CircStatus
from stem import Signal
import tbselenium.common as cm
from tbselenium.utils import launch_tbb_tor_with_stem
from tbselenium.utils import start_xvfb, stop_xvfb
from selenium.webdriver.common.utils import free_port
import tempfile
from os.path import join
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

def check_ping(webpage):
    response = os.system("ping -c 1 " + webpage)
    return response

def stop_xvfb_display():
#    list_running_processes()
    proc = sub.Popen(["pgrep", "-f", "Xvfb"], stdout=sub.PIPE)
        # Kill process, if exists
    for pid in proc.stdout:
        os.kill(int(pid), signal.SIGTERM)
#    list_running_processes()

def capture_traffic(scenario, connection_type, webpage, batch_number, sample_number, interface_to_inet):
    process = None
    capture_folder = "/shared_folder/captures/%s/%s/"%(scenario, connection_type)
    os.system('mkdir -p %s'%capture_folder)
    try:
        process = sub.Popen('tcpdump' + ' -i '+ interface_to_inet +' -W 1 -w ' + capture_folder + webpage + "_%s_%s"%(batch_number,sample_number) + '.pcap' , shell=True, stdout=sub.PIPE, stderr=sub.PIPE, preexec_fn=os.setsid)
        logger.debug("Popen is working")
    except Exception as e:
        logger.debug("Error occurred:" + str(e))
    logger.debug("Starting Traffic Capture - " + "%s/%s/%s_%s_%s"%(scenario, connection_type, webpage, batch_number, sample_number))
    return process

def list_running_processes():
    command = 'ps aux'
    try:
        result = sub.run(command, shell=True, check=True, capture_output=True, text=True)
        logger.debug(str(result.stdout))
    except sub.CalledProcessError as e:
        logger.debug("Error occurred while executing ps aux:" + str(e.stderr))


def stop_capture(process):
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        logger.debug("Process and shell terminated successfully.")
    except Exception as e:
        logger.debug("Error occurred while terminating the process and shell:" + str(e))
    logger.debug("Stopping Traffic Capture")


def get_address_firefox(scenario, connection_type, webpage, batch_number, sample_number, interface_to_inet):
    global firefox_driver, image_address_firefox
    alpha = check_ping("google.com")
    gamma = check_ping(webpage)
    delta = [[]]
    beta = []
    ram = str(psutil.virtual_memory().percent)
    num_processes = str(len(list(psutil.process_iter())))
    process_list = ""
    for process in psutil.process_iter(['pid', 'name']):
        process_list = process_list + str(process.info)
    beta.append(ram)
    beta.append(num_processes)
    beta.append(process_list)
    csv_file = open("/shared_folder/data.csv", mode="a", newline="")
    beta.append("Firefox access")
    beta.append(webpage)
    beta.append(str(datetime.datetime.now()))
    if alpha == 0:
        beta.append("Internet ping working")
    else:
        beta.append("Internet ping not working")
    if gamma == 0:
        beta.append("Webpage ping working")
    else:
        beta.append("Webpage ping not working")

    proc = capture_traffic(scenario, connection_type, webpage, batch_number, sample_number, interface_to_inet)

    try:
        #Access webpage
        firefox_driver.delete_all_cookies()

        firefox_driver.get("http://"+webpage)

        out_img = image_address_firefox + webpage + "_%s_%s"%(batch_number,sample_number) + '.png'
        firefox_driver.save_screenshot(out_img)
        logger.debug("Screenshot is saved as %s" % out_img)

        beta.append("No Error !!")
        #Compute page load time
        try:
            navigationStart = firefox_driver.execute_script("return window.performance.timing.navigationStart")
            domComplete = firefox_driver.execute_script("return window.performance.timing.domComplete")
            page_load_time = domComplete - navigationStart
        except:
            page_load_time = 1000

    except TimeoutException as te:
        temp = open("/shared_folder/list_of_errors.txt", "a")
        temp.write(webpage + "_" + str(batch_number) + "_" + str(sample_number) + "\n")
        temp.close()
        beta.append(str(te))
        page_load_time = 60 * 1000
    except WebDriverException as we:
        temp = open("/shared_folder/list_of_errors.txt", "a")
        temp.write(webpage + "_" + str(batch_number) + "_" + str(sample_number) + "\n")
        temp.close()
        beta.append(str(we))
        page_load_time = 0
    finally:
        beta.append(str(page_load_time))
        delta.append(beta)
        writer = csv.writer(csv_file)
        writer.writerows(delta)
        csv_file.close()
        stop_capture(proc)

    return page_load_time

def get_address_tor(scenario, connection_type, webpage, batch_number, sample_number, interface_to_inet):
    global tor_driver, image_address_tor
    alpha = check_ping("google.com")
    gamma = check_ping(webpage)
    deltaf = [[]]
    beta = []
    ram = str(psutil.virtual_memory().percent)
    num_processes = str(len(list(psutil.process_iter())))
    process_list = ""
    for process in psutil.process_iter(['pid', 'name']):
        process_list = process_list + str(process.info)
    beta.append(ram)
    beta.append(num_processes)
    beta.append(process_list)
    csv_file = open("/shared_folder/data.csv", mode="a", newline="")
    beta.append("Tor access")
    beta.append(webpage)
    beta.append(str(datetime.datetime.now()))
    if alpha == 0:
        beta.append("Internet ping working")
    else:
        beta.append("Internet ping not working")
    if gamma == 0:
        beta.append("Webpage ping working")
    else:
        beta.append("Webpage ping not working")


    proc = capture_traffic(scenario, connection_type, webpage, batch_number, sample_number, interface_to_inet)
    #Access webpage via Tor
    try:
        before = datetime.datetime.now()
        tor_driver.delete_all_cookies()

        xvfb_display = start_xvfb()

        tor_driver.load_url("http://"+webpage, wait_for_page_body=True)

        out_img = image_address_tor + webpage + "_%s_%s"%(batch_number,sample_number) + '.png'
        tor_driver.get_screenshot_as_file(out_img)
        logger.debug("Screenshot is saved as %s" % out_img)

        stop_xvfb_display()

        page_title = tor_driver.title
        if 'error' in page_title.lower():
            logger.debug("Error in page")
            raise WebDriverException("Error in loading page !!")
        
        after = datetime.datetime.now()

        delta = after - before
        delta = int(delta.total_seconds() * 1000)
        temp = open("/shared_folder/list_of_errors.txt", "a")
        temp.write(webpage + "\n")
        temp.close()
        beta.append("No Error !!")

    except TimeoutException as te:
        temp = open("/shared_folder/list_of_errors.txt", "a")
        temp.write(webpage + "_" + str(batch_number) + "_" + str(sample_number) + "\n")
        temp.close()
        beta.append(str(te))
        delta = 60 * 1000

    except WebDriverException as we:
        temp = open("/shared_folder/list_of_errors.txt", "a")
        temp.write(webpage + "_" + str(batch_number) + "_" + str(sample_number) + "\n")
        temp.close()
        beta.append(str(we))

        if "Tried to run command without establishing a connection" in str(we):
            stop_browser_tor()
            tor_driver = run_tor_browser()
        delta = 0

    finally:
        beta.append(str(delta))
        deltaf.append(beta)
        writer = csv.writer(csv_file)
        writer.writerows(deltaf)
        csv_file.close()
        stop_capture(proc)

    return delta


def log_page_load(webpage, scenario, connection_type, batch_number, sample_number, page_load_time):
    log = open("/shared_folder/timing/%s/%s/"%(scenario, connection_type) + webpage + "_%d_%d"%(batch_number,sample_number) + '.txt', "w")
    log.write("%s"%str(page_load_time))
    log.close()

def run_firefox_browser():
    firefox_profile = Options()
    
    firefox_profile.binary_location = '/usr/lib/firefox/firefox'
    firefox_profile.add_argument("--headless")
    service = Service('/gecko/geckodriver')

    #Set up browsing session
    driver = webdriver.Firefox(service=service, options=firefox_profile)
    driver.set_page_load_timeout(60)
    driver.refresh()
    return driver

def run_tor_browser():
    tbb_dir = '/tor-browser/'
    driver = TorBrowserDriver(tbb_dir, executable_path='/gecko/geckodriver', tbb_logfile_path='/shared_folder/headless_tor_browser.log', headless=True)
    driver.set_page_load_timeout(60)
    driver.refresh()
    return driver

def stop_browser_firefox():
    global firefox_driver   
    firefox_driver.quit()
    logger.debug("Firefox Driver Stopped !!")

def stop_browser_tor():
    global tor_driver
    tor_driver.quit()
    logger.debug("Tor Driver Stopped !!")

@app.route('/startTrafficCapture', methods=['POST'])
def start_traffic_capture():
    scenario, connection_type, webpage, b_number, s_number = str(request.data.decode("utf-8")).split(",")
    batch_number = int(b_number)
    sample_number = int(s_number)

    global flag,firefox_driver, tor_driver, image_address_tor, image_address_firefox

    if flag:
        timing_folder = "/shared_folder/timing/%s/%s/"%(scenario, 'firefox')
        os.system('mkdir -p %s'%timing_folder)
        timing_folder = "/shared_folder/timing/%s/%s/"%(scenario, 'tor')
        os.system('mkdir -p %s'%timing_folder)
        image_address_firefox = "/shared_folder/image/%s/%s/"%(scenario, 'firefox')
        os.system('mkdir -p %s'%image_address_firefox)
        image_address_tor = "/shared_folder/image/%s/%s/"%(scenario, 'tor')
        os.system('mkdir -p %s'%image_address_tor)
        flag = False

    if connection_type=='firefox':
        firefox_driver = run_firefox_browser()
        timer = get_address_firefox(scenario, connection_type, webpage, batch_number, sample_number, 'eth0')
        stop_browser_firefox()

    if connection_type=='tor':
        tor_driver = run_tor_browser()
        timer = get_address_tor(scenario, connection_type, webpage, batch_number, sample_number, 'eth0')
        stop_browser_tor()

    log_page_load(webpage, scenario, connection_type, batch_number, sample_number, timer)

    response_data = {'result': timer}
    response = jsonify(response_data)
    # Use make_response to send the response back to the client
    return response

if __name__ == "__main__":
    global flag
    flag = True
    app.run(debug=False, host='0.0.0.0', port=5005)
