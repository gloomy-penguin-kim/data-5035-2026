
import requests
from bs4 import BeautifulSoup, Comment
import re 
from datetime import datetime
from rapidfuzz import fuzz 
import hashlib
from pprint import pprint
import json

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
from transformers import pipeline

emotion = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base"
) 

# def normalize_headline(text: str) -> str:
#     # text = text.lower()
#     # text = re.sub(r'^default:\s*', '', text)  
#     text = re.sub(r'\.\.\.$', '', text)       
#     # text = re.sub(r'\s+', ' ', text)
#     return text.strip()  
 
def parse_drudge(html):

    soup = BeautifulSoup(html, "html.parser")
    results = []

    blocks = soup.find_all("p", style="margin-bottom:4px;")

    for block in blocks:

        strong = block.find("strong")
        if not strong:
            continue

        link = strong.find("a")
        if not link: continue 
        headline = link.get_text(strip=True)
        article_url = link["href"]

        meta = block.find_next(string=re.compile("From the"))
        if not meta:
            continue

        archive_link = meta.find_next("a")
        archive_date = "" 
        edition_time = "" 
        archive_url = "" 
        if archive_link: 
            archive_date = archive_link.get_text(strip=True) 
            archive_url = archive_link["href"] 

            if archive_link.parent: 
                full_text = archive_link.parent.get_text(" ", strip=True)

                time_match = re.search(r"(\d{2}:\d{2}:\d{2})", full_text)
                edition_time = time_match.group(1) if time_match else None

        results.append({
            "headline": headline,
            "article_url": article_url,
            "archive_date": archive_date,
            "edition_time": edition_time,
            "archive_url": archive_url,
        })

    return results 


def process_results(results, query_name): 
    result_array = [] 
    seen_headlines = set()  
    seen_urls = set() 

    for item in results: 
        headline = (item['headline']) 
        article_url = item['article_url']  

        if article_url not in seen_urls:
            seen_urls.add(article_url)

            found = False 
            for seen_headline in seen_headlines:   
                if fuzz.token_set_ratio(seen_headline, headline) >= 95: 
                    found = True
                    break 
            
            if not found:   
                item["query_name"] = query_name
                item["emotion"] = emotion(headline)
                item["scores"] = analyzer.polarity_scores(headline) 
                item["hash"] = hashlib.sha256(headline.encode()).hexdigest()
                item["scraped_at"] = datetime.utcnow().isoformat() 
                result_array.append(item) 
                seen_headlines.add(headline)
                seen_urls.add(item['article_url']) 

    return result_array
  
#######################################################################
# known limitation on data cleansing: 
#######################################################################
# Trump welcomes support from QAnon conspiracy theory...
# Trump dodges question on QANON conspiracy theory...

#######################################################################
# real emotional api
#######################################################################
# url = "https://api.apilayer.com/text_to_emotion" 
# payload = "".encode("utf-8")
# headers= {
#   "apikey": "OISqCVeXyWvs8RMAmzc9ZM2G9xdEZG4F"
# } 
# response = requests.request("POST", url, headers=headers, data = payload) 
# status_code = response.status_code
# result = response.text

#######################################################################
# and then...
#######################################################################
# I want gather, as example ONLY, all the reports on the Moon. And 
# see what aligns with consiracy theories either by date or by similar
# proper nouns or whatever.  See if the Moon, NASA brings in tides and 
# consipiracy theories 

results_array = [] 

# Drudge Report for "Conspiracy Theor" for 2024-03-01 to current day: 
url = 'https://www.drudgereportarchives.com/dsp/search.htm?searchFor=conspiracy+theor&searchStartDate=2024-03-01&searchEndDate=2026-03-01'  

response = requests.get(url) 
results = parse_drudge(response.text)
results_array += process_results(results, "conspiracy theor")

# Drudge Report for "Moon" for 2024-03-01 to current day: 
url = 'https://www.drudgereportarchives.com/dsp/search.htm?searchFor=moon&searchStartDate=2024-03-01&searchEndDate=2026-03-01' 
 
response = requests.get(url) 

results = parse_drudge(response.text)
results_array += process_results(results, "moon")

# Drudge Report for "NASA" for 2024-03-01 to current day: 
url = 'https://www.drudgereportarchives.com/dsp/search.htm?searchFor=nasa&searchStartDate=2024-03-01&searchEndDate=2026-03-01'  
 
response = requests.get(url)
 
results = parse_drudge(response.text)
results_array += process_results(results, "nasa")


import json 
with open("output.json", 'w') as file:
    json.dump(results_array, file, indent=4)
 

#######################################################################
# and then...
#######################################################################
# I want put this data in postgres (because I know how to use it with 
# datagrip) and really analyze it to see if I can find any trends it it.
# With my silly idea of Moon vs Conspiracy Theories it is sort of psuedo
# science but I wanted to get off the easy buzzwords of poltics,
# religion, etc.  




#######################################################################
# after thoughts
#######################################################################
# At least up until a certain time frame, it does allow you to look at the 
# day of data you collected by an archive_url.  That might be easer to cross
# list or find common keywords for.  That is the next real adventure - 
# guessing what might add up or letting the data tell you for you.  I don't
# want to go any further (and hopefully this demonstrated enough...) but
# as a demo.... again, here we have the druge report for "moon"

# Drudge Report for "Moon" for 2024-03-01 to current day: 
url = 'https://www.drudgereportarchives.com/dsp/search.htm?searchFor=moon&searchStartDate=2024-03-01&searchEndDate=2026-03-01'  

results_array = [] 

response = requests.get(url)  
results = parse_drudge(response.text)
results_array += process_results(results, "moon")


stories_days = [] 

for a in results_array: 
    url = a["archive_url"] 
    response = requests.get(url)   
    soup = BeautifulSoup(response.text, "html.parser")
 

    main_block = soup.find("div", id="DR-HU-MAIN")
    main_headlines = []

    if not main_block: continue 

    # this shows as an error down here but runs fine 
    for aa in main_block.find_all("a", href=True):
        text = aa.get_text(strip=True) 

        if text:
            main_headlines.append({
                "headline": text,
                "url": aa["href"],
                "scraped_at": datetime.utcnow().isoformat(),
                "archive_date": a["archive_date"] # TODO: FIX THIS whole situation 
            }) 
  
    # this shows as an error down here but runs fine 
    headline_table = main_block.find_next("table")
    columns = headline_table.find_all("td", width="33%")
    def looks_like_story(text):
        if not text:
            return False
        if len(text) < 25:
            return False
        if "EMAIL:" in text: 
            return False 
        return True


    stories = []

    for col_index, col in enumerate(columns):

        for aa in col.find_all("a", href=True):
            text = aa.get_text(" ", strip=True)

            if looks_like_story(text):
                stories.append({
                    "headline": text,
                    "url": aa["href"],
                    "column": col_index,
                    "archive_date": a["archive_date"],
                    "hash": hashlib.sha256(text.encode()).hexdigest(),
                    "scraped_at": datetime.utcnow().isoformat()  
                })

    stories_days.append(stories)

import json 
with open("output_daily_historic_view.json", 'w') as file:
    json.dump(stories_days, file, indent=4)
pprint(stories_days) 
 
 
#######################################################################
# Now I want to isolate proper or important nouns, let's at least 
# remove a lot of those extra words, I guess...
#######################################################################
# but I will stop here since this requires more eyes than mine if it 
# will be for a group  