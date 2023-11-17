import re
from flask import Flask, request, render_template
from crawler_v2 import search as whoosh_search

app = Flask(__name__)

@app.route('/')
def start():
    return render_template("start.html")

@app.route('/search')
def search():

    query = request.args['q']

    r  = whoosh_search(query)

    if r == []:
        return """<h1>Nothing fitting to be found :( </h1> <br>
                  <button><a href="/">Search again</a></button> <br>
                  <img src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/9022043e-4c38-44fb-92e2-dfa725b9ea1e/d4mxkol-2485fccf-1200-4672-b0c7-0a1615e92c27.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwic3ViIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsImF1ZCI6WyJ1cm46c2VydmljZTpmaWxlLmRvd25sb2FkIl0sIm9iaiI6W1t7InBhdGgiOiIvZi85MDIyMDQzZS00YzM4LTQ0ZmItOTJlMi1kZmE3MjViOWVhMWUvZDRteGtvbC0yNDg1ZmNjZi0xMjAwLTQ2NzItYjBjNy0wYTE2MTVlOTJjMjcucG5nIn1dXX0.m89VQ7ZtDQU6AgaeDgR42xnResZtlu8DkfPMWkcvOYY" 
                  alt="Sad platypus"> 
                  
            """
    
    return render_template("result.html", results=r, query=query)

