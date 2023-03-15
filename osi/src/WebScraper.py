import requests
from bs4 import BeautifulSoup
from googlesearch import search

class WebScraper:
    """WebScraper class to scrape text from a given serch query"""
    def __init__(self):
        pass

    def scrape(self, url):
        """Scrape text from a given url"""
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            text = " ".join([p.get_text() for p in soup.find_all("p")])
            return text
        else:
            return None
        
    def google_search(self, query, num_results=5):
        """Search google for a given query and return a list of urls"""
        urls = []
        try:
            for url in search(query, num_results=num_results):
                urls.append(url)
        except Exception as e:
            print(f"Error while searching: {e}")

        print(f"Found results for '{query}':")
        for url in urls:
            print(f"\t{url}")
        return urls
    
    def perform_search(self, search_query, n_top=1):
        page_texts = []
        
        search_urls = self.google_search(search_query, num_results=n_top)
        for url in search_urls:
            page_text = self.scrape(url)
            if page_text:
                page_texts.append(page_text)

        return page_texts
