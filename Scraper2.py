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
import Summarize

with open('./database.txt') as jsonfile:
    data = json.load(jsonfile)

diseases = data.keys() # top level data

print(diseases)
