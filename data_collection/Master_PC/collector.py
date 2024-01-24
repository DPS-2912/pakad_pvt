import sys
from loguru import logger
import time
import datetime
import requests
from multiprocessing import Pool
from webpages import get_webpage_list, get_more_webpage_list
from validate_data import check_if_valid
import json

def RESTCall(host, method, args=""):
    url='http://' + host + method
    r = None
    backoff = 1
    timerr = 1
    while(r is None):
        try:
            r = requests.post(url, data=args)
            json_content = json.loads(r.content.decode('utf-8'))
            timerr = int(json_content['result'])
        except requests.exceptions.RequestException as e:
            logger.debug(e)
            logger.debug("Sleeping for backoff time: %ds"%backoff)
            time.sleep(backoff)
            if(backoff < 16):
                backoff = backoff * 2
    return timerr

def collect_more(limit):
    webpages_limit = limit*2
    total_accesses = 3
    batches = 40
    webpages = get_more_webpage_list(webpages_limit)

    scenario = "simple"
    connection_types = ["tor"]
    host_ips = ["129.97.84.27:5005","192.168.1.99:5005"] #add the ips of remote devices here, device and port connected to fiber and satellite connection

    flag_tor_first = True

    #Collect traffic
    data1 = datetime.datetime.now()
    logger.debug("=== Collecting webpage traffic ====")
    for b in range(1,batches+1):
        for connection_type in connection_types:
            logger.debug("==== Scenario: %s | Connection type: %s | ===="%(scenario,connection_type))
            for n, webpage in enumerate(webpages):
                numberOfErrors = 0
                i = 1
                while i < total_accesses+1+numberOfErrors and numberOfErrors <= 2*total_accesses:
                    ls = []
                    pool = Pool(processes=2)
                    for host_ip  in host_ips:
                        ls.append(pool.apply_async(RESTCall, args=(host_ip, "/startTrafficCapture", "%s,%s,%s,%d,%d"%(scenario, connection_type, webpage, b, i))))
                    pool.close()
                    pool.join()
                    error_flag = False
                    logger.debug("==== %s %d Collection Done ===="%(webpage,i)) 
                    for l in ls:
                        if l.get()==0 or l.get()==60000:
                            logger.debug("==== Error Data Collection ====") 
                            error_flag=True
                            break
                    if error_flag:
                        numberOfErrors = numberOfErrors + 1
                    i=i+1

    data2 = datetime.datetime.now()
    diff = data2 - data1
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    logger.debug("Finished more as well! Time elapsed: %d:%d:%d"%(hours, minutes, seconds))

def collect(open_world):

    if open_world:
        webpages_limit = 10
        total_accesses = 1
        batches = 1
        webpages = get_webpage_list("tranco_open", webpages_limit)
    else:
        webpages_limit = 25
        total_accesses = 1
        batches = 2
        webpages = get_webpage_list("dummy", webpages_limit)

    scenario = "simple"
    connection_types = ["firefox"]
    host_ips = ["192.168.1.99:5005"] #add the ips of remote devices here, device and port connected to fiber and satellite connection

    flag_tor_first = True

    #Collect traffic
    data1 = datetime.datetime.now()
    logger.debug("=== Collecting webpage traffic ====")
    for b in range(1,batches+1):
        for connection_type in connection_types:
            logger.debug("==== Scenario: %s | Connection type: %s | ===="%(scenario,connection_type))
            for n, webpage in enumerate(webpages):
                numberOfErrors = 0
                i = 1
                while i < total_accesses+1+numberOfErrors and numberOfErrors <= 2*total_accesses:
                    ls = []
                    pool = Pool(processes=2)
                    for host_ip  in host_ips:
                        ls.append(pool.apply_async(RESTCall, args=(host_ip, "/startTrafficCapture", "%s,%s,%s,%d,%d"%(scenario, connection_type, webpage, b, i))))
                    pool.close()
                    pool.join()
                    error_flag = False
                    logger.debug("==== %s %d Collection Done ===="%(webpage,i)) 
                    for l in ls:
                        if l.get()==0 or l.get()==60000:
                            logger.debug("==== Error Data Collection ====") 
                            error_flag=True
                            break
                    if error_flag:
                        numberOfErrors = numberOfErrors + 1
                    i=i+1

    data2 = datetime.datetime.now()
    diff = data2 - data1
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    logger.debug("Finished! Time elapsed: %d:%d:%d"%(hours, minutes, seconds))
    if 1==1:
        return
    totalSites = 125
    numberOfValidSitesNeeded = 100
    currentOkSites = totalSites - check_if_valid()
    while(True):
        if currentOkSites >= 100:
            break
        totalSites = totalSites + 2*(numberOfValidSitesNeeded-currentOkSites) 
        collect_more(2*(numberOfValidSitesNeeded-currentOkSites))
        currentOkSites = totalSites - check_if_valid()

