import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

"""def is_internal_link(url, base_url):
    # Check if the URL is an internal link (within the same server)
    # Returns True or False
    return base_url in url"""

def get_internal_links(soup, base_url):
    # Find and return all internal links on the page
    internal_links = []
    for link in soup.find_all("a"):
        #print(link)
        href = link.get("href")
        #print(href)
        if href and (base_url in href): #is_internal_link(href, base_url):
            internal_links.append(href)
    return internal_links


def crawler(start_url, base_url, server_domain):
    visited = set()  # list to keep track of visited pages
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

            print(visited)
        else:
            print(f"Error: Failed to fetch the page. Status code: {response.status_code}, URL: {current_url}")


# Test with given URL
start_url = "https://vm009.rz.uos.de/crawl/index.html"
base_url = "https://vm009.rz.uos.de/crawl"
server_domain = "vm009.rz.uos.de"
crawler(start_url, base_url, server_domain)
