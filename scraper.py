from typing import NamedTuple, List,Literal
import sqlite3
class ResearchPaperSchema(NamedTuple):
    """
    Ensures all API data are in the same format
    """
    title: str
    authors: str
    date: str
    research_link: str
    additional_links: str
    excerpt: str


class WebScraper():
    def __init__(self,max_docs:int,storage_type:Literal["csv", "db"]):
        """
        Describes Base Webscraper

        Args:
            base_url: Base url of site to be scraped
            API : Depends if an API is being used
            max_docs : Maximum number of data to scrape
        """
        self.max_docs = max_docs
        self.storage_type = storage_type
        self.storage_handlers= {
            "csv": self.save_data_to_csv,
            "db": self.save_data_to_db
        }
    
    def save_data_to_db(self, data,file_name="scraped_data.db"):
        """
        Saves document title and content to an SQLite database.
        Initializes the database and table if they don't exist.
        """
        # # Connect to an SQLite database (or create it if it doesn't exist)
        conn = sqlite3.connect(file_name)
        # # Create a cursor object using the cursor() method
        cursor = conn.cursor()
        # # Create table
        cursor.execute('''CREATE TABLE IF NOT EXISTS documents
                    (title TEXT, author TEXT, link TEXT, date DATE, additional_link TEXT, excerpt TEXT)''')
        # # Insert a row of data
        cursor.execute("INSERT INTO documents (title,author,link,date, additional_link, excerpt) VALUES (?, ?, ?, ?, ?, ?)", (data.title, data.authors, data.research_link, data.date, data.additional_links, data.excerpt))
        # # Save (commit) the changes
        conn.commit()
        # # Close the connection
        conn.close()
    
    
    def save_data_to_csv(self, data, filename='scraped_data.csv'):
        """
        Saves research paper data to a CSV file.
        """
        import os
        import csv 
        
        file_exists = os.path.isfile(filename)  # Check if file exists

        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Write the header only if the file is new
            if not file_exists:
                header = data._fields  # Use fields from ResearchPaperSchema
                writer.writerow(header)

            # Format lists to strings for CSV
            row = [str(item) if isinstance(item, list) else item for item in data]
            writer.writerow(row)
                
    def format_research_paper_data(self, title, authors, date, research_link, additional_links, excerpt):
        """
        Formats raw data into ResearchPaperSchema.
        """
        # Create and return a ResearchPaperSchema instance
        return ResearchPaperSchema(
            title=title,
            authors=authors or "N/A",
            date=date or "N/A",
            research_link=research_link,
            additional_links=additional_links or "N/A",
            excerpt=excerpt 
        )
                
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
    
    