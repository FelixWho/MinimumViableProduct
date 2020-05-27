# Scrape Google

# Things to gather:
# short description
# long description
# symptoms
# screening method

import html
from html.parser import HTMLParser
import time
import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json
import pandas as pd
import urllib.parse

def normalize(str):
    '''
    Normalize strings
    '''
    return str.strip().lower()

data = {}
disease_list = []

f1 = open("nhs_disease_list.txt", "r")
f2 = open("STD.txt", "r")

for line in f1:
    disease_list.append(normalize(line))

for line in f2:
    n = normalize(line)
    if n not in disease_list:
        disease_list.append(n)


for d in disease_list:
    print("Processing: "+d.strip())
    query = urllib.parse.quote(str(d)) # encode it for url

    #overview page
    try:
        req = Request("https://www.google.com/search?q="+str(query), headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        webpage = urlopen(req).read().decode('utf-8')
    except urllib.request.HTTPError as e:
        error_message = e.read()
        print(error_message)
    soup = BeautifulSoup(webpage, 'html.parser')
    description_short = " ".join(html.unescape(x.text) for x in soup.findAll("div", {"data-attrid": "kc:/medicine/disease:description"}))
    description_long = " ".join(html.unescape(x.text) for x in soup.findAll("div", {"data-attrid": "kc:/medicine/disease:long description"}))
    infectiousness = [html.unescape(x.text) for x in soup.findAll("div", {"data-attrid": "kc:/medicine/disease:how it spreads"})]
    name = " ".join(html.unescape(x.text) for x in soup.findAll("span", {"class": "xEaFBe"}))
    data[name] = {}
    if infectiousness:
        data[name]["infectiousness"] = infectiousness
    data[name]["description_long"] = description_short+" "+description_long # this is because they logically flow together
    data[name]["description_short"] = description_short

    #symptoms page
    req = Request("https://www.google.com/search?q="+str(query)+"+symptoms", headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    webpage = urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(webpage, 'html.parser')
    symptoms_short = " ".join(html.unescape(x.text) for x in soup.findAll("div", {"data-attrid": "kc:/medicine/disease:symptoms description"}))
    data[name]["symptoms_description"] = symptoms_short

    #treatment page
    req = Request("https://www.google.com/search?q="+str(query)+"+treatment", headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    webpage = urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(webpage, 'html.parser')
    treatment_simple = ". ".join(html.unescape(x.text) for x in soup.findAll("div", {"data-attrid": "kc:/medicine/disease/treatments:info"}))
    data[name]["treatment_simple"] = treatment_simple

    time.sleep(4) # to avoid HTTP error 429

converted_data = json.dumps(data)

out = open("database.txt", "w")
out.write(converted_data)
out.close()
