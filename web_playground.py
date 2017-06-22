# -*- coding: utf-8 -*-
import os
import json
import cProfile, pstats, io
from pprint import pprint
from flask import Flask, render_template
from playground_templates.sw import page


app = Flask(__name__)

with open('sw-people.json', 'r') as f:
    people = json.load(f)

@app.route('/tempy')
def tempy_handler():
    # pr = cProfile.Profile()
    # pr.enable()
    page.body.inject(charachters = people.values())
    rend = page.render()
    # pr.disable()
    # s = io.StringIO()
    # sortby = 'cumulative'
    # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    # ps.print_stats()
    # print(s.getvalue())
    return rend

@app.route('/j2')
def j2_handler():
    return render_template('characters.html', people=people)

if __name__ == '__main__':
    app.run(port=8888, debug=False)
