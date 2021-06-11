from flask import Blueprint, render_template, request, send_from_directory
from flask import current_app as app
from delivery.ext.db.models import Items, Store
from delivery.ext.auth.controller import list_image

page = Blueprint("page", __name__)


@page.route('/uploads/<file>')
def upload_file(file):
    return send_from_directory(app.config['UPLOAD_FOLDER_SEARCH'], file)


@page.route("/", methods=["GET"])
def index():
    store = Store.query.all()
    items = Items.query.all()
    return render_template("index.html", store=store, items=items)


@page.route("/restaurantes", methods=["GET"])
def restaurants():
    store = Store.query.all()
    return render_template("restaurants.html", store=store)

@page.route("/sorveteria", methods=["GET"])
def sorveteria():
    item = Items.query.all()
    store = Store.query.all()
    return render_template("sorveteria.html", item=item, store=store)

@page.route("/lanches", methods=["GET"])
def lanches():
    item = Items.query.all()
    store = Store.query.all()
    return render_template("lanches.html", item=item, store=store)

@page.route("/pasteis", methods=["GET"])
def pasteis():
    item = Items.query.all()
    store = Store.query.all()
    return render_template("pasteis.html", item=item, store=store)


@page.route("/sobre")
def about():
    return render_template("about.html")
