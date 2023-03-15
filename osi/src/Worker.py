import sys
import os
import openai
from osi.src.WebScraper import WebScraper
from osi.src.OpenAICaller import OpenAICaller

class Worker:
    """
    The Worker class is responsible for performing the following tasks:
    - Generate search queries
    - Summarize web pages
    - Generate SBAR responses
    """
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.model_name = model_name
        self.scraper = WebScraper()
        self.openai = OpenAICaller(model_name)
        self.config_generate_queries = (
            "Your role is to generate search queries related to a given research topic. Make sure to look for reliable sources."
            "Example:\n\n"
            "Input: 'Renewable energy sources'\n"
            "Output: 'Benefits of renewable energy sources', 'Types of renewable energy, wikipedia', 'Renewable energy technology advancements'"
        )

        self.config_summarize_page = (
            "Your role is to summarize the web page content in under 5 sentences. Ignore it if it's a video or an advertisement or a technical log."
            "Example:\n\n"
            "Input: 'Solar energy is the conversion of sunlight into electricity...'\n"
            "Output: 'Solar energy involves converting sunlight into electricity. It's a clean and renewable source of power.'"
        )

        self.config_sbar_response = (
            "Your role is to provide an SBAR response based on a set of summaries. "
            "Use the SBAR format (Situation, Background, Assessment, Recommendation) for your response. "
            "Example:\n\n"
            "Input: 'Summary 1: Solar energy involves converting sunlight into electricity...'\n"
            "Output: 'Situation: The world is shifting towards renewable energy sources due to environmental concerns. "
            "Background: Solar, wind, and hydropower are some of the most popular renewable energy sources. "
            "Assessment: Renewable energy sources are gaining traction, with advances in technology and decreasing costs. "
            "Recommendation: Investing in renewable energy technologies can help mitigate climate change and promote energy independence.'"
        )

    def log(self, message):
        """Log a message to the console

        Args:
            message (str): Message to log
        """
        print(f"{self.__class__.__name__}: {message}")

    def generate_search_queries(self, research_topic):
        """Generate 3 search queries related to the research topic
        
        Args:
            research_topic (str): Research topic to generate search queries for

        Returns:
            list: List of 3 search queries
        """
        self.log(f"Generating search queries for '{research_topic}'...")

        prompt = self.config_generate_queries + f"Generate 3 search queries related to the research topic: '{research_topic}'."
        response = self.openai.gen_request_to_api(prompt, max_tokens=50, temperature=0.5, n=1, stop=None)
        queries = response.strip().split("\n")
        return [query.strip() for query in queries]

    def summarize_page(self, page_text):
        """Summarize a web page in 2-3 sentences

        Args:
            page_text (str): Text content of the web page
            
        Returns:
            str: Summary of the web page
        """
        self.log(f"Summarizing web page...")

        prompt = self.config_summarize_page + f"Summarize the following content in 5-20 sentences:\n\n{page_text}"
        response = self.openai.gen_request_to_api(prompt, max_tokens=100, temperature=0.5, n=1, stop=None)
        summary = response.strip()
        return summary

    def sbar_response(self, summaries):
        """Generate an SBAR response based on a set of summaries

        Args:
            summaries (str): Summaries of the web pages

        Returns:
            str: SBAR response
        """
        self.log(f"Generating SBAR response...")

        prompt = self.config_sbar_response + f"Provide an SBAR response based on the following summaries:\n\n{summaries}"
        response = self.openai.gen_request_to_api(prompt, max_tokens=500, temperature=0.5, n=1, stop=None)
        sbar = response.strip()
        return sbar

    def perform_task(self, research_topic, depth_n=1):
        # Generate search queries
        search_queries = self.generate_search_queries(research_topic)

        # Scrape and summarize web pages
        all_summaries = []
        for query in search_queries:
            self.log(f"Performing summary for '{query}'...")
            # Use a search engine API or a custom scraper to obtain the URLs of the top x search results for each query
            page_texts = self.scraper.perform_search(query, n_top = depth_n)  # a list of text content of the web pages

            # Summarize the web pages
            for page_text in page_texts:
                summary = self.summarize_page(page_text)
                all_summaries.append(summary)

        # Concatenate summaries
        summaries_text = "\n\n===============================\n\n".join(all_summaries)
        self.log(f"Summaries:\n{summaries_text}")

        # Generate an SBAR response
        sbar = self.sbar_response(summaries_text)

        return sbar
