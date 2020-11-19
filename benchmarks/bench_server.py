# -*- coding: utf-8 -*-
import json
from flask import Flask, render_template

from tempy_templates.hello_world import page as hw_page
from tempy_templates.sw_multifile import page as sw_multi_page
from tempy_templates.sw_monofile import page as sw_mono_page
# from tempy_templates.sw_multifile_table import page as sw_multi_page_table

app = Flask(__name__)
with open('sw-people.json', 'r') as f:
    people = json.load(f)


@app.route('/j2_sw_multifile_table')
def j2_sw_multifile_table():
    return render_template('sw_characters_table.html', people=people)


def tempy_sw():
    from tempy_templates.sw_monofile import page
    return page.render(characters=people.values())


@app.route('/j2_sw_monofile')
def j2_sw():
    return render_template('j2_sw_monofile.html', people=people)


@app.route('/tempy_sw_mono')
def tempy_sw_monofile():
    return sw_mono_page.render(characters=people.values())


@app.route('/tempy_sw_multifile')
def tempy_sw_multifile():
    return sw_multi_page.render(characters=people.values(), pretty=True)


@app.route('/j2_sw_multifile')
def j2_sw_multifile():
    return render_template('sw_characters.html', people=people)


@app.route('/tempy_hw')
def tempy_hw():
    return hw_page.render()


@app.route('/j2_hw')
def j2_hw():
    return render_template('hello_world.html')


if __name__ == '__main__':
    app.run(port=8888, debug=False)
