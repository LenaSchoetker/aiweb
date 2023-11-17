from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from flask import Flask, request


app = Flask(__name__)

# Load the Whoosh index
ix = open_dir("indexdir")

@app.route("/")
def start():
    return "<form action='search' method='get'><input type='text' name='q'><input type='submit' value='Search'></form>"

@app.route("/search")
def search():
    # Get the search query parameter 'q' from the URL
    search_query = request.args.get('q')

    # Initialize an empty list to store the results
    results_list = []

    # Retrieving data
    with ix.searcher() as searcher:
        # find entries with the words 
        query = QueryParser("content", ix.schema).parse(search_query)
        print("no", query)
        results = searcher.search(query)
        print("yes", results)

        # Build a list of dictionaries containing relevant information
        for r in results:
            result_dict = {'title': r['title'], 'url': r['url']}
            print("yes", result_dict)
            results_list.append(result_dict)
    
    for r in results_list:
        print(f"Title: {r['title']} - URL: {r['url']}")
    if results_list == []:
        return "<h1>No results found</h1>"
    
    # Generate HTML content with clickable links
    html_content = "<h1>Search Results</h1>"
    html_content += "<ul>"
    for result in results_list:
        html_content += f"<li><strong>Title:</strong> {result['title']}<br><strong>URL:</strong> <a href='{result['url']}'>{result['url']}</a></li>"
    html_content += "</ul>"

    # Return the HTML content as a response
    return html_content

