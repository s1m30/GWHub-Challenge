# GWHub-Challenge 🚀

## Title: AI Research Web Scraper 📰

### Scrapes Latest Research Papers from Top AI Platforms: Anthropic, Google 🧠

- Anthropic Research Website: [https://www.anthropic.com/research/](https://www.anthropic.com/research/)
- Google Deepmind Research Website: [https://deepmind.google/research/publications/](https://deepmind.google/research/publications/)
- SerpAPI: [https://serpapi.com/](https://serpapi.com/)
  
1.  **Web Scraping Strategy 🕸️**

    - **Approach 🎯**: This project showcases a hybrid approach to web scraping, targeting both DeepMind and Anthropic websites. The Anthropic scraper utilizes Selenium to handle dynamic content, while the DeepMind scraper relies on BeautifulSoup for direct HTML parsing.

    - **Handling Scraping Challenges 🚧**:
      - A significant challenge was the dynamic content loading on the Anthropic research website. Selenium's `WebDriverWait` mechanism was crucial to ensure elements loaded before scraping, making it possible to access research papers.
      ```
      WebDriverWait(driver, 20).until(
      EC.presence_of_element_located((By.CLASS_NAME, "PostList_post-card__1g0fm"))
      )
      ```
      - While the Anthropic website lacked pagination, the DeepMind research site implemented pagination, which was addressed by iteratively scraping pages using a `for` loop which ran based on the maximum number documents a user specified.
      ```
      for item in list_items:
        if self.update_counter(count)>=self.max_docs:
            print(f"Reached maximum document limit:{self.max_docs}")
            return
      ```
      -  Although no major anti-scraping mechanisms were encountered during development, the Anthropic scraper's Selenium foundation allows for future integration of advanced techniques like SeleniumBase's UC (Undetected ChromeDriver) mode to bypass CAPTCHAs and Cloudflare challenges.

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

3.  **API-based Alternatives 🔄**

    - **SerpAPI Google Scholar API**: SerpAPI's Google Scholar API is utilized not only as an alternative data source but also to aggregate a broader range of research papers beyond those exclusively listed on Anthropic and Google DeepMind's websites, enhancing the dataset's comprehensiveness.
    ```
    search = serpapi.Client(api_key=api_key).search(params)
    ```

4. **Optimizing Scraper for long-term Usage**🚀

   To ensure the AI Research Web Scraper remains efficient and scalable over time, especially for large-scale data collection, several optimization strategies can be implemented.
   - **Parallel Processing**:  To significantly speed up scraping, especially when dealing with a large number of research papers or pages, one could implement parallel processing using Python's `multiprocessing` or `asyncio` libraries can be employed to achieve this. 

   - **Distributed Scraping**: For extremely large-scale data collection, one can consider distributing the scraping workload across multiple Ip addresses. This approach not only increases scraping speed but also helps in circumventing IP blocking or rate limiting by distributing requests from different IP addresses. This can be achieved with frameworks like Scrapy with Scrapyd or cloud-based solutions.
     
   - **Caching Mechanisms**: Implement caching to avoid redundant scraping of the same content. HTTP caching can be used to cache responses from websites, and database caching can store already scraped paper metadata to prevent re-scraping.

   - **API-Based Alternatives**:  As highlighted, SerpAPI's Google Scholar API is already integrated as an alternative. APIs are generally more stable, efficient, and less prone to breaking compared to website scraping. Other alternatives include Arxiv and Pubmed APIs. 
   

![Scraper Architecture](https://github.com/user-attachments/assets/9d974b71-de9e-49bf-b24b-aa9fa07c58d1)


