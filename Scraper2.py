# Scrape MedlinePlus Encyclopedia for disease causes
# https://medlineplus.gov/ency/encyclopedia_A.htm

import html
from html.parser import HTMLParser
import time
import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json
import pandas as pd
import urllib.parse
from string import ascii_lowercase
import spacy
#import Summarize

def removeParen(text):
    ret = ""
    inRange = 0
    for i in range(len(text)):
        if text[i] == "(":
            inRange+=1
        if inRange == 0:
            ret+=text[i]
        if text[i] == ")":
            inRange = max(0, inRange-1)
    return ret.strip()

nlp = spacy.load('en_core_web_lg') 

mayo_dict = {}

# get all diseases off of Mayo Clinic
for c in ascii_lowercase:
    url = "https://www.mayoclinic.org/diseases-conditions/index?letter="+c
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        webpage = urlopen(req).read().decode('utf-8')
    except urllib.request.HTTPError as e:
        error_message = e.read()
        print(error_message)
    soup = BeautifulSoup(webpage, 'html.parser')
    main_body = soup.find("div", {"class": "index content-within"})
    list_element = [(removeParen(html.unescape(x.text.strip())), "https://www.mayoclinic.org"+x.find("a", href=True)["href"]) for x in main_body.findAll("li")]
    for item in list_element:
        mayo_dict[item[0].lower()] = item[1]

# trying to match database diseases with mayo clinic diseases

with open('./database.txt') as jsonfile:
    data = json.load(jsonfile)

diseases = data.keys() # top level data

for disease in diseases:
    # find mayo clinic item that most closely matches
    print("Currently on disease: "+disease)
    doc1 = nlp(disease.lower())
    best = ""
    value = -1.0 
    for item in mayo_dict.keys():
        #print(item)
        doc2 = nlp(item)
        sim = doc1.similarity(doc2)
        if sim > value:
            best = item
            value = sim
    data[disease]["MayoClinic"] = mayo_dict[best]

converted_data = json.dumps(data)
out = open("database_with_links.txt", "w")
out.write(converted_data)
out.close()   
