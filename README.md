# soaring-urls **(sURL)**

A simple URL Shortner, easy to deploy and use, developed using `Python`, `Flask`, and `SQLiteDict`.

## Deploy your own instance

Deployment is easy as this project relies in three (3) python libraries. Ensure python is installed `v2` or `v3` does not matter in our case.

Head to the project's root and install the necessary libraries using `pip install -r requirements.txt`.

Once all libraries are installed, simply run it with `FLASK_APP=main.py FLASK_ENV=production flask run` for production purposes or `FLASK_APP=main.py FLASK_ENV=development flask run` for development purposes.

## Routes

There are two main routes at the time of development, main page and the URL translation page. The main page handles both `GET` and `POST` requests whereas, the translation page only handles `GET` requests.

1. Homepage (root)
   - `/` - `GET` request does not accept nor expects any arguments nor parameters. Simply returns the homepage template to the clients.
   - `/` - `POST` request requires the request to include `url` parameter with valid URL as a string. Utilizes Django's URL validation regex to verify URL.
2. URL Translation
   - `/<ID>` - `GET` requires shortened ID generated from the `/`'s `POST` method. It checks the passed `<ID>` against the database and returns a temporary redirect to the translated URL.

### Limitations

Rate limitation has been put in place to avoid spams and irregular requests, using a nifty Python library called `Flask-Limiter`.

1. `/` - `GET` - No limitations are put in place for this route and method.
2. `/` - `POST` - 1 request per second.
3. `/<ID>` - `GET` - 1 request per second. *(I've Been receiving high amount of irregular requests in this route)*

## Attributions

1. [Python](https://www.python.org/)
2. [Flask](https://flask.palletsprojects.com)
3. [SQLiteDict](https://pypi.org/project/sqlitedict/)
4. [Flask-Limiter](https://flask-limiter.readthedocs.io/en/stable/)
5. [Django's URL Validation Regex](https://stackoverflow.com/a/7995979)