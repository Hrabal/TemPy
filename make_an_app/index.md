---
layout: default
title: Let's Build an app with TemPy
permalink: /make_an_app/
---

# Let's Build an App

In this tutorial we'll build a simple webapp using Flask, SQLAlchemy and Tempy. This tutorial is similar to many other but we'll use TemPy, instead of Jinja2 or Mako, for the templating part of our app.
This tutorial is based on the great Miguel Grinberg's [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world), if you are new to Flask and/or SQLAlchemy please read his tutorial first.

We'll cover all the steps from zero to a working Contact Book app, focusing more in the TemPy parts, If you are confident using Flask and SQLAlchemy you can skip to the [TemPy in action](tempy/) part of this tutorial.

### Check we have what we need

First we'll check everything we need to build our app, in this tutorial we'll use Python >= 3.6 and sqllite3.

Open a terminal/shell window and type the following to check if we have Python3 installed:

```shell
$ python3 --version
Python 3.7.0
```

If you get an error or the output shows a Python version lower than 3.6, please go to [python.org](https://www.python.org/) and install the latest stable Python3 version.

Same thing for Sqlite3:

```shell
$ sqlite3 --version
3.24.0 2018-06-04 14:10:15 95fbac39baaab1c3a84fdfc82ccb7f42398b2e92f18a2a57bce1d4a713cbaapl
```
If you get an error probably you don't have sqlite3 installed on you machine, to get SQLite3 follow [this](https://www.tutorialspoint.com/sqlite/sqlite_installation.htm) tutorial.

### Setup 

Now we'll start making our project, go back to the shell window and type those commands to make the project folder structure:
```shell
$ mkdir tempy_app
$ cd tempy_app
$ mkdir {static,templates}
```

Then we fire a [vitualenv](https://virtualenv.pypa.io/en/latest/) on our project's dir:
```shell
$ virtualenv -p python3.7 venv
Running virtualenv with interpreter /usr/local/bin/python3.7
Using base prefix '/Library/Frameworks/Python.framework/Versions/3.7'
New python executable in /Users/user/tempy_app/venv/bin/python3.7
Also creating executable in /Users/user/tempy_app/venv/bin/python
Installing setuptools, pip, wheel...done.

$ source venv/bin/activate
```

Now that we activated our virtualenv, we'll use the virtualen's Python interpreter, tools and plugins.
But we don't have the plugins yet, so we'll install all the Python modules that we need for this project using pip. 

First, we'll make a `requirements.txt` file with the list of the needed modules:

```shell
(venv)$ touch requirements.txt
```

Open your favourite text editor and edit the file `requirements.txt` adding those lines:

```
bcrypt==3.1.4
SQLAlchemy==1.2.13
sqlalchemy-migrate
Flask==0.12.2
Flask-Login==0.4.0
Flask-SQLAlchemy==2.2
tem-py
```

Save the file, go back to the shell and run:

```shell
(venv)$ pip install -r requirements.txt
```

`requirements.txt` contains the list of all the packages and modules that we'll be using to build the app.

Now we are ready to build a blog using TemPy, Flask and SQLAlchemy! Go to the next section: [Base Files](base_files/)
