import requests
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
    crawl(start_url, base_url, server_domain)



