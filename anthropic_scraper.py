from bs4 import BeautifulSoup as soup
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper import *
import os

class AnthropicScraper(WebScraper):
    def __init__(self, base_url,max_docs,storage_type):
        """
        Initializes the AnthropicScraper with the base URL and maximum number of documents to scrape.
        Args:
            anthropic_base_url: Url link to anthropic research site
        """
        super().__init__(max_docs,storage_type)
        self.driver = Driver(uc=True, headless=False)
        self.base_url=base_url
        self.storage_type=storage_type

    def run_scraper(self):
        """
        Scrapes the Anthropic research papers and extract their details.
        It uses Selenium to automate the browser and BeautifulSoup for parsing HTML content.
        """

        # Initialize driver
        driver = self.driver
        try:
            driver.get(self.base_url)
            # Utilize delay to allow dynamic content to complete loading
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "PostList_post-card__1g0fm"))
            )
            # Find Parent Class containing links to research Paper
            research_paper_section = driver.find_elements(By.CLASS_NAME, "PostList_post-card__1g0fm")

            count = 0
            # Loop through each research Paper section
            for research_paper in research_paper_section:
                if count >= self.max_docs:
                    print(f"Reached maximum document limit: {self.max_docs}")
                    break
                try:
                    formatted_data=self.get_papers(research_paper)
                    self.print_results(formatted_data) # Print the results
                    store_data=self.storage_handlers.get(self.storage_type)
                    store_data(formatted_data)
                except Exception as e:
                    print(f"Error processing post: {e}")
                count += 1
        finally:
            # Quit WebDriver
            driver.quit()

    def parse_external_link(self, research_link):
        """
        This function is used to parse the external link of the research paper
        and extract the first 1000 characters from the <article> inside the specified div. 
        Args:
            research_link (str): The URL of the research paper.
        """
        driver = self.driver
        # Open the post in a new tab
        driver.execute_script("window.open(arguments[0]);", research_link)
        driver.switch_to.window(self.driver.window_handles[1])  # Switch to new tab
        try:
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
            # Close the new tab and return to the main tab
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            return read_paper_link, excerpt_text
        except Exception as e:
            print(f"Error parsing external link {research_link}: {e}")
            return None, "Error fetching data"
    
    def get_papers(self,research_paper):
        # DOM content containing research paper details 
        html_content = research_paper.get_attribute("outerHTML")
        # Extract the post link
        research_link = research_paper.get_attribute("href")
        current_soup = soup(html_content, "html.parser") # Corrected soup instance
        research_title = current_soup.find("h3", class_="PostList_post-heading__iL3Su").text.strip() if current_soup.find("h3", class_="PostList_post-heading__iL3Su") else "N/A"
        research_date = current_soup.find("div", class_="PostList_post-date__djrOA").text.strip() if current_soup.find("div", class_="PostList_post-date__djrOA") else "N/A"
        
        additional_links, excerpt = self.parse_external_link(research_link)
        
        # Save each part to the 
        formatted_data = self.format_research_paper_data(
            title=research_title,
            authors="",
            date=research_date,
            research_link=research_link.strip(),
            excerpt=excerpt,
            additional_links=additional_links.strip()
            ) # Format the data
        return formatted_data