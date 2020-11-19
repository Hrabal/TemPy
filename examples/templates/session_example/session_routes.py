from flask import request, redirect, url_for, session

super_secret_token = 'admin_token'


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
    login_credentials = {'username' : 'admin', 'password' : 'admin'}

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
