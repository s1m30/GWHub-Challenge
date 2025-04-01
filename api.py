import serpapi
from typing import List
from scraper import *
# Assuming ResearchPaperSchema is defined in scraper.py or a shared location
from scrapers import ResearchPaperSchema  # Import ResearchPaperSchema

#API Studio
def SerpAPISearch(topic, max_docs, start_year, engine, api_key):
    """
    Utilizes SerpAPI API
    Args:
        topic: Topic of research paper(s).
        max_docs: Number of research paper(s) to return.
        start_year: From the start year to the present.
        engine: SerpAPI's engine providers (e.g., "google_scholar", "google").
        api_key: SerpAPI key

    Returns:
        List[ResearchPaperSchema]: A list of ResearchPaperSchema objects.
    """

    params = {
        "engine": engine,  # required
        "q": topic,  # required
        "as_ylo": start_year,
        "num": max_docs
    }

    search = serpapi.Client(api_key=api_key).search(params)  # required
    publications = []
    organic_results = search.get("organic_results", [])  # Handle cases where organic_results is missing

    for result in organic_results:
        title = result.get("title", "N/A")
        research_link = result.get("link", "N/A")
        excerpt = result.get("snippet", "N/A")

        inline_links_data = result.get("inline_links", [])
        additional_links = [link.get("related_pages_link", "N/A") for link in inline_links_data]

        publication_info = result.get("publication_info", {})
        authors = [author.get("name", "N/A") for author in publication_info.get("authors", [])]
        date = publication_info.get("date", "N/A") # Extract date from publication info if available, otherwise N/A

        # Create ResearchPaperSchema instance
        research_paper = ResearchPaperSchema(
            title=title,
            authors=authors,
            date=date,
            research_link=research_link,
            additional_links=additional_links,
            excerpt=excerpt
        )
        publications.append(research_paper)

    return publications
