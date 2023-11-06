# myapp.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from flask import Flask, request, render_template 
#from crawler_whoosh import crawl



app = Flask(__name__)

# Load the Whoosh index
ix = open_dir("indexdir")

@app.route("/")
def start():
    return "<form action='search' method='get'><input type='text' name='q'><input type='submit' value='Search'></form>"

@app.route("/search")
def search():
    """    # Get the search query parameter 'q' from the URL
    search_query = request.args.get('q')

    # Create a search query parser
    query_parser = QueryParser("content", ix.schema)

    # Parse the search query
    query = query_parser.parse(search_query)

    # Search the index and get the results
    with ix.searcher() as searcher:
        results = searcher.search(query)

    # Return the search results as an HTML page
    return render_template('search_results.html', results=results)"""
    
    # Get the search query parameter 'q' from the URL
    search_query = request.args.get('q')

    # Create a search query parser
    query_parser = QueryParser("content", ix.schema)

    # Parse the search query
    query = query_parser.parse(search_query)
    
    # Initialize an empty list to store the results
    results = []

    # Search the index and get the results
    with ix.searcher() as searcher:
        results = list(searcher.search(query))  # Store results in the list # Store results in a list

    # Return the search results as a plain text response
    result_text = "\n".join([f"{result['title']} - {result['url']}" for result in results])
    return f"Search Results:\n{result_text}"


