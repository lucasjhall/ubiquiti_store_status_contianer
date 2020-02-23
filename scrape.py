#!/usr/bin/env python3

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import json
import requests
import os

display = Display(visible=0, size=(800, 600))
display.start()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.headless = True
driver = webdriver.Chrome(options=chrome_options)

webhook_url = os.environ['SLACK_WEBHOOK']
url = os.environ['URL']
itemName = url.rsplit('/', 1)[-1]
avail = []

driver.get(url)
content = driver.page_source
soup = BeautifulSoup(content,'html.parser')
cart = soup.find(text='Sold Out')

def make_slack_payload(itemName):
    json_payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":red-alert-siren: *Item In Stock* :red-alert-siren: \n The {} is now in stock. \n <{}|Shut up and take my money.>".format(itemName, url)
                }
            }
        ]
    }
    return json_payload

def post_to_slack(json_payload):
    payload = json.dumps(json_payload)
    response = requests.post(webhook_url, data=payload, headers={'Content-Type': 'application/json'})

    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )
    else:
        print("Success, Slack returned code: {}".format(response.status_code))


if cart:
    print("{}: Sold Out".format(itemName))
else:
    print("{}: Available!".format(itemName))
    post_to_slack(make_slack_payload(itemName))
driver.quit()
display.stop()