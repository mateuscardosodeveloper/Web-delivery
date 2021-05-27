from flask import Blueprint, render_template, request, send_from_directory
from flask import current_app as app
from delivery.ext.db.models import Items
from delivery.ext.auth.controller import list_image

page = Blueprint("page", __name__)


@page.route('/uploads/<file>')
def upload_file(file):
    return send_from_directory(app.config['UPLOAD_FOLDER_SEARCH'], file)


@page.route("/", methods=["GET"])
def index():
    item = Items.query.all()
    return render_template("index.html", item=item)


@page.route("/restaurantes")
def restaurants():
    return render_template("restaurants.html")


@page.route("/sobre")
def about():
    return render_template("about.html")
