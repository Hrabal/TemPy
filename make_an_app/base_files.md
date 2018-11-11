---
layout: default
title: The base files
permalink: /make_an_app/base_files/
---

# Let's Build an App

### Base files

Now we'll make the base code to make our Flask app working. We start by making an `app.py` file that will contain the Flask initialization:

```python
# app.py

import locale
from flask import Flask
import logging

locale.setlocale(locale.LC_TIME, locale.getlocale())
logging.basicConfig()

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def index():
    return "Hello World"
```

In this file we setup the basic logging utilities and we set some locale config for datetime.
The important part here is the declaration of the `app` variable which is an instance of Flask, this will manage all our web requests. With the `app.config.from_object('config')` instruction we tell Flask to load oll the configurations of our app from a config file, so now we need to make the `config.py` file:

```python
# config.py

SECRET_KEY = 'very secret string!'
```
This file is small right now, we'll add some more lines as we'll add a database access to our app.

The only missing thing in order to run our raw webapp is way to start it, so we make a `run.py` file with the only those two lines of code:

```python
# run.py

from app import app
app.run(debug=True)
```

Now we are ready to test if everything is working, go to the shell and run our last created file:

```shell
(venv)$ python run.py
WARNING:werkzeug: * Debugger is active!
```

Now our app is up and running, and we should be able to get the Hello World message in the browser hitting the [`http://127.0.0.1:5000/`](http://127.0.0.1:5000/){:target="_blank"} address.


get back to the terminal and hit `control + c` to stop the wesberver.
---

### Project structure

Now that we made our Flask app running, let's make it a little more organized so we'll have organiside code.
At this point our folder structure should be this:

```
tempy_app\
    venv\
    static\
    templates\
    requirements.txt
    app.py      
    run.py 
    config.py     
```

We'll add one empty file that will contain or database models:
```shell
(venv)$ touch models.py
```

and we move the controllers code to a new file. First create the `controllers.py` file and add the controller code from `app.py`:

```python
from app import app


@app.route('/')
def index():
    return "Hello World"
```

..and replace the controller code in `app.py` with an import of this new files, `app.py` will now look like this:

```python
# app.py

import locale
from flask import Flask
import logging

locale.setlocale(locale.LC_TIME, locale.getlocale())
logging.basicConfig()

app = Flask(__name__)
app.config.from_object('config')

import models
import controllers
```

Now that we have the basic app structure we need to add a database to our app in the [next section](../database/).
