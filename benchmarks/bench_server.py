# -*- coding: utf-8 -*-
import json
from flask import Flask, render_template
from playground_templates.sw import page


app = Flask(__name__)

with open('sw-people.json', 'r') as f:
    people = json.load(f)

@app.route('/tempy')
def tempy_handler():
    return page.render(characters=people.values())

@app.route('/j2')
def j2_handler():
    return render_template('characters.html', people=people)

if __name__ == '__main__':
    app.run(port=8888, debug=False)
