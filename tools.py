from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import os


load_dotenv()



def web_search(query):
    url = "https://api.tavily.com/search"
    headers = {"Authorization": os.getenv("TAVILY_API")}
    json_body = {
    "query": query,
    "search_depth": "advanced"
    }
    response = requests.post(url, json=json_body, headers=headers)

    search = ""
    for i, r in enumerate(response.json()['results']):
        search += f"Result {i+1}:\nTitle: {r['title']}\nUrl: {r['url']}\n\n"

    print(search)
    return search


def fetch_page(url):
    full_text = ""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    full_text += soup.find('h1').text
    full_text += "\n"
    full_text += soup.find('h2').text
    full_text += "\n"

    paragraphs = [x.text for x in soup.find_all('p')]

    full_text += " ".join(paragraphs)

    return full_text[:3000]
