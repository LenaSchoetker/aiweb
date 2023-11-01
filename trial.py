import requests
from bs4 import BeautifulSoup

def is_internal_link(url, base_url):
    # Check if the URL is an internal link (within the same server)
    # Returns True or False
    return base_url in url

def get_internal_links(soup, base_url):
    # Find and return all internal links on the page
    internal_links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and is_internal_link(href, base_url):
            internal_links.append(href)
    return internal_links

def crawler(start_url, base_url):
    visited = set()  # Set to keep track of visited pages
    stack = [start_url]  # Stack to store links to visit

    while stack: #links available on this page or more branches available to follow
        current_url = stack.pop()

        # If page visited before, continue
        if current_url in visited:
            continue

        response = requests.get(current_url)
        if response.status_code == 200 and 'text/html' in response.headers.get('Content-Type', ''):
            soup = BeautifulSoup(response.content, 'html.parser')

        #get content
        title_tag = soup.title
        if title_tag:
            print("Title:", title_tag.text)            
            #title_tag.text #text content of a Tag

        #analyze page, update index

        # update visited list
        visited.add(current_url)

        # Find and add internal links to the stack
        internal_links = get_internal_links(soup, base_url)
        for link in internal_links:
            stack.append(link)

    else:
        print("Error: Failed to fetch the page. Status code:", r.status_code)

# Test with given URL
start_url = "https://vm009.rz.uos.de/crawl/index.html"
base_url = start_url.split('/')[2]
crawler(start_url, base_url)
