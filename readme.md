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
* [FastAPI](#fastapi)
* [Connexion](#connexion)

<!-- vim-markdown-toc -->

# local setup

```sh
python3 -m venv env && source env/bin/activate
pip install -r requirements.txt
# flask, fastapi, connexion, python-dotenv
```

# Flask

http://localhost:7701

```sh
cd flask-backend
flask run # see .flaskenv for envvars.
```

* *security note: the `.flaskenv` file should not be commited if there are
any secrets stored in it*
    * you could use the `.env` file for secrets
    * **TODO: show injection without escape** (`/i` route)
* *security note: when returning HTML (the default) user provided values
must be `escape()`d to prevent injections*
    * Jinja templates do this automatically

# FastAPI

# Connexion
