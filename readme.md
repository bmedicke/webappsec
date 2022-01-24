# Web Application Security

For my WEB (web application security) seminar paper I have decided to write a chat-app with profile function that can be integrated in a canvas-based multiplayer game.
Since the game is still very much work in progress I have focused on creating a web-app with the corresponding functionality.

> ![image](https://user-images.githubusercontent.com/173962/150765330-c4e8e70e-8386-4379-a71a-0ec44c814a83.png)
> 
> landing page for logged-in users

## table of contents

<!-- vim-markdown-toc GFM -->

* [TODO](#todo)
* [local development setup](#local-development-setup)
  * [Flask app](#flask-app)
* [used libraries](#used-libraries)
* [the chat app](#the-chat-app)
  * [list of post endpoints](#list-of-post-endpoints)
    * [list of endpoints that write to the db](#list-of-endpoints-that-write-to-the-db)
  * [structure of the app**](#structure-of-the-app)
  * [database schema](#database-schema)
  * [statistics](#statistics)
* [things to mention](#things-to-mention)
* [resources](#resources)

<!-- vim-markdown-toc -->

# TODO

* [x] grep for todos and fix them (`rg -i todo`)
* [ ] write tests
* [ ] deploy app with https

# local development setup

The app is based on [Flask](https://flask.palletsprojects.com/), a Python micro web framework.
To get it running in development mode execute the following steps that will install all 
required dependencies. For a detailed breakdown of used libraries see the section:
[used libraries](#used-libraries).

```sh
git clone 'git@github.com:bmedicke/MCS3_WEB_seminar_paper.git' # clone repo.
cd MCS3_WEB_seminar_paper # switch to it.

python3 -m venv env # create virtual environment.
source env/bin/activate # activate virtual environment.

pip install -r requirements.txt # install dependencies.

# optional:
docker-compose up -d # start docker-compose services in background.
```
See [.flaskenv](https://github.com/bmedicke/MCS3_WEB_seminar_paper/blob/main/.flaskenv) for configuration options
including the bound network interface and port as well as the secret that is used for signing session cookies.
By default the development server will run at: [0.0.0.0:7701](http://0.0.0.0:7701).

---

The following docker-compose services are available:

 * **db**: Postgres
     * *security note: standard password should be changed to something secure*
     * *security note: password should be removed from docker-compose file (and it should not be commited)* 
     * since the app is currently using `sqlite` this service is not in use
 * [**adminer** (localhost:7780)](http://localhost:7780)
     * web-base database manager/GUI

## Flask app

```sh
flask init-db # apply db schema.
sqlitebrowser instance/flask-api.sqlite
flask run # see .flaskenv for envvars.
```

# used libraries

* tailwind
    * utility-class based styling
* flask, fastapi, connexion
    * the libraries to compare
* flask-wtf
    * flask wtforms integration (with csrf protection)
    * https://testdriven.io/blog/csrf-flask/#how-to-prevent-csrf
* python-dotenv
    * for setting environment variables from `.env` files
* sqlalchemy
    * object relational mapper
* psycopg[pool,binary] (versions 3) and psycopg2-binary (version 2)
    * Postres adapter (for notify/listen evens)
* black
    * code formatter
    * `black -l79 **/*.py`
* ptpython, ipython
    * for proper code completion in breakpoints/repl
* bcrypt
    * salt and hashing
        * *security note: bcrypt truncates passwords to 72 bytes*
* click
    * command line parsing

---

other interesting libs to consider:

* https://github.com/flasgger/flasgger
* https://flask-sqlalchemy.palletsprojects.com/
* flask-login (session handling)

# the chat app

## list of post endpoints

grep for `.methods`

* /
* /create
* /profile/edit
* /register
* /login
* /delete/<int:id>

### list of endpoints that write to the db

grep for `.commit`

* / (via `message_post`)
* /create (via `message_post`)
* /profile/edit
* /register
* /delete/<int:id>

## structure of the app**

```sh
(env) root::kali:flask_api:# tree                                                   0 [main]
.
├── auth.py
├── database.py
├── __init__.py
├── message.py
├── old_endpoints.py
├── profile.py
├── schema.sql
├── static
│   ├── profiles
│   │   ├── 0000.png
│   │   ├── 0001.png
│   │   ├── 0002.png
│   │   ├── 0003.png
│   │   ├── 0004.png
│   │   └── 0005.png
│   └── style.css
└── templates
    ├── auth
    │   ├── login.html
    │   └── register.html
    ├── base.html
    ├── index.html
    ├── message
    │   └── create.html
    └── profile
        ├── edit.html
        ├── show.html
        └── user.html
```

## database schema

![image](https://user-images.githubusercontent.com/173962/150687869-9d1d31de-7728-43e8-ba88-9b2e3a3328ab.png)

![image](https://user-images.githubusercontent.com/173962/145773177-4b7a9803-14c7-43c1-ad70-7c5093fe7a5c.png)

* [flask (localhost:7701)](http://localhost:7701)
* *security note: the `.flaskenv` file should not be commited if there are
any secrets stored in it*
    * you could use the `.env` file for secrets
* *security note: when returning HTML (the default) user provided values
must be `escape()`d to prevent injections*
    * unsafe: `http://localhost:7701/i/<body onload='alert("this is bad");'>`
    * safe: `http://localhost:7701/u/<body onload='alert("this is bad");'>`
    * Jinja templates do this automatically
* thread local objects (for thread safety) and notes about security
    * flask protects against XSS. (via flask itself and jinja2)
        * https://flask.palletsprojects.com/en/1.0.x/advanced_foreword/
* **security note**: use type hinting
* try injections: https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/SQLite%20Injection.md

---

* start out with `sqlite`, maybe switch to postgres later
    * sqlite is purely concurrent and might be too slow for larger apps
* the `flask-api` directory contains a python package (`__init__.py`) for the app with the application factory (`create_app()`)

## statistics

```sh
root::kali:flask_api:# cloc *.py **/*.html
      14 text files.
      14 unique files.
       0 files ignored.

github.com/AlDanial/cloc v 1.90  T=0.01 s (977.1 files/s, 60231.7 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Python                           6            123            156            286
HTML                             8             54              0            244
-------------------------------------------------------------------------------
SUM:                            14            177            156            530
-------------------------------------------------------------------------------

```

# things to mention

* [ ] werkzeug only in development, not production (https://werkzeug.palletsprojects.com/en/2.0.x/serving/)
    * https://flask.palletsprojects.com/en/2.0.x/tutorial/deploy/
* [ ] application factory
* [ ] `app.config` options
    * [ ] `SECRET_KEY` https://flask.palletsprojects.com/en/2.0.x/config/#SECRET_KEY
        * set via env vars or `config.py`
        * used for signing session cookies
    * [ ] `PERMANENT_SESSION_LIFETIME` 31 days
    * [ ] `SESSION_COOKIE_SECURE` and `SESSION_COOKIE_SAMESITE` False?
    * [ ] `WTF_*`

```python
 {
     'WTF_CSRF_ENABLED': True,
     'WTF_CSRF_CHECK_DEFAULT': True,
     'WTF_CSRF_METHODS': {'POST', 'DELETE', 'PATCH', 'PUT'},
     'WTF_CSRF_FIELD_NAME': 'csrf_token',
     'WTF_CSRF_HEADERS': ['X-CSRFToken', 'X-CSRF-Token'],
     'WTF_CSRF_TIME_LIMIT': 3600,
     'WTF_CSRF_SSL_STRICT': True
 }
```

* [ ] debug mode (werkzeug), production mode (proper wsgi server)
* [ ] sqlite is slow because writes happen concurrently
* [ ] connections are tied to the request (closed before sending it)
* [ ] `g` is a global (to the request) object, stores state during request only
* [ ] `@login_required` decorator
* [ ] blueprints and views (https://flask.palletsprojects.com/en/2.0.x/tutorial/views/)
* [ ] `from werkzeug.security import check_password_hash, generate_password_hash`
    * https://werkzeug.palletsprojects.com/en/2.0.x/utils/#werkzeug.security.generate_password_hash
    * uses `pbkdf2:sha256` (https://en.wikipedia.org/wiki/PBKDF2)
    * uses salt length of `16`
* [ ] `GET` requests should not change the database
* [ ] `old_endpoints.py` (user profiles escaped?)
* [ ] CSRF tokens (`__init__.py` and `.html`s)
* [ ] `/user/<int:id>` endpoint (with backup `escape()`)
* [ ] git hooks, github webhooks
* [ ] linten (black, pyflakes) & static analysis
* [ ] commits durchgehen, etwicklung der app
* [ ] https://dependencytrack.org/
* [ ] semgrep
* [ ] dotenv
* [ ] gitignore
* [ ] externalized configuration
* [ ] [SAST](https://owasp.org/www-community/Source_Code_Analysis_Tools)
    * https://cheatsheetseries.owasp.org/IndexTopTen.html
* [ ] escaping/quoting
* [ ] http header
* [ ] `npm audit` for python
* [ ] set secure-ish session cookie flags
* [ ] `ripgrep`
* [ ] kein npm-audit für python github dependabot
* [ ] jinja2 template
* [ ] check OWASP top 10
* [ ] check if libs are outdated (vuln scanner?)
* [ ] check out https://pythonhosted.org/Flask-Security/
* [ ] check out https://github.com/FHPythonUtils/PyTaintX
* [ ] session lifetime?
* [ ] mention JWT?
* [ ] two-factor login?
* [ ] write some tests

# resources

* https://github.blog/2021-12-06-write-more-secure-code-owasp-top-10-proactive-controls/

