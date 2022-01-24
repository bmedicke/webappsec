# Web Application Security

For my WEB (web application security) seminar paper I have decided to write a
chat-app with profile function that can be integrated in a canvas-based
multiplayer game.
Since the game is still very much work in progress I have focused on creating a
web-app with the corresponding functionality.
(See [GitHub version](https://github.com/bmedicke/MCS3_WEB_seminar_paper)
of this writeup.)

![image](https://user-images.githubusercontent.com/173962/150825414-33777ed8-46f0-4a0f-a1d4-9c1783b9b958.png)
> landing page for logged-in users

## table of contents

<!-- vim-markdown-toc GFM -->

* [TODO](#todo)
* [local development setup](#local-development-setup)
  * [starting the app](#starting-the-app)
* [used libraries](#used-libraries)
* [the chat app](#the-chat-app)
  * [database schema](#database-schema)
  * [list of `GET` endpoints](#list-of-get-endpoints)
  * [list of `POST` endpoints](#list-of-post-endpoints)
    * [list of endpoints that write to the db](#list-of-endpoints-that-write-to-the-db)
  * [structure of the app](#structure-of-the-app)
    * [dunder init](#dunder-init)
  * [statistics](#statistics)
* [things to mention](#things-to-mention)
* [resources](#resources)

<!-- vim-markdown-toc -->

# TODO

* [ ] grep for todos and fix them (`rg -i todo`)
* [ ] write tests
* [ ] deploy app with https certificate
* [ ] change docstrings to flasgger format
* [ ] switch to PostGres

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
including the bound network interface and port. By default the development server will run at: [0.0.0.0:7701](http://0.0.0.0:7701).

**Security note:** Note, that the secret, that is used for signing session cookies, defaults to `dev`
if the environment variable `SECRET_KEY` is not set. There are three ways to set this key when deploying:

* via `export SECRET_KEY=xxxx` before starting flask
* via `SECRET_KEY=xxxx` in `.env` (recommended)
* via `SECRET_KEY=xxxx` in `.flaskenv` (not recommended since this file is commited)

Both `.flaskenv` and `.env` are automatically parsed.

You can use `flask generate-secret-key` to create your own secure key. This command uses the `token_urlsafe()` function
from Python's `secret` module to generate cryptographically strong random strings (32 characters long). **This string should not be commited**!

<br>

![image](https://user-images.githubusercontent.com/173962/150771984-e03b5e90-da39-4d15-a347-a190c1ee2fec.png)
> example run of `flask generate-secret-key` (be sure to run it yourself)
<br>

---

The following docker-compose services are available:

 * **db**: Postgres
     * *security note: standard password should be changed to something secure*
     * *security note: password should be removed from docker-compose file (and it should not be commited)* 
     * since the app is currently using `sqlite` this service is not in use
 * [**adminer** (localhost:7780)](http://localhost:7780)
     * web-base database manager/GUI

## starting the app

The app uses a [SQLite](https://www.sqlite.org/index.html) (file-based) database for storing user profiles and messages.
Before starting the app the database schema has to be used to create the database:

```sh
flask init-db # apply db schema (recreates db if it exists).
sqlitebrowser instance/flask-api.sqlite # take a look at the schema.
flask run # see .flaskenv and .env for environment variables.
```

To check if configuration changes took affect you can run `flask read-config`:

<br>

![image](https://user-images.githubusercontent.com/173962/150776298-8046308a-916a-4a41-9d82-a51abcfe10d2.png)
> abbreviated output from `flask read-config`

# used libraries

* [Flask](https://flask.palletsprojects.com/)
    * relatively unopinionated Python web microframework
    * there is a default templating engine but it can be changed
    * as a microframework it aims to be simple (no ORM) but extensible
* [flask-wtf](https://flask-wtf.readthedocs.io/)
    * integration between [WTForms](https://wtforms.readthedocs.io) and Flask
    * provides CSRF (Cross-Site-Request-Forgery) protection
        * can be used without WTForms (as in this project)
* [bcrypt](https://github.com/pyca/bcrypt/)
    * password salting and hashing
        * *security note: bcrypt truncates passwords to 72 bytes*
    * no longer used for this project (switched to flask-wtf)
* [python-dotenv](https://github.com/theskumar/python-dotenv)
    * for setting environment variables in Python from dotfiles
    * can be used standalone but also acts as Flask extension when imported into a Flask app:
        * automatically parses `.env` and `.flaskenv`
* [sqlite3](https://docs.python.org/3/library/sqlite3.html)
    * SQLite is a file-based, self-contained SQL database engine
    * easy to use during prototyping
    * this is part of the Python standard library
* [click](https://click.palletsprojects.com/)
    * library for command line parsing
    * can be used standalone but also acts as Flask extension when imported into a Flask app:
    * used for extending Flask with the custom CLI commands:
        * init_db_cli
        * gen_secret_key
        * read_config
* [SQLAlchemy](https://www.sqlalchemy.org/)
    * object relational mapper
    * supports a wide range of databases
    * not yet used in `main` branch
* [psycopg\[pool,binary\]](https://www.psycopg.org/) (versions 3) and psycopg2-binary (version 2)
    * Postgres adapter (for notify/listen events)
    * not yet used in `main` branch
    * planned alternative for sqlite
* [black](https://github.com/psf/black)
    * highly opinionated Python code formatter
    * code style for this project: `black -l79 **/*.py`
        * all defaults except reduce maximum linewidth to 79
* [ptpython](https://github.com/prompt-toolkit/ptpython), [ipython](https://ironpython.net/)
    * ptpython is used for debugging:
      * for proper code completion in the breakpoints REPL
    * ptpython requires the (nonstandard) IronPython runtime
* [flasgger](https://github.com/flasgger/flasgger)
    * Flask extension that extracts [OpenAPI](https://swagger.io/specification/) specification from Flask views
    * adds an API endpoint ([/apidocs](localhost:7701/apidocs)) that serves endpoint documentation
* [Jinja2](https://www.palletsprojects.com/p/jinja/)
    * Flask's default template engine
    * similar to Django's templating syntax:
        * control structures `{% %}`
        * variable values `{{ }}`
        * comments `{# #}`
    * *supports Unicode*
    * *automatic HTML escaping*
    * *optional Sandbox to evaluete untrusted code*
* [Tailwind CSS](https://tailwindcss.com/)
    * Tailwind provides utility-class based styling

---

other interesting libraries to consider:

* [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) SQLAlchemy extension for Flask
* [flask-login](https://flask-login.readthedocs.io/en/latest/) for session handling

# the chat app

The following sections cover a specific aspect of the chat app each:

## database schema

The old schema was based on a private messaging function. It also stored salt and password in seperate fields.

![image](https://user-images.githubusercontent.com/173962/145773177-4b7a9803-14c7-43c1-ad70-7c5093fe7a5c.png)
> old schema (PostGres)

I've since changed my mind and switched to an exclusively, global chat
(planned to be a proximity-based chat in the game)

![image](https://user-images.githubusercontent.com/173962/150687869-9d1d31de-7728-43e8-ba88-9b2e3a3328ab.png)
> current schema (SQLite)

<br>

relevant sections from `schema.sql`:

```sql
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  avatar TEXT NOT NULL DEFAULT '0000',
  about TEXT DEFAULT '',
  private INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE message (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  text TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

```

Note the following:

* the `id` fields are auto-incrementing primary keys of type `INTEGER`
* the `message` table has an `author_id` field that is a foreign key pointing to the `id` field of the `user` table
    * each message is owned by a user (the author)
* `created` is a timestamp that is populated by sqlite itself via `CURRENT_TIMESTAMP`
* `text` is of type `TEXT` and may not be null, empty messages don't make much sense
* `username` and `password` are of type text as well and can not be null
  * `username` is `UNIQUE`
  * **potentially dangerous bug**: `password` was unique for some time as well
      * This kind of bug might have been exploited by an attacker by creating accounts with
      common passwords (and unlikely usernames) and checking if a server error occurs. On a server error
      the attacker could have tried known usernames (from the chat) with the
      identified passwords.
      * Not in this instance though, since the stored passwords are hashed with
      a salt. (The `password` field actually stores 3 things: the algorithm, the hashed password and the salt itself)
* the `user` table has a field named `private` that stores wheter the user profile should be hidden
  * since sqlite does not have a Boolean type this is stored as `INTEGER` and cast to `bool` before usage
  * for **privacy reasons** this **defaults to `True`** when creating a new user
  * a user public profile shows: their profile picture, the customizable about text and their username
  * a private user profile only shows: `private user`
  * a non existing user profile also shows: `private user` to **avoid user enumeration** (auto-incrementing user ids would make this task trivial otherwise)
  * users have the option to set this option to `False` in their profile
* `avatar` stores an image id (from a list of options) and not the path to an image or the image itself
* **TODO**: add `coordinates` field to both the `message` and `user` table for proximity-based chatting

<br>

![image](https://user-images.githubusercontent.com/173962/150795487-49f185aa-9e26-45ed-ad4c-307858765e6d.png)
> user table via `sqlitebrowser`: showing the `id`, `username`, and `password` fields

<br>

---

The following is a short overview of available endpoints and a manual analysis
of endpoints (specifically methods) that have the potential to change data:

## list of `GET` endpoints

Grep sourcecode for `.route`:

* [/](http://localhost:7701/)
  * the landing page and main chat interface
* [/user/\<int:user_id\>](http://localhost:7701/user/0)
  * user profile pages
* [/auth/register](http://localhost:7701/auth/register)
  * form to create a new account
* [/auth/login](http://localhost:7701/auth/login)
  * form to login
* [/auth/logout](http://localhost:7701/auth/logout)
  * endpoint to logout
* [/profile](http://localhost:7701/profile)
  * displays own user profile (different from `/user/`)
* [/profile/edit](http://localhost:7701/profile/edit)
  * edit user profile of logged-in user
* ~~[/create](http://localhost:7701/create)~~
  * form to send a message
  * functionality integrated into the `/` endpoint
    * avoids duplication of code and improves maintainability

## list of `POST` endpoints

Grep for `.methods`:

* `/`
  * post a message from `/` by pressing enter from the chat bar
* `/delete/<int:message_id>`
  * deletes a message (if logged-in user is the author)
  * send POST-request from `/` by clicking red cross
* `/profile/edit`
  * POST-request from same endpoint
* `/auth/register`
  * POST-request via form on same endpoint
* `/auth/login`
  * POST-request via form on same endpoint

### list of endpoints that write to the db

Grep for `.commit`:

* `/` (via `message_post()`), POST
* `/profile/edit`, POST
* `/register`, POST
* `/delete/<int:message_id>`, POST

Cross reference of endpoints with functions that can change the database:

**All endpoints that have the ability to change the database are POST**.
(As far as I know only `POST` and `GET` methods are allowed in forms,
so I am limited to these for now, even if it is not quite conform with REST)

---

Other things to note when creating endpoints:

*Security note:* When creating an endpoint that extracts a variable
from the url that is later used it has to be properly escaped!

Compare the following two Flask routes (inspired by a bug):

```python
@app.route("/i/<unescaped>")
def injection(unescaped):
    """
    injection demo route

    localhost:7701/i/<body onload='alert("this is bad");'>
    """
    return f"{unescaped}"

@app.route("/e/<escaped>")
def no_injection(escaped):
    """
    injection-safe demo route

    localhost:7701/e/<body onload='alert("this is bad");'>
    """
    return f"{escape(escaped)}"
```

<br>

![image](https://user-images.githubusercontent.com/173962/150808281-7de2dcef-07e6-4c2f-8292-b6751c91d16b.png)
> route with proper escaping of user input

<br>

![image](https://user-images.githubusercontent.com/173962/150808466-9e7c93eb-5538-4560-b070-c0e3508481f3.png)
> route without proper input sanitization allows for JavaScript injection attacks

<br>

---

It is also possible to restrict the variable part of a route to a datatype,
which can mitigate this kind of attack as well. See the `/user` route from
[profile.py](https://github.com/bmedicke/MCS3_WEB_seminar_paper/blob/main/flask_api/profile.py#L97-L114) for an example:

```python
@blueprint.route("/user/<int:id>")
def user(id):
    """
    shows profile of user by id (if set to public)

    returns html
    """
    db = get_db()
    user = db.execute(
        """
        SELECT username, private, avatar, about
        FROM user
        WHERE id = ?
        """,
        (escape(id),),
    ).fetchone()

    return render_template("/profile/user.html", user=user)
```

Note the following:

* the user route will only trigger for integers in the variable part of the URL: `<int:id>`
* I have chosen to `escape()` the input nontheless in case the endpoint is
  edited in the future (or if there's a bug in the endpoint handling)
* SQL queries in this app use parameterized statements (the sqlite3 library does not support prepared statements)

## structure of the app

The following ASCII diagram shows the project structure:

```sh
├── docker
│   ├── ...
├── docker-compose.yml
├── env
│   ├── ...
├── flask_api
│   ├── auth.py
│   ├── database.py
│   ├── __init__.py
│   ├── message.py
│   ├── profile.py
│   ├── schema.sql
│   ├── static
│   │   ├── favicon.png
│   │   ├── profiles
│   │   │   ├── 0000.png
│   │   │   ├── 0001.png
│   │   │   ├── ...
│   │   └── style.css
│   └── templates
│       ├── auth
│       │   ├── login.html
│       │   └── register.html
│       ├── base.html
│       ├── index.html
│       ├── message
│       │   └── create.html
│       └── profile
│           ├── edit.html
│           ├── show.html
│           └── user.html
├── instance
│   └── flask-api.sqlite
├── readme.md
├── requirements.txt
├── .gitignore
├── .env
└── .flaskenv
```

* `docker` and `docker-compose.yml` are used for storing docker data (postgres) and the service file respectively
* `env` is the virtual environment that is used to store installed libraries (instead of the global store)
* `__init__.py` is the starting point of the Flask app and marks the encompassing folder as a Python module
  * this file imports the other scripts
* `schema.sql` is used by `flask init-db` to setup the database (see [database schema](#database-schema))
* `static` files are served directly
* `templates` contains the served HTML/Jinja2 templates, `base.html` is inherited from by the other templates
* `instance` is created by `flask init-db` and contains the sqlite database (`flask-api.sqlite`)
* `.env` and `.flaskenv` are parsed by the app and used for environment variables

<br>

* *security note: the `.flaskenv` file should not be commited if there are
any secrets stored in it*
    * you sould use the `.env` file for secrets (which is in `.gitignore`)
* *security note: when returning HTML (the default) user provided values
must be `escape()`d to prevent injections*
    * unsafe: `http://localhost:7701/i/<body onload='alert("this is bad");'>`
    * safe: `http://localhost:7701/u/<body onload='alert("this is bad");'>`
    * Jinja templates do this automatically (but you can explicitly disable this behaviour)

### dunder init

Abbreviated `__init__.py`, the starting point of the app:
```sh
from dotenv import load_dotenv  # automatically load .flaskenv
from flask import Flask
from flasgger import Swagger
from flask_wtf.csrf import CSRFProtect
import os

def create_app(test_config=None):
    """
    application factory function for the Flask app.

    returns a Flask object
    """

    # read secret key from env vars when deploying,
    # used for signing session cookies:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")

    # name app after module name:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        DATABASE=os.path.join(app.instance_path, "flask-api.sqlite"),
    )

    # ...

    # views for routes are imported via blueprints:
    from . import auth
    from . import database
    from . import message
    from . import profile

    # register database functions with the app (includes cli command):
    database.init_app(app)

    # register authentication blueprint (register/login/logout):
    app.register_blueprint(auth.blueprint)

    # ...

    # require valid CSRF token for modifying requests:
    csrf = CSRFProtect()
    csrf.init_app(app)

    # generate apidocs:
    Swagger(app)

    return app
```

`__init__.py` defines a single function that in turn creates the Flask
app (factory pattern). If no `SECRET_KEY` environment variable is it
defaults to `dev`. After the configuration is done, the blueprints for
endpoints are imported and registered with the app.

`CSRFProtect` is imported from the `flask_wtf` library (which is
only used for the CSRF protection).
Calling `csrf.init_app(app)` enables CSRF protection globally
(for `POST` requests) by registering the Flask extension.

Since I use my own forms (as opposed to WTForms) a hidden `csrf_token`
has to be added to each form. The value of the token can be be used
in Jinja with `{{ csrf_token }}`, `flask_wtf` populates this variable automatically.

When receiving a form this value is expected, otherwise the request will
not be performed.

As an example here is part of the `index.html`:

```html
<!-- ... -->

<form method="post" accept-charset="utf-8">
    <input type="text" name="text"
        id="text" value="" placeholder="{{ "write your message here"
                           if g.user else "log in to start chatting" }}"
        class="chatbar w-full pl-2 mt-2 font-mono
                    {{ "bg-gray-50" if not g.user else "bg-sky-50" }}"
        required {{ "disabled" if not g.user }}>
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
</form>

<!-- ... -->
```

Populated `csrf_token` variable in a browser:

![image](https://user-images.githubusercontent.com/173962/150823071-697ef323-a8ae-4f40-97d8-5557461e6a0a.png)
> the same form rendered in a browser

And here a screenshot when creating a request without that token:

![image](https://user-images.githubusercontent.com/173962/150823470-fac397b5-4f53-43a3-bc20-f4e4656b1964.png)
> missing CSRF token

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

* thread local objects (for thread safety) and notes about security
    * flask protects against XSS. (via flask itself and jinja2)
        * https://flask.palletsprojects.com/en/1.0.x/advanced_foreword/
* **security note**: use type hinting
* try injections: https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/SQLite%20Injection.md

---

* start out with `sqlite`, maybe switch to postgres later
    * sqlite is purely concurrent and might be too slow for larger apps
* the `flask-api` directory contains a python package (`__init__.py`) for the app with the application factory (`create_app()`)



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

