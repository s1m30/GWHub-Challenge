import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get("serpapi_key")

from api import SerpAPISearch
from scrapers import AnthropicScraper, DeepMindScraper
anthropic_base_url="https://www.anthropic.com/research"
deepmind_base_url="https://deepmind.google/research/publications/?page="
serp_engine="google_scholar"

if __name__=="__main__":
    #SerpAPI test
    print("api key",api_key)
    # print(SerpAPISearch("Biology of Large Language Models",7,2022, serp_engine, api_key))

    #AnthropicScraper test
    ap=AnthropicScraper(anthropic_base_url,7)
    ap.browse_automation()

    #DeepMindScraper test
    print(DeepMindScraper(deepmind_base_url,1))
