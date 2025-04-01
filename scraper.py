from typing import NamedTuple, List
import sqlite3
class ResearchPaperSchema(NamedTuple):
    """
    Ensures all API data are in the same format
    Args:
        NamedTuple (_type_): _description_
    """
    title: str
    authors: List[str]
    date: str
    research_link: str
    additional_links: List[str]
    excerpt: str


class WebScraper():
    def __init__(self,base_url,API, max_docs,timeline):
        """
        Describes Base Webscraper

        Args:
            base_url: Base url of site to be scraped
            API : Depends if an API is being used
            max_docs : Maximum number of data to scrape
        """
        self.api=API
        self.base_url=base_url
        self.max_docs = max_docs
        self.timeline = timeline
    
    def save_data_to_db(self, data):
        """
        Saves document title and content to an SQLite database.
        Initializes the database and table if they don't exist.
        """
        # # Connect to an SQLite database (or create it if it doesn't exist)
        conn = sqlite3.connect('scraped_data.db')
        # # Create a cursor object using the cursor() method
        cursor = conn.cursor()
        # # Create table
        cursor.execute('''CREATE TABLE IF NOT EXISTS documents
                    (title TEXT, author TEXT, summary TEXT, link TEXT, date TEXT, additional_link TEXT, excerpt TEXT)''')
        # # Insert a row of data
        cursor.execute("INSERT INTO documents (title,author,summary,link,date, additional_link, excerpt) VALUES (?, ?, ?, ?, ?, ?, ?)", (data["title"], data["authors"], data["summary"], data["research_link"], data["date"], data["additional_links"], data["excerpt"]))
        # # Save (commit) the changes
        conn.commit()
        # # Close the connection
        conn.close()
    
    
    def save_data_to_csv(self, data_list, filename='scraped_data.csv'):
        """
        Saves a list of research paper data to a CSV file.

        Args:
            data_list (list): List of dictionaries, where each dictionary
                               represents a research paper's data.
            filename (str): The name of the CSV file to save to.
        """
        import csv

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Write the header row
            if data_list:
                header = data_list[0]._fields # Use fields from ResearchPaperSchema
                writer.writerow(header)

            # Write data rows
            for data_item in data_list:
                # Format lists to strings for CSV
                row = [str(item) if isinstance(item, list) else item for item in data_item]
                writer.writerow(row)
                
    def print_results(self, data: ResearchPaperSchema):
        """
        Prints the scraped research paper data in a formatted way.

        Args:
            data (ResearchPaperSchema): The scraped data to print.
        """
        print("Scraped Result:")
        print(f"  Title: {data.title}")
        print(f"  Authors: {', '.join(data.authors) if data.authors else 'N/A'}") # Handle cases where authors is None or empty
        print(f"  Date: {data.date}")
        print(f"  Research Link: {data.research_link}")
        print(f"  Additional Links: {', '.join(data.additional_links) if data.additional_links else 'N/A'}") # Handle cases where additional_links is None or empty
        print(f"  Excerpt Preview: {data.excerpt[:200]}...") # Preview excerpt
        print("-" * 80)
    
    