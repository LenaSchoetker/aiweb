import re
from flask import Flask, request, render_template
from crawlerv2 import search as whoosh_search
import traceback


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
    return render_template("result.html", results=r, query=query)


@app.errorhandler(500)
def internal_error(exception):
   return "<pre>"+traceback.format_exc()+"</pre>"