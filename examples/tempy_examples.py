# -*- coding: utf-8 -*-
import json
import os
from flask import Flask, request, redirect, url_for, session

app = Flask(__name__)

# In an actual project, this secret key would be hidden.
# It is mostly used so we can create an example login session.
app.secret_key = '&Gp07(pz#oIA]jQ'
super_secret_token = 'admin_token'


@app.route('/')
def none_handler():
    from templates.homepage import page
    return page.render() 


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


@app.route('/user_login')
def login_handler():
    from templates.session_example.login_page import get_page

    if session.get('messages'):
        page = get_page(messages=session.pop('messages'))
    elif session.get('token') == super_secret_token: 
        return redirect(url_for('user_page_handler'))
    else: 
        page = get_page()
    return page.render()


@app.route('/user_logout', methods=['POST'])
def logout_handler():
    if session.get('token'):
        session.pop('token')
    session['messages'] = ['Successfuly logged out!']
    return redirect(url_for('login_handler'))


@app.route('/user_page', methods=['GET', 'POST'])
def user_page_handler():
    from templates.session_example.user_page import page
    data = dict(request.form)

    # In an actual project, you will probably want to use a db :)
    login_credentials = {'username': 'admin', 'password': 'admin'}

    if session.get('token') == super_secret_token: 
        success = True
    elif not data: 
        session['messages'] = ['You must login first. ']
        success = False
    elif data['username'] != login_credentials['username'] or data['password'] != login_credentials['password']:
        session['messages'] = ['Invalid credentials. ']
        success = False
    else:
        session['token'] = 'admin_token'
        success = True

    if not success: 
        return redirect(url_for('login_handler'))

    return page.render()


@app.route('/video_tag')
def video_tag_handler():
    from templates.video_tag import page
    return page.render()


@app.route('/form')
def form_handler():
    from templates.form_components import page
    return page.render()


@app.route('/homepage')
def homepage_handler():
    from templates.homepage import page
    return page.render()


if __name__ == '__main__':
    app.run(port=8888, debug=True)
