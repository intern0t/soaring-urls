from flask import Flask, request, jsonify, redirect, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import hashlib
import time
from sqlitedict import SqliteDict
from config import CONFIGS

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

database = SqliteDict("./%s" % CONFIGS["DATABASE_NAME"], autocommit=True)

'''
 Root route, entry point for the shortener application.
'''


@app.route('/', methods=['GET'])
@limiter.exempt
def get_index():
    if request.method == 'GET':
        # Use template engines/custom templates to send a form & handle form submit.
        # return jsonify(error=False, message="OK!"), 200
        return render_template('index.html', title=CONFIGS['SITE_INFO']['title'], description=CONFIGS['SITE_INFO']['description'], deploy_url=CONFIGS['DOMAIN'], year=CONFIGS['SITE_INFO']['year']), 200
    else:
        return jsonify(error=True, message="Not OK!"), 404


@app.route('/', methods=['POST'])
@limiter.limit("1/second")
def post_method():
    if request.method == 'POST':
        # Someone used unorthodox method to shorten their URLs.
        long_url = request.form.get('url')
        if long_url != None and len(long_url) >= 20 and is_valid_url(long_url):
            if url_exists(long_url) == False:
                # URL doesn't exist in the database, add to database.
                id = generate_id(long_url)
                database[id] = str(long_url)
                return jsonify(error=False, id=id, url=long_url, shortened="%s/%s" % (CONFIGS['DOMAIN'], id)), 200
            else:
                # URL exists, find & return the key.
                id = generate_id(long_url)
                return jsonify(error=False, message="URL exists.", id=id, url=long_url, shortened="%s/%s" % (CONFIGS['DOMAIN'], id))
        else:
            return jsonify(error=True, message="The url parameter must be provided, more than 20 characters long, and a valid URL.", url_length="Unknown" if long_url == None else len(long_url), valid_url=is_valid_url(long_url), url=long_url)
    else:
        return jsonify(error=True, message="Not OK!"), 404


@app.route("/<id>", methods=['GET'])
@limiter.exempt
def navigate(id):
    if id != None and len(id) == CONFIGS['ID_LENGTH']:
        if id in database:
            return redirect("%s" % database[id], code=302)
        else:
            return jsonify(error=True, id=id, message="No URL exists in the database that could be resolved by the ID you provided.")
    else:
        return jsonify(error=True, id=id, message="The ID you provided does not meet our ID specifications.")


def md5(url):
    url = str(url)
    hashed = hashlib.md5(url.encode())
    return hashed.hexdigest()


def get_timestamp():
    return time.time()


def generate_id(url):
    timestamp = md5(url)
    return timestamp[:CONFIGS['ID_LENGTH']]


def url_exists(url) -> bool:
    url_id = generate_id(url)
    if url_id in database:
        return True
    else:
        return False

# REF: https://stackoverflow.com/a/7995979


def is_valid_url(url):
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)
