# soaring-urls **(sURL)**

A simple URL Shortner, easy to deploy and use, developed using `Python`, `Flask`, and `SQLiteDict`.

## Deploy your own instance

Deployment is easy as this project relies in three (3) python libraries. Ensure python is installed `v2` or `v3` does not matter in our case.

Head to the project's root and install the necessary libraries using `pip install -r requirements.txt`.

Once all libraries are installed, simply run it with `FLASK_APP=main.py FLASK_ENV=production flask run` for production purposes or `FLASK_APP=main.py FLASK_ENV=development flask run` for development purposes.

## Attributions

1.  [Python](https://www.python.org/)
2. [Flask](https://flask.palletsprojects.com)
3. [SQLiteDict](https://pypi.org/project/sqlitedict/)
4. [Flask-Limiter](https://flask-limiter.readthedocs.io/en/stable/)