# Scrape Google

# Things to gather:
# short description
# long description
# symptoms
# screening method

import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json
import pandas as pd

data = {}

query = str("Scoliosis")
data[query] = {}

#overview page
req = Request("https://www.google.com/search?q="+str(query), headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
webpage = urlopen(req).read().decode('utf-8')
soup = BeautifulSoup(webpage, 'html.parser')
description_short = " ".join(x.text for x in soup.findAll("div", {"data-attrid": "kc:/medicine/disease:description"}))
description_long = " ".join(x.text for x in soup.findAll("div", {"data-attrid": "kc:/medicine/disease:long description"}))
data[query]["description_long"] = description_short+description_long # this is because they logically flow together
data[query]["description_short"] = description_short

#symptoms page
req = Request("https://www.google.com/search?q="+str(query)+"+symptoms", headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
webpage = urlopen(req).read().decode('utf-8')
soup = BeautifulSoup(webpage, 'html.parser')
symptoms_short = " ".join(x.text for x in soup.findAll("div", {"data-attrid": "kc:/medicine/disease:symptoms description"}))
data[query]["symptoms_description"] = symptoms_short

#treatment page
req = Request("https://www.google.com/search?q="+str(query)+"+treatment", headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
webpage = urlopen(req).read().decode('utf-8')
soup = BeautifulSoup(webpage, 'html.parser')
treatment_simple = ". ".join(x.text for x in soup.findAll("div", {"data-attrid": "kc:/medicine/disease/treatments:info"}))
data[query]["treatment_simple"] = treatment_simple

converted_data = json.dumps(data)
print(converted_data)
