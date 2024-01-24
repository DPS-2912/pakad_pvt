FROM ubuntu:20.04
RUN apt-get update --fix-missing
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:longsleep/golang-backports
RUN apt-get update --fix-missing
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install wireshark
RUN apt-get install -y iptables iproute2 wget golang-go python3-pip
RUN apt-get install -y netcat
RUN pip3 install netifaces
RUN apt-get update && apt-get install -y iputils-ping
RUN python3 -m pip install selenium==4.9.1
RUN python3 -m pip install tbselenium
RUN python3 -m pip install pyvirtualdisplay
RUN python3 -m pip install stem
RUN python3 -m pip install loguru
RUN python3 -m pip install datetime
RUN python3 -m pip install requests
RUN python3 -m pip install argparse
RUN python3 -m pip install stem
RUN python3 -m pip install flask
RUN apt-get install -y wget
RUN apt-get install nano
RUN apt-get update --fix-missing
RUN apt-get install -y firefox
RUN apt-get install -y xvfb
COPY geckodriver-v0.33.0-linux64.tar.gz geckodriver-v0.33.0-linux64.tar.gz
RUN mkdir /gecko
RUN tar -zxf geckodriver-v0.33.0-linux64.tar.gz -C /gecko
RUN apt install -y tor
COPY tor-browser-linux64-12.0.7_ALL.tar.xz tor-browser-linux64-12.0.7_ALL.tar.xz
RUN tar -xf tor-browser-linux64-12.0.7_ALL.tar.xz
COPY app_to_collect_data.py app_to_collect_data.py
RUN apt-get install -y tcpdump
RUN service tor start
RUN pip3 install psutil
CMD exec tail -f /dev/null