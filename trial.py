"""import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def get_internal_links(soup, base_url):
    # Find and return all internal links on the page
    internal_links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and (base_url in href):
            internal_links.append(href)
    return internal_links

def crawl(start_url, base_url, server_domain):
    # Initialize a set to keep track of visited pages
    visited = set()
    # Create a stack to store links to visit
    stack = [start_url]

    while stack:
        current_url = stack.pop()

        # If the page has been visited before, skip it
        if current_url in visited:
            continue

        response = requests.get(current_url)

        # Check if the response is an HTML page
        if response.status_code == 200 and 'text/html' in response.headers.get('Content-Type', ''):
            soup = BeautifulSoup(response.content, 'html.parser')

            # Process the page (e.g., extract the title)
            title_tag = soup.title
            if title_tag:
                print("Title:", title_tag.text)

            # Mark the current page as visited
            visited.add(current_url)
            
            # Get internal links on the page
            internal_links = get_internal_links(soup, base_url)
            for link in internal_links:
                stack.append(link)

            # Find and add more internal links from anchor tags
            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    absolute_link = urljoin(start_url, href)
                    parsed_url = urlparse(absolute_link)

                    # Check if the link belongs to the same server and hasn't been visited
                    if parsed_url.netloc == server_domain and absolute_link not in visited:
                        stack.append(absolute_link)

        else:
            print(f"Error: Failed to fetch the page. Status code: {response.status_code}, URL: {current_url}")

if __name__ == '__main__':
    # Test the crawler with the provided URL
    start_url = "https://vm009.rz.uos.de/crawl/index.html"
    base_url = "https://vm009.rz.uos.de/crawl"
    server_domain = "vm009.rz.uos.de"
    crawl(start_url, base_url, server_domain)"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re

# Define a function to extract words from text
def extract_words(text):
    # Use regular expressions to extract words (you can customize the pattern)
    words = re.findall(r'\w+', text.lower())
    return words

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
    index = {}

    while stack:
        current_url = stack.pop()

        if current_url in visited:
            continue

        response = requests.get(current_url, timeout=3)

        if response.status_code == 200 and 'text/html' in response.headers.get('Content-Type', ''):
            soup = BeautifulSoup(response.content, 'html.parser')

            # Process the page
            title_tag = soup.title
            if title_tag:
                print("Title:", title_tag.text)

            # Extract words from the page's text content
            page_text = soup.get_text()
            words = extract_words(page_text)

            # Update the index with words and the current URL
            for word in words:
                if word in index:
                    index[word].append(current_url)
                else:
                    index[word] = [current_url]

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

    return index  # Return the index when crawling is complete

"""if __name__ == '__main__':
    start_url = "https://vm009.rz.uos.de/crawl/index.html"
    base_url = "https://vm009.rz.uos.de/crawl"
    server_domain = "vm009.rz.uos.de"
    
    # Run the crawler and get the index
    index = crawl(start_url, base_url, server_domain)
    
    # Print the index for demonstration
    for word, urls in index.items():
        print(f"Word: {word} -> URLs: {', '.join(urls)}")"""


"""def search(index, words):
    matching_urls = None
    
    # Ensure all words are in lowercase for consistency
    words = [word.lower() for word in words]
    
    for word in words:
        if word in index:
            if matching_urls is None:
                matching_urls = set(index[word])
            else:
                matching_urls = matching_urls.intersection(index[word])

    return list(matching_urls) if matching_urls is not None else []"""

def search(index, words):
    matching_urls = None
    
    # Ensure all words are in lowercase for consistency
    words = [word.lower() for word in words]
    
    for word in words:
        if word in index:
            if matching_urls is None:
                matching_urls = set(index[word])
            else:
                matching_urls = matching_urls.intersection(index[word])

    # Ensure that the matching URLs contain all the specified words
    for url in list(matching_urls):
        url_words = [word.lower() for word in extract_words(requests.get(url).text)]
        if not all(word in url_words for word in words):
            matching_urls.remove(url)

    return list(matching_urls) if matching_urls is not None else []

if __name__ == '__main__':
    start_url = "https://vm009.rz.uos.de/crawl/index.html"
    base_url = "https://vm009.rz.uos.de/crawl"
    server_domain = "vm009.rz.uos.de"
    
    # Run the crawler and get the index
    index = crawl(start_url, base_url, server_domain)
    
    # Test the search function with a list of words
    search_words = ["platypus", "sewn"]  # Replace with your search words
    matching_urls = search(index, search_words)
    
    # Print the URLs that match the search criteria
    if matching_urls:
        print("Matching URLs:")
        for url in matching_urls:
            print(url)
    else:
        print("No matching URLs found.")


