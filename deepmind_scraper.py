import requests
from bs4 import BeautifulSoup as soup
import math
from scraper import *

class DeepMindScraper(WebScraper):
    def __init__(self, base_url, max_docs, storage_type):
        super().__init__(max_docs, storage_type)
        self.base_url=base_url
        self.max_docs=max_docs
        self.storage_type=storage_type
        self.count=0

    def run_scraper(self, links_per_page=20):
        """
        Parses the DeepMind research page to extract publication data.
        This method handles pagination and collects the specified number of links.
        """
        total_pages = math.ceil(self.max_docs / links_per_page)  # Calculate required pages
        # Handle Pagination by looping through each page
        for page_num in range(1, total_pages + 1):
            self.parse(self.base_url,page_num)
           
    def parse_external_link(self, page_link):
         # Fetch additional details from the page_link
        if page_link:
            # Initialize fields to be fetched from the detail page
            excerpt = ""
            additional_link_element = ""
            detail_response = requests.get("https://deepmind.google" + page_link)
            if detail_response.status_code == 200:
                detail_soup = soup(detail_response.text, 'html.parser') # Corrected soup instance

            # Extract excerpt (first <p> inside .publication-page__content)
                excerpt_element = detail_soup.select_one(".publication-page__content p")
                if excerpt_element:
                    excerpt = excerpt_element.text.strip()[:1000]  # Limit to 1000 characters

                # Extract additional link (button with text "View publication")
                a_tag=detail_soup.find("a", class_="button")  # Find all buttons
                if a_tag:
                    span = a_tag.find("span", class_="button__text")  # Look inside for text
                    if span and "View publication" in span.text:
                        additional_link_element = a_tag["href"]
            return excerpt, additional_link_element
        
    def parse(self,base_url,page_num):
        response = requests.get(f"{base_url}{page_num}")
        if response.status_code == 200:
            current_soup = soup(response.text, 'html.parser') # Corrected soup instance

            # Find all list items
            list_items = current_soup.find_all("li", class_="list-compact__item")
            for item in list_items:
                if self.count>=self.max_docs:
                    print(f"Reached maximum document limit:{self.max_docs}")
                    return
                page_link = item.find('a', href=True)['href']
                # Extract date
                date_element = item.find("time")
                date = date_element["datetime"] if date_element else "N/A"
                # Extract title
                title_element = item.find("a", class_="list-compact__link")
                title = title_element.text.strip() if title_element else "N/A"
                # Extract authors
                authors_element = item.find_all("dd")[2] if len(item.find_all("dd")) > 2 else None
                authors = authors_element.text.strip() if authors_element else "N/A"

                excerpt, additional_link_element = self.parse_external_link(page_link)
                # Store extracted data
                formatted_data=self.format_research_paper_data(
                    research_link="https://deepmind.google"+ page_link, # Corrected key
                    date= date,
                    title=title,
                    authors= authors.strip(),
                    excerpt= excerpt,
                    additional_links= additional_link_element.strip() # Corrected key
                )
                
                self.print_results(formatted_data) # Print the results
                store_data=self.storage_handlers.get(self.storage_type)
                store_data(formatted_data)
                self.count += 1  # Update count

        else:
            print(f"Failed to fetch page {base_url}{page_num}. Status code: {response.status_code}")
            return  # Exit gracefully instead of crashing

      
    
