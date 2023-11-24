import re
from flask import Flask, request, render_template
from crawlerv2 import search as whoosh_search

#TODO: nicer way to show content of results
#TODO: Improve the index by adding information?

app = Flask(__name__)

@app.route('/')
def start():
    return render_template("start.html")

@app.route('/search')
def search():

    query = request.args['q']

    r  = whoosh_search(query)

    if r == []:
        return render_template("error.html")
            #TODO: download image instead of including link
    return render_template("result.html", results=r, query=query)

