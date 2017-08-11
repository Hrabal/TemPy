# -*- coding: utf-8 -*-
import json
from flask import Flask

app = Flask(__name__)

@app.route('/')
def none_handler():
    return 'Ready for some Tempy examples?'

@app.route('/hello_world')
def tempy_handler():
    from templates.hello_world import page
    return page.render()

@app.route('/star_wars')
def tempy_handler():
    from templates.star_wars import page
    with open('sw-people.json', 'r') as f:
        people = list(json.load(f).values())
    return page.render(characters=people)

if __name__ == '__main__':
    app.run(port=8888, debug=False)
