---
layout: default
title: The database
permalink: /make_an_app/database/
---

# Let's Build an App

### Database

Now it's time to add a database to project that will store contacts. First we need to add some db configurations in our `config.py` file, change the file with this content:

```python
# config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'very secret string!'

db_name = basedir.split('/')[-1] + '.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, db_name)
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SQLALCHEMY_TRACK_MODIFICATIONS = False
```


We have added some constats that SQLAlchemy will use to manage our db, but we have no db yet so we add it to our `app.py`. We need to change the app.py file like this:

```python
# app.py

import locale
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

locale.setlocale(locale.LC_TIME, locale.getlocale())
logging.basicConfig()

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

import models
import controllers
```

We added the SQLAlchemy import and the db variable instantiation. Now SQLAlchemy can do a lot of work for us and so we don't have to write SQL queries, and it will also do the database creation an update for us.
Now, following the [database part](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database) of the Miguel Grinberg's Flask Mega-Tutorial we'll make some utility scripts that will manage the db for us.
Make the files `db_create.py`, `db_update.py`, `db_migrate.py` and  `db_downgrade.py` with those contents:

```python
# db_create.py

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path
db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

```

```python
# db_update.py

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('Current database version: ' + str(v))

```

```python
# db_migrate.py

import imp
from migrate.versioning import api
from app import db
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
tmp_module = imp.new_module('old_model')
old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
exec(old_model, tmp_module.__dict__)
script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('New migration saved as ' + migration)
print('Current database version: ' + str(v))
```

```python
# db_downgrade.py

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('Current database version: ' + str(v))
```

If you want to understand what's happening in those files please refer to [Miguel Grinberg's Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database). Those are scripts that we'll use to create and update the database everytime we change our databse models or structure, let's try the db creation script:

```shell
(venv)$ python db_create.py
```

We now have a new folder and a new file in our folder:
 * db_repository is a folder that contains some internal SQLAlchemy infos
 * tempy_app.db is our database


Now we are ready to make some models to use in our app in the [next section](../models/).
