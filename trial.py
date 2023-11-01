import requests
from bs4 import BeautifulSoup

def crawler(start_url):
    visited = set()  # Set to keep track of visited pages
    stack = [start_url]  # Stack to store links to visit

    if start.status_code == 200:

        while stack: #links available on this page or more branches available to follow
            current_url = stack.pop()

            #if page visited before, continue:
            if current_url in visited:
                continue

            response = requests.get(current_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            #get content
            title_tag = soup.title
            if title_tag:
                print("Title:", title_tag.text)            
                #title_tag.text #text content of a Tag

            #analyze page, update index
            # List of links on that website
            for l in soup.find_all("a"):
                print(l)
                # add links to the stack (push)

            # update visited list
            visited.add(current_url)
    else:
        print("Error: Failed to fetch the page. Status code:", r.status_code)

start = requests.get("https://vm009.rz.uos.de/crawl/index.html")
crawler(start)
