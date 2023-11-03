import bs4
import requests
import nltk
from nltk.corpus import stopwords
import re

def extract_urls(found_url:list, base_url:str)-> list:
    """format the urls found on the website to absolute urls and return them as a list of strings, which will be added to the stack

    Args:
        found_url (list): the urls found on the current website
        base_url (str): the currently visited url

    Returns:
        list: the list of absolute urls
    """

    list = [] #list of absolute urls

    for url in found_url: #iterate over all urls found on the website

        if url.has_attr('href'): #check if the url has a href attribute

            url = url["href"] #get the value of the href attribute
        else:
            continue

        #case 1: url is absolute,
        if url.startswith('http'): #TODO: Naja, ne
            list.append(url)

        #Case 2 url is relative (everything after domainending)
        elif url.startswith('/'):
            match = re.match(r'^https?://[^/]+', base_url).group(0) #return everthing until the domain ending E.g /startseite/
            list.append(match + url)

        #case 3 url is relative (only extension to path or needs to replace the current path (after last /)) E.g. #c251337
        else:
            #print("3",base_url.rsplit("/", 1)[0] + url)
            list.append(base_url.rsplit("/", 1)[0] +"/" + url)

    return list

def update_index(index:dict , word: str, url: str, count:int )-> dict:
    """ update the index dictionary with the new word and its count

    Args:
        index (dict): a dictionary with words as keys and a list of tuples (url, count) as values
        word (str): the word to be added or updated to the index
        url (str): the url where the word was found
        count (int): the number of appearances of the word on the website

    Returns:
        dict: the updated index
    """

    if word not in index: #if the word is not in the index yet, add it
        index[word] = []

    if (url, count) not in index[word]: #avoid double entries

        index[word].append((url, count))

    return index

def crawl(url:str) -> None:

    index = {} #dictionary with words as keys and a list of tuples (url, count) as values

    visited = [] #keep track of visited urls
    stack = [url] #stack of urls to visit

    while stack:
        
        current_url = stack.pop(0) #get first element of stack
        print(current_url)

        if current_url not in visited: #avoid double entries/loops
            
            visited.append(current_url)

            try:
                r = requests.get(current_url) #send GET request
            except Exception as e:
                print(e)
                continue

            if r.status_code == 200:
                soup = bs4.BeautifulSoup(r.content, 'html.parser') #parse the content of the website
                soup_text = re.sub(r'[^a-zA-Z0-9\s]', '', soup.text.lower()) #remove special characters and make everything lowercase

                #TODO: find language of website
                stop_words = stopwords.words('english')

                #Tokenize the text   
                for w in soup_text.split():

                    if w not in stop_words: #ignore stop words

                        freq = soup_text.count(w) #count the number of appearances of the word
                        index = update_index(index, w, current_url, freq)

                new_urls = soup.findAll('a') #find all links on the website

                if new_urls:
                    stack[len(stack):] = extract_urls(new_urls, current_url) #add new urls to stack

    return index


if __name__ == '__main__':

    nltk.download('stopwords')

    index = crawl('https://vm009.rz.uos.de/crawl/index.html')  

    #print(indx)
