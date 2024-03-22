#!/usr/bin/python3
"""Flask Framework"""
from flask import Flask

app = Flask(__name__)
@app.route('/')
def hekki_hbnb():
    return 'Hello HBNB'
if __name__ == '__main__':
    app.run()
