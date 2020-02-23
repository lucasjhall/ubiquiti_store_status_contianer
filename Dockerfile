FROM ubuntu:latest

RUN apt-get update && apt-get install -qq -y xvfb chromium-chromedriver python3-pip

ENV INSTALL_PATH /scape
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY scrape.py .
RUN chmod +x scrape.py

CMD ./scrape.py
