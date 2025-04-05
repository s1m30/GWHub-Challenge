import serpapi
from scraper import *

class SerpAPISearch(WebScraper):
    def __init__(self,topic, max_docs, start_year, engine, api_key,storage_type):
        """
        Utilizes SerpAPI API
        Args:
            topic: Topic of research paper(s).
            max_docs: Number of research paper(s) to return.
            start_year: From the start year to the present.
            engine: SerpAPI's engine providers (in this case "google_scholar").
            api_key: SerpAPI key
        """
        super().__init__(max_docs,storage_type)
        params = {
            "engine": engine,  # required
            "q": topic,  # required
            "as_ylo": start_year,
            "num": max_docs
        }
        try:
            search = serpapi.Client(api_key=api_key).search(params)  # required
            organic_results = search.get("organic_results", [])  # Handle cases where organic_results is missing

            for result in organic_results:
                title = result.get("title", "N/A")
                research_link = result.get("link", "N/A")
                excerpt = result.get("snippet", "N/A")

                inline_links_data = result.get("inline_links", [])
                additional_links = [link.get("related_pages_link", "N/A") for link in inline_links_data]

                publication_info = result.get("publication_info", {})
                authors = ",".join([author.get("name", "N/A") for author in publication_info.get("authors", [])])
                date = publication_info.get("date", "N/A") # Extract date from publication info if available, otherwise N/A

                # Create ResearchPaperSchema instance
                formatted_data = self.format_research_paper_data(
                    title=title,
                    authors=authors,
                    date=date,
                    research_link=research_link,
                    additional_links=additional_links,
                    excerpt=excerpt
                )
                self.print_results(formatted_data) # Print the results
                store_data=self.storage_handlers.get(self.storage_type)
                store_data(formatted_data)
        except Exception as e:
            print(f"Error fetching data from SerpAPI: {e}")
            return

        
