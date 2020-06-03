# scrape causes from Medline link

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
from deeppavlov import build_model, configs
import re
import unicodedata

m = build_model(configs.squad.squad, download=True)

with open('./database_with_mayo_and_medline_links.txt') as jsonfile:
    data = json.load(jsonfile)

diseases = data.keys()

for disease in diseases:
    # MEDLINE
    
    url = data[disease]["Medline"]
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        webpage = urlopen(req).read().decode('utf-8')
    except urllib.request.HTTPError as e:
        error_message = e.read()
        print(error_message)
    soup = BeautifulSoup(webpage, 'html.parser')
    main_body = soup.find("div", {"id": "section-1"})
    if not main_body:
        continue
    medline_text = unicodedata.normalize("NFKD", html.unescape(main_body.text.strip()))
    

    # MAYO CLINIC
    url = data[disease]["MayoClinic"]
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        webpage = urlopen(req).read().decode('utf-8')
    except urllib.request.HTTPError as e:
        error_message = e.read()
        print(error_message)
    soup = BeautifulSoup(webpage, 'html.parser')
    pattern = re.compile(r'Causes')
    causes_header = soup.find('h2', text=pattern)
    if not causes_header:
        continue
    mayo_text = ""
    ne = causes_header.next
    while ne is not None and ne.name != "h1" and ne.name != "h2" and ne.name != "h3":
        #mayo_text+=ne.text
        if ne.string:
            mayo_text+=unicodedata.normalize("NFKD", html.unescape(ne.string))
        ne=ne.next
    
    medline_text = medline_text.strip()
    mayo_text = mayo_text.strip()
    #all_text = medline_text+"\n"+mayo_text
    all_text = mayo_text
    print(disease +": "+ str(m([all_text],["What causes "+disease+"?"])))

    



