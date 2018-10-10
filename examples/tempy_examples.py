# -*- coding: utf-8 -*-
import json
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def none_handler():
    return """Ready for some Tempy examples?
   </br>
   <ul>
    <li><a href="/hello_world">Hello World</a></li>
    <li><a href="/star_wars">Star Wars</a></li>
    <li><a href="/list">List</a></li>
    <li><a href="/static">Static Image</a></li>
    <li><a href="/table">Table</a></li>
    <li><a href="/css">CSS</a></li>
    </ul>
    """

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

@app.route('/table')
def table_handler():
    from templates.table_example import page
    return page.render()

@app.route('/css')
def css_handler():
    from templates.css_example import page
    return page.render()


if __name__ == '__main__':
    app.run(port=8888, debug=True)
