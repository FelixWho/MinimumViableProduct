import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json
import pandas as pd

# usage: python CommonDisease.py
# description: writes all diseases listed on the following website to a file
# source of diseases: https://www.nhsinform.scot/illnesses-and-conditions/a-to-z

req = Request("https://www.nhsinform.scot/illnesses-and-conditions/a-to-z", headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
webpage = urlopen(req).read().decode('utf-8')
soup = BeautifulSoup(webpage, 'html.parser')
f = open("nhs_disease_list.txt", "w")
for x in soup.findAll("h2", {"class": "module__title"}):
    f.write(x.text.strip()+"\n")
f.close()
