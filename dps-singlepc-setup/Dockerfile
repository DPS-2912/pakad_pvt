FROM ubuntu:20.04
ENV DISPLAY=:99
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
RUN wget -O /tmp/geckodriver.tar.gz "https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz" && \
    tar -xvzf /tmp/geckodriver.tar.gz -C /usr/bin/ && \
    chmod +x /usr/bin/geckodriver && \
    rm /tmp/geckodriver.tar.gz
WORKDIR /app
COPY websites.csv /app/
COPY app_to_collect_data.py /app/
RUN apt-get install -y tcpdump
RUN apt-get update && apt-get install -y tshark
RUN pip3 install psutil
CMD exec tail -f /dev/null
