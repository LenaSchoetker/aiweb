import bs4
import requests
import nltk
from nltk.corpus import stopwords
import re

from whoosh.index import create_in, Index, open_dir
from whoosh.fields import Schema, TEXT

from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh import highlight
from whoosh.query import Term



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
        if url.startswith('http'): 
            list.append(url)

        #Case 2 url is relative (everything after domainending)
        elif url.startswith('/'):
            match = re.match(r'^https?://[^/]+', base_url).group(0) #return everthing until the domain ending 
            list.append(match + url) # url is E.g /startseite/

        #case 3 url is relative (only extension to path or needs to replace the current path (after last /)) E.g. #c251337
        else:
            #print("3",base_url.rsplit("/", 1)[0] + url)
            list.append(base_url.rsplit("/", 1)[0] +"/" + url)

    return list

def crawl(url:str) -> None:

    start_server = re.search(r'\/\/([^/]+)', url).group(1) #get the server of the url to avoid crawling other servers
    print("setting the start server to: ", start_server)

    #create index
    schema = Schema(title=TEXT(stored=True),content=TEXT(stored=True), url=TEXT(stored=True))
    ix = create_in("indexdir", schema) 
    writer = ix.writer() 

    visited = [] #keep track of visited urls
    stack = [url] #stack of urls to visit

    while stack:
        
        current_url = stack.pop(0) #get first element of stack

        if current_url not in visited and start_server ==  re.search(r'\/\/([^/]+)', current_url).group(1): #avoid double entries/loops
            
            print("currently visiting: ", current_url)

            visited.append(current_url)

            try:
                r = requests.get(current_url) #send GET request
            except Exception as e:
                print(e)
                continue

            if r.status_code == 200:
                soup = bs4.BeautifulSoup(r.content, 'html.parser') #parse the content of the website
                print(soup.body.get_text(separator=' '))

                writer.add_document(title= soup.title.text, content=soup.body.get_text(separator=' '), url=current_url) #add the document to the index

                new_urls = soup.findAll('a') #find all links on the website

                if new_urls:
                    stack[len(stack):] = extract_urls(new_urls, current_url) #add new urls to stack

    writer.commit()
    return ix

def search(query:str) -> list:
    """
    search for the query in the index and return the urls where the query was found

    Args:
        query (str): the query to be searched for
    """

    index = open_dir("indexdir")
    out = []
    
    with index.searcher() as searcher:
        corrector = searcher.corrector("content")

        p_query = QueryParser("content", index.schema).parse(query)
        querylist = query.split()

        # Extract terms from the parsed query
        terms = p_query.all_terms()

        # Replace each term with its most similar index entry
        for term in terms:
            corrected_term = corrector.suggest(term[1], limit=1)
            if not corrected_term:
                # Handle the case when there are no suggestions
                return []
            corrected_term = corrected_term[0]
            p_query = p_query.replace("content", term[1], corrected_term)  # Replace the term with a new Term object
      
        result = searcher.search(p_query, terms = True)
        #sort result by how often the search terms are mentioned
        result = sorted(result, key=lambda x: sum(x['content'].lower().count(q) for q in querylist), reverse=True)

        for r in result:
            # Highlight search terms in bold
            highlighted_content = r.highlights("content")
    
            # Append the result with highlighted content to the output list
            out.append({
                'title': r['title'],
                'content': highlighted_content,
                'url': r['url']
            })
            

    return out

if __name__ == '__main__':

    nltk.download('stopwords')

    crawl('https://vm009.rz.uos.de/crawl/index.html')  

    query = "uncorn"

    result = search(query)