from flask import Flask, request, render_template
from crawlerv2 import search as whoosh_search
import traceback


app = Flask(__name__) 

@app.route('/')
def start():
    """ start page of the search engine"""

    return render_template("start.html")

@app.route('/search')
def search():
    """ search for the query in the index and return the urls where the query was found"""

    query = request.args['q'] #get the query from the url

    r  = whoosh_search(query) #search for the query in the index using the whoosh_search function from crawlerv2.py

    if r == []:
        #if no results were found, return the error page
        return render_template("error.html")
    
    #else return the result page
    return render_template("result.html", results=r, query=query)


@app.errorhandler(500)
def internal_error(exception):
   """ handler for HTTP status code 500, which corresponds to Internal Server Error"""
   
   return "<pre>"+traceback.format_exc()+"</pre>"