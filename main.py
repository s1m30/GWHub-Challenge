import os
from dotenv import load_dotenv
from api import SerpAPISearch
from anthropic_scraper import AnthropicScraper
from deepmind_scraper import DeepMindScraper

if __name__=="__main__":
    #SerpAPI test
    # load_dotenv()
    # api_key = os.environ.get("serpapi_key")
    # serp_engine="google_scholar"
    # print(SerpAPISearch(topic="Biology of Large Language Models",max_docs=7,start_year=2022, engine=serp_engine, api_key=api_key))

    #AnthropicScraper test
    # anthropic_base_url="https://www.anthropic.com/research"
    # ap=AnthropicScraper(base_url=anthropic_base_url,max_docs=7,storage_type="db")
    # ap.run_scraper()

    #DeepMindScraper test
    deepmind_base_url="https://deepmind.google/research/publications/?page="
    dm=DeepMindScraper(base_url=deepmind_base_url,max_docs=5,storage_type="csv")
    dm.run_scraper()