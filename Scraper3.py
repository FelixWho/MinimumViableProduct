# Find associated MedlinePlus Encyclopedia entry
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
from string import ascii_uppercase
import spacy
import editdistance
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

def removeDash(text):
    sp = text.split(" - ")
    return sp[0]

nlp = spacy.load('en_core_web_lg') 

medline_dict = {}

# get all diseases off of MedlinePlus
for c in ascii_uppercase:
    url = "https://medlineplus.gov/ency/encyclopedia_"+c+".htm"
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        webpage = urlopen(req).read().decode('utf-8')
    except urllib.request.HTTPError as e:
        error_message = e.read()
        print(error_message)
    soup = BeautifulSoup(webpage, 'html.parser')
    main_body = soup.find("ul", {"id": "index"})
    list_element = [(removeDash(removeParen(html.unescape(x.text.strip()))), "https://medlineplus.gov/ency/"+x.find("a", href=True)["href"]) for x in main_body.findAll("li")]
    for item in list_element:
        medline_dict[item[0].lower()] = item[1]
        #print(item[0]+" : "+item[1])

#
# trying to match database diseases with medlineplus diseases
#

with open('./database_with_mayolinks.txt') as jsonfile:
    data = json.load(jsonfile)

diseases = data.keys() # top level data

for disease in diseases:
    # find mayo clinic item that most closely matches
    print("Currently on disease: "+disease)
    doc1 = nlp(disease.lower())
    best = ""
    value = -1.0 
    lowest_edit_distance = 1000
    best_using_dist = ""
    if disease.lower() in medline_dict.keys():
        data[disease]["Medline"] = medline_dict[disease.lower()]
        continue
    for item in medline_dict.keys():
        #print(item)
        dist = editdistance.eval(disease.lower(), item)
        if dist < lowest_edit_distance:
            lowest_edit_distance = dist
            best_using_dist = item
        doc2 = nlp(item)
        sim = doc1.similarity(doc2)
        if sim > value:
            best = item
            value = sim
    if value > 0:
        data[disease]["Medline"] = medline_dict[best]
    else:
        data[disease]["Medline"] = medline_dict[best_using_dist]

converted_data = json.dumps(data)
out = open("database_with_mayo_and_medline_links.txt", "w")
out.write(converted_data)
out.close()   
