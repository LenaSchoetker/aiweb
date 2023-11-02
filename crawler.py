import string
from collections import Counter

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def get_words_from_file(file_path):
    try:
        # Open the file in read mode
        with open(file_path, 'r') as file:
            # Read the content of the file
            document = file.read()
            # Split the document into lines
            lines = document.split('\n')
            # Initialize an empty list to store words
            all_words = []

            # Iterate through each line and split it into words
            for line in lines:
                words_in_line = line.split()
                # Add the words to the list
                all_words.extend(words_in_line)

            return all_words

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []


def get_content(link, url, worldslist, dic):
    #get all the text
    text = link.text
    # Create a translation table mapping each punctuation character to None
    translation_table = str.maketrans("", "", string.punctuation)

    # Use translate to remove punctuation from the text
    puncfree = text.translate(translation_table)
    puncfree = puncfree.lower()
    puncfree = puncfree.split()

    #we only need every word once
    puncfree = list(set(puncfree))
    print(puncfree)
    #loop through the text on the page
    for word in puncfree:
        if not word in worldslist:
            #when not in document, add to dictionary with website
            if word not in dict:
                # If the word is not in the dictionary, create a new entry with a list containing the current URL
                dict[word] = [url]
            else:
                # If the word is already in the dictionary, append the current URL to the list
                dict[word].append(url)



def get_internal_links(soup, base_url):
    # Find and return all internal links on the page
    internal_links = []
    #find all links in the html
    for link in soup.find_all("a"):
        href = link.get("href")
        # Use urlparse to get the scheme and netloc of the base URL
        base_parsed = urlparse(base_url)

        # Use urljoin to resolve relative URLs
        resolved_url = urljoin(base_url, href)

        #if the scheme is missing in the htlm, add it
        if not urlparse(resolved_url).scheme:
            resolved_url = f'https://{resolved_url}'

        parsed_url = urlparse(resolved_url)

        #sort out external links
        if(parsed_url.netloc == base_parsed.netloc):
            internal_links.append(resolved_url)
    return internal_links


def crawler(start_url, base_url, dict, words_list):
    visited = []  # list to keep track of visited pages
    stack = [start_url]  # Stack to store links to visit

    while stack:  # links available on this page or more branches available to follow
        #print(visited)
        current_url = stack.pop()

        # If page visited before, continue
        if current_url in visited:
            continue

        #get the url - returs the status code etc.
        response = requests.get(current_url)
        #make sure getting the site worked and it is in html
        if response.status_code == 200 and 'text/html' in response.headers.get('Content-Type', ''):

            #exception for non-html sites
            if "text/html" not in response.headers.get("Content-Type"):
                print(f"Skipping non-HTML content at {current_url}")
                continue

            #parse the site to html
            soup = BeautifulSoup(response.content, 'html.parser')

            # analyze page, update index
            get_content(soup, current_url, words_list, dict)

            # update visited list
            visited.append(current_url)

            # Find and add internal links to the stack
            internal_links = get_internal_links(soup, base_url)

            for link in internal_links:
                stack.append(link)

        else:
            print(f"Error: Failed to fetch the page. Status code: {response.status_code}, URL: {current_url}")
    return visited


# Test with given URL
start_url = "https://vm009.rz.uos.de/crawl/index.html"
base_url = "https://vm009.rz.uos.de/crawl/"
server_domain = "vm009.rz.uos.de"
dict = {}
#get stop words form: https://countwordsfree.com/stopwords
file_path = "words.txt"
words_list = get_words_from_file(file_path)
allpages = crawler(start_url, base_url, dict, words_list)

print(allpages)
print(dict)