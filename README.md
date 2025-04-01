# GWHub-Challenge 🚀

## Title: AI Research Web Scraper 📰

### Scrapes Latest Research Papers from Top AI Platforms: Anthropic, Google 🧠

1.  **Web Scraping Strategy 🕸️**

    - **Approach 🎯**: This project showcases a hybrid approach to web scraping, targeting both DeepMind and Anthropic websites. The Anthropic scraper utilizes Selenium to handle dynamic content, while the DeepMind scraper relies on BeautifulSoup for direct HTML parsing.

    - **Handling Scraping Challenges 🚧**: A significant challenge was the dynamic content loading on the Anthropic research website. Selenium's `WebDriverWait` mechanism was crucial to ensure elements loaded before scraping, making it possible to access research papers. While the Anthropic website lacked pagination, the DeepMind research site implemented pagination, which was addressed by iteratively scraping pages using a `while` loop until no more content was found. Although no major anti-scraping mechanisms were encountered during development, the Anthropic scraper's Selenium foundation allows for future integration of advanced techniques like SeleniumBase's UC (Undetected ChromeDriver) mode to bypass CAPTCHAs and Cloudflare challenges.

    - **Data Format 🗂️**: A uniform data schema was defined for both web scrapers and API tools to ensure consistency. The schema includes the following fields:

    ```json
    {
      "title": "Title of Research Paper",
      "authors": "Authors of Research Paper",
      "date": "Date of Research Paper Release",
      "research_link": "Direct link to the research paper",
      "additional_links": "Links featured in the paper",
      "excerpt": "Short excerpt from the paper"
    }
    ```

    - **Python Libraries 🐍**:
      - Selenium: Employed to handle dynamic content loading on websites like Anthropic's, which is not directly achievable with BeautifulSoup.
      - BeautifulSoup and Requests: Used for direct parsing of the Google DeepMind website's HTML structure.
      - SeleniumBase (Future Integration): While not currently implemented, SeleniumBase can be integrated to enhance the existing Selenium setup, particularly for bypassing anti-scraping measures.

2.  **Data Processing and Optimization ⚙️**

    - **Data Pre-processing 🧹**: For the current tasks, extensive data pre-processing is not necessary as the scraped data is mostly straightforward. While some missing values may exist, they do not significantly impact the intended applications. However, for in-depth data analysis applications, the Pandas framework would be utilized to manage missing or duplicate data effectively.

    - **Data Preparation for Specific Tasks 📝**:

      - **Task 1: AI Research Paper Collator Website 🌐**: For creating a regularly updated website showcasing the latest AI research, no data conversion is needed. The scraped data can be directly used to populate the website.

      - **Task 2: LLM-Paired Research Assistant Database 🤖**: To create a research assistant, the database can be integrated with an LLM using either Retrieval Augmented Generation (RAG) or as a tool for direct lookup. For RAG implementation, embedding the titles and excerpts would enable vector search capabilities, which can be supported by databases like Supabase or Pinecone. When used as a tool, the LLM can translate user prompts into SQL queries to retrieve relevant research papers.

      - **Task 3: Data Analysis and Visualizations 📊**:
        - **Number of Papers per Author**: This analysis requires extracting author names from the data and counting paper contributions per author.
        - **Visualization of Similar Papers**: To visualize similar papers, embedding titles and excerpts would be necessary to calculate similarity metrics.
        - **Analysis by Date**: No specific data processing is required for date-based analysis.

3.  **API-based Alternatives 🔄**

    - **SerpAPI Google Scholar API**: SerpAPI's Google Scholar API is utilized not only as an alternative data source but also to aggregate a broader range of research papers beyond those exclusively listed on Anthropic and Google DeepMind's websites, enhancing the dataset's comprehensiveness.

![Scraper Architecture](https://github.com/user-attachments/assets/9d974b71-de9e-49bf-b24b-aa9fa07c58d1)
