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

```sh
cd flask-backend
export FLASK_APP=api
export FLASK_ENV=development
flask run --host 0.0.0.0 --port 7701 # bind to all interfaces.
```

# FastAPI

# Connexion
