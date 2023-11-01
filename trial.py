import requests
from bs4 import BeautifulSoup

x = True

def crawler(r):
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')

        while x:#links available on this page or more branches available to follow
            #if page not visited before:
                # List of links on that website
                for l in soup.find_all("a"):
                    print(l)
    else:
        print("Error: Failed to fetch the page. Status code:", r.status_code)

r = requests.get("https://vm009.rz.uos.de/crawl/index.html")
crawler(r)
