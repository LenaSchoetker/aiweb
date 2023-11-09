import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser

def get_internal_links(soup, base_url):
    internal_links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and (base_url in href):
            internal_links.append(href)
    return internal_links

def crawl(start_url, base_url, server_domain):
    visited = set()
    stack = [start_url]

    # Create an index to store words and corresponding URLs
    schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True), url=TEXT(stored=True))
    # Create an index in the directory indexdr (the directory must already exist!)
    ix = create_in("indexdir", schema)
    writer = ix.writer()

    while stack:
        current_url = stack.pop()

        if current_url in visited:
            continue

        response = requests.get(current_url, timeout=3)

        if response.status_code == 200 and 'text/html' in response.headers.get('Content-Type', ''):
            soup = BeautifulSoup(response.text, 'html.parser') 

            # Process the page
            title_tag = soup.title
            if title_tag:
                print("Title:", title_tag.text)

            # Extract words from the page's text content
            page_text = soup.get_text()
            writer.add_document(title=title_tag.text, content=page_text, url=current_url)

            visited.add(current_url)
            
            internal_links = get_internal_links(soup, base_url)
            for link in internal_links:
                stack.append(link)

            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    absolute_link = urljoin(start_url, href)
                    parsed_url = urlparse(absolute_link)

                    if parsed_url.netloc == server_domain and absolute_link not in visited:
                        stack.append(absolute_link)

        else:
            print(f"Error: Failed to fetch the page. Status code: {response.status_code}, URL: {current_url}")

    writer.commit()
    return ix  # Return the index when crawling is complete

def search(search_words):
    # Run the crawler and get the index
    ix = crawl(start_url, base_url, server_domain)

    # Initialize an empty list to store the results
    results_list = []

    # Retrieving data
    with ix.searcher() as searcher:
        # find entries with the words 
        query = QueryParser("content", ix.schema).parse(" ".join(search_words))
        results = searcher.search(query)

        # Build a list of dictionaries containing relevant information
        for r in results:
            result_dict = {'title': r['title'], 'url': r['url']}
            results_list.append(result_dict)

    return results_list

    

if __name__ == '__main__':
    start_url = "https://vm009.rz.uos.de/crawl/index.html"
    base_url = "https://vm009.rz.uos.de/crawl"
    server_domain = "vm009.rz.uos.de"
    
    
    # Test the search function with a list of words
    search_words = ["platypus", "sewn"]  # Replace with your search words
    
    results = search(search_words)

    # print all results
    for r in results:
        print(f"Title: {r['title']} - URL: {r['url']}")