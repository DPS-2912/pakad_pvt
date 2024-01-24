import csv
import urllib.request

def load_tranco_webpages_openWorld(limit):
    webpage_list = []

    tranco_list = open("tranco_82GXV.csv", "r")
    csv_reader = csv.reader(tranco_list, delimiter=',')
    
    temp = open("temp.txt","r")
    valueTillClosed = int(temp.read())
    temp.close()

    count = 0

    for n, row in enumerate(csv_reader):
        
        if n%2==0 or n<=valueTillClosed:
            continue
        
        url = "http://" + row[1]

        status_code = -100
        try:
            status_code = urllib.request.urlopen(url).getcode()
        except:
            status_code = -200
        
        if status_code == 200:
            webpage_list.append(row[1])
            count = count + 1
        
        if(count==limit):
            break

    tranco_list.close()

    return webpage_list

def load_tranco_webpages_closedWorld(limit):
    webpage_list = []

    tranco_list = open("tranco_82GXV.csv", "r")
    csv_reader = csv.reader(tranco_list, delimiter=',')
    
    count = 0

    for n, row in enumerate(csv_reader):
        
        if n%2==1:
            continue
        
        url = "http://" + row[1]

        status_code = -100
        try:
            status_code = urllib.request.urlopen(url).getcode()
        except:
            status_code = -200
        
        if status_code == 200:
            webpage_list.append(row[1])
            count = count + 1
        
        if(count==limit):
            break

    tranco_list.close()
    
    temp = open("temp.txt","w")
    temp.write(str(n))
    temp.close()
    return webpage_list



def get_webpage_list(nickname,limit):
    webpage_list = None
    if(nickname == "dummy"):
        webpage_list = ["google.com","tinyurl.com","telegram.org","tradingview.org"]
    elif(nickname == "tranco_closed"):
        webpage_list = load_tranco_webpages_closedWorld(limit)
    elif(nickname == "tranco_open"):
        webpage_list = load_tranco_webpages_openWorld(limit)
    return webpage_list

def get_more_webpage_list(limit):
    webpage_list = []

    tranco_list = open("tranco_82GXV.csv", "r")
    csv_reader = csv.reader(tranco_list, delimiter=',')

    temp = open("temp.txt","r")
    valueTillClosed = int(temp.read())
    temp.close()
    
    count = 0

    for n, row in enumerate(csv_reader):
        
        if n%2==1 or n<=valueTillClosed:
            continue
        
        url = "http://" + row[1]

        status_code = -100
        try:
            status_code = urllib.request.urlopen(url).getcode()
        except:
            status_code = -200
        
        if status_code == 200:
            webpage_list.append(row[1])
            count = count + 1
        
        if(count==limit):
            break

    tranco_list.close()
    
    temp = open("temp.txt","w")
    temp.write(str(n))
    temp.close()
    return webpage_list
