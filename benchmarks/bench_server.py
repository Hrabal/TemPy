# -*- coding: utf-8 -*-
import json
from flask import Flask, render_template

app = Flask(__name__)

with open('sw-people.json', 'r') as f:
    people = json.load(f)

@app.route('/tempy_sw')
def tempy_sw():
    from tempy_templates.sw import page
    return page.render(characters=people.values())

@app.route('/j2_sw')
def j2_sw():
    return render_template('hello_World.html', )

@app.route('/tempy_hw')
def tempy_hw():
    from tempy_templates.hello_world import page
    return page.render()

@app.route('/j2_hw')
def j2_hw():
    return render_template('sw_characters.html', people=people)

if __name__ == '__main__':
    app.run(port=8888, debug=False)
