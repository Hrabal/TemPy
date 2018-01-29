# -*- coding: utf-8 -*-
import json
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def none_handler():
    return 'Ready for some Tempy examples?'

@app.route('/hello_world')
def hello_world_handler():
    from templates.hello_world import page
    return page.render()

@app.route('/star_wars')
def star_wars_handler():
    from templates.star_wars import page
    json_filename = os.path.join(app.static_folder, 'sw-people.json')
    with open(json_filename, 'r') as f:
        people = json.load(f)['characters']
    return page.render(characters=people)

@app.route('/list')
def render_list_handler():
    from templates.render_list import page
    return page.render()

@app.route('/static')
def static_files_handler():
    from templates.static_files import page
    return page.render()

if __name__ == '__main__':
    app.run(port=8888, debug=True)
