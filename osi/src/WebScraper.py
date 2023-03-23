import requests
import os
from bs4 import BeautifulSoup
from googlesearch import search
import time
from tqdm import tqdm

class WebScraper:
    """WebScraper class to scrape text from a given serch query"""
    def __init__(self, engine="google"):
        self.engine = engine

        self.METHODS = {
            "google": self.google_search,
            "bing": self.bing_search,
        }

        if self.engine not in self.METHODS:
            raise ValueError(f"Invalid engine: {self.engine}")

        if self.engine == "bing":
            self.bing_subscription_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
            self.bing_endpoint = os.environ['BING_SEARCH_V7_ENDPOINT'] + "v7.0/search"

    def scrape(self, url):
        """Scrape text from a given url"""
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            text = " ".join([p.get_text() for p in soup.find_all("p")])
            return text
        else:
            return None
        
    def bing_search(self, query, num_results=5):
        """Return a list of urls from a bing search"""
        # Construct a request
        mkt = 'en-US'
        params = { 'q': query, 'mkt': mkt }
        headers = { 'Ocp-Apim-Subscription-Key': self.bing_subscription_key }

        # Call the API
        response = requests.get(self.bing_endpoint, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        counter = 0
        while "webPages" not in search_results:
            if counter > 10:
                break
            response = requests.get(self.bing_endpoint, headers=headers, params=params)
            response.raise_for_status()
            time.sleep(2)
            search_results = response.json()
            print(f"Retrying the search...")
            counter += 1
        
        try:
            search_results = response.json()["webPages"]["value"]
            return [search_result["url"] for search_result in search_results[:num_results]]

        except Exception as ex:
            raise ex
    

    def google_search(self, query, num_results=5):
        """Search google for a given query and return a list of urls"""
        urls = []
        try:
            for url in search(query, num_results=num_results):
                urls.append(url)
        except Exception as e:
            print(f"Error while searching: {e}")

        for url in urls:
            print(f"\t{url}")
        return urls
    

    def internet_search(self, query, num_results=5):
        """Search the internet for a given query and return a list of urls"""
        return self.METHODS[self.engine](query, num_results=num_results)

    def perform_search(self, search_query, n_top=1):
        page_texts = []
        links = []
        
        search_urls = self.internet_search(search_query, num_results=n_top+3)
        for _, url in tqdm(enumerate(search_urls)):
            try:
                page_text = self.scrape(url)
                if page_text:
                    page_texts.append(page_text)
                    links.append(url)
            except Exception as e:
                print(f"Error while scraping: {e}")
                continue

        return page_texts, links
