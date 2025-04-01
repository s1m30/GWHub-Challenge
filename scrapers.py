import requests
from bs4 import BeautifulSoup as soup
from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import math
from scraper import *

#Anthropic API
service = Service(executable_path="chromedriver.exe")

def format_research_paper_data(data):
    """
    Formats raw data into ResearchPaperSchema, ensuring 'additional_links' is a list.
    """
    authors = data.get("authors", "N/A")
    if not isinstance(authors, list):  # Ensure authors is always a list
        authors = [authors] if authors != "N/A" else []

    additional_links = data.get("additional_links", [])
    if isinstance(additional_links, str):  # Ensure additional_links is always a list
        additional_links = [additional_links]
    elif additional_links is None:
        additional_links = []

    return ResearchPaperSchema(
        title=data.get("title", "N/A"),
        authors=authors,
        date=data.get("date", "N/A"),
        research_link=data.get("research_link", data.get("link", "N/A")),  # Handles both keys
        additional_links=additional_links,
        excerpt=data.get("excerpt", "N/A")
    )
    
        
class AnthropicScraper(WebScraper):
    def __init__(self, anthropic_base_url, max_docs, timeline=None):
        """
        Webscraper for scraping papers from the Anthropic research website
        Args:
            anthropic_base_url: Url link to anthropic research site
        """
        super().__init__(anthropic_base_url, None, max_docs, timeline)
        self.anthropic_base_url = anthropic_base_url
        self.driver = webdriver.Chrome(service=service)
        
    def browse_automation(self):
        # Initialize driver
        # Utilize delay to allow dynamic content to complete loading
        driver = self.driver
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "PostList_post-card__1g0fm"))
        )
        # Find Parent Class containing links to research Paper
        research_paper_section = driver.find_elements(By.CLASS_NAME, "PostList_post-card__1g0fm")
        
        count = 0
        data = []
        individual_data = {}
        # Loop through each research Paper section
        for research_paper in research_paper_section:
            try:
                # DOM content containing research paper details 
                html_content = research_paper.get_attribute("outerHTML")
                # Extract the post link
                research_link = research_paper.get_attribute("href")
                current_soup = soup(html_content, "html.parser") # Corrected soup instance
                research_title = current_soup.find("h3", class_="PostList_post-heading__iL3Su").text.strip() if current_soup.find("h3", class_="PostList_post-heading__iL3Su") else "N/A"
                research_category = current_soup.find("span", class_="text-label").text.strip() if current_soup.find("span", class_="text-label") else "N/A"
                research_date = current_soup.find("div", class_="PostList_post-date__djrOA").text.strip() if current_soup.find("div", class_="PostList_post-date__djrOA") else "N/A"
                
                research_links, excerpt = self.parse_external_link(research_link)
                
                # Save each part to the 
                individual_data["research_link"] = research_link # Corrected key
                individual_data["date"] = research_date
                individual_data["title"] = research_title
                individual_data["additional_links"] = research_links
                individual_data["excerpt"] = excerpt
                formatted_data = format_research_paper_data(individual_data) # Format the data
                data.append(formatted_data) # Append the formatted data
                count += 1
            
            except Exception as e:
                print(f"Error processing post: {e}")

        # Close the new tab and return to the main tab (moved outside loop)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        # Quit WebDriver
        driver.quit()
        return data

    def parse_external_link(self, research_link):
        """
        Args:
            bs4_object: BeautifulSoup Object
        """
        driver = self.driver
        # Open the post in a new tab
        driver.execute_script("window.open(arguments[0]);", research_link)
        driver.switch_to.window(self.driver.window_handles[1])  # Switch to new tab
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Create beautifulSoup object
        detail_soup = soup(driver.page_source, "html.parser") # Corrected soup instance
        # Extract "Read Paper" link if available
        read_paper_link = None
        article_tag = detail_soup.find("article")
        if article_tag and article_tag.find("a"): # Added check for article_tag
            read_paper_link = [a.get("href") for a in article_tag.find_all("a", href=True)]

        # Extract the first 1000 characters from <article> inside the specified div
        article_div = detail_soup.find("div", class_="PostDetail_post-detail__6Ldh_")
        if article_div:
            article = article_div.find("article")
            if article:
                excerpt_text = article.get_text(strip=True)[:1000]  # First 1000 characters
            else:
                excerpt_text = "No article found"
        else:
            excerpt_text = "No post detail section found"

        return read_paper_link, excerpt_text


class DeepMindScraper(WebScraper):
    def __init__(self, base_url, max_docs, timeline):
        super().__init__(base_url, None, max_docs, timeline)

    def parse(self, base_url, max_links, links_per_page=20):
        """
        Utilizes BeautifulSoup to parse the deepmind website
        Args:
            base_url (_type_): _description_
            max_links (_type_): _description_
            links_per_page (int, optional): _description_. Defaults to 20.

        Returns:
            _type_: _description_
        """
        publications = []  # List to store extracted data
        total_pages = math.ceil(max_links / links_per_page)  # Calculate required pages

        # Handle Pagination by looping through each page
        for page_num in range(1, total_pages + 1):
            response = requests.get(f"{base_url}{page_num}")
            if response.status_code == 200:
                current_soup = soup(response.text, 'html.parser') # Corrected soup instance

                # Find all list items
                list_items = current_soup.find_all("li", class_="list-compact__item")
                for item in list_items:
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
                    publication_data = { # Use a dict to collect data
                        "research_link":"https://deepmind.google"+ page_link, # Corrected key
                        "date": date,
                        "title": title,
                        "authors": authors,
                        "excerpt": excerpt,
                        "additional_links": additional_link_element # Corrected key
                    }
                    formatted_data = format_research_paper_data(publication_data) # Format data
                    publications.append(formatted_data) # Append formatted data

                    # Stop collecting if we reach max_links
                    if len(publications) >= max_links:
                        return publications

            else:
                print(f"Failed to retrieve page {page_num}. Status code: {response.status_code}")
                break  # Stop on failed request

        return publications[:max_links]  # Trim extra entries if needed

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
                for a_tag in detail_soup.find_all("a", class_="button"):  # Find all buttons
                    span = a_tag.find("span", class_="button__text")  # Look inside for text
                    if span and "View publication" in span.text:
                        additional_link_element = a_tag["href"]
                        break
            return excerpt, additional_link_element
