# Web Application Security

> Exploits are the closest thing to “magic spells”
> we experience in the real world:<br>
> Construct the right incantation,
> gain remote control over device.
>
> @halvarflake

---

## toc

<!-- vim-markdown-toc GFM -->

* [TODO](#todo)
* [local setup](#local-setup)
* [Flask](#flask)
* [resources](#resources)
* [FastAPI](#fastapi)
* [Connexion](#connexion)

<!-- vim-markdown-toc -->

# TODO

* user registration
* authentication
* JWT
* two-factor login

# local setup

```sh
python3 -m venv env && source env/bin/activate
pip install -r requirements.txt

docker-compose up -d # start db and adminer.
```

* docker-compose services
    * **db**: Postgres
        * *security note: standard password should be changed to something secure*
        * *security note: password should be removed from docker-compose file (and it should probably not be commited)*
    * [**adminer** (localhost:7780)](http://localhost:7780)
        * web-based DB-GUI
* used libraries:
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

other interesting libs:

* https://github.com/flasgger/flasgger
* https://flask-sqlalchemy.palletsprojects.com/

# Flask

```sh
cd flask-backend
flask init-db # apply db schema.
sqlitebrowser instance/flask-api.sqlite
flask run # see .flaskenv for envvars.
```

**database schema**

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

# resources

* https://github.blog/2021-12-06-write-more-secure-code-owasp-top-10-proactive-controls/

# FastAPI

# Connexion
