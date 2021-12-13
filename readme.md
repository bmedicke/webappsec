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

* [local setup](#local-setup)
* [Flask](#flask)
* [resources](#resources)
* [FastAPI](#fastapi)
* [Connexion](#connexion)

<!-- vim-markdown-toc -->

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

---

other interesting libs:

* https://github.com/flasgger/flasgger
* https://flask-sqlalchemy.palletsprojects.com/

# Flask

```sh
cd flask-backend
flask run # see .flaskenv for envvars.
```

* [flask (localhost:7701)](http://localhost:7701)
* *security note: the `.flaskenv` file should not be commited if there are
any secrets stored in it*
    * you could use the `.env` file for secrets
* *security note: when returning HTML (the default) user provided values
must be `escape()`d to prevent injections*
    * unsafe: `http://localhost:7701/i/<body onload='alert("this is bad");'>`
    * safe: `http://localhost:7701/u/<body onload='alert("this is bad");'>`
    * Jinja templates do this automatically

# resources

* https://github.blog/2021-12-06-write-more-secure-code-owasp-top-10-proactive-controls/

# FastAPI

# Connexion
