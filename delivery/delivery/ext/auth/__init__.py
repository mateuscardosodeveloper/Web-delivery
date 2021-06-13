from delivery.ext.db import models #noqa
from delivery.ext.auth.commands import add_user, add_category, add_store, add_item, add_address, add_order, del_category
from delivery.ext.auth.controller import list_users, list_categorys, list_stores, list_itens, list_address, list_order

from delivery.ext.db import db
from delivery.ext.auth.admin import UserAdmin
from delivery.ext.admin import admin
from delivery.ext.db.models import User
from delivery.ext.auth.admin import AdminView

def init_app(app):
    app.cli.command()(list_users)
    app.cli.command()(list_categorys)
    app.cli.command()(list_stores)
    app.cli.command()(list_itens)
    app.cli.command()(list_address)
    app.cli.command()(list_order)
    app.cli.command()(add_user)
    app.cli.command()(add_category)
    app.cli.command()(add_store)
    app.cli.command()(add_item)
    app.cli.command()(add_address)
    app.cli.command()(add_order)
    app.cli.command()(del_category)

    admin.add_view(UserAdmin(User, db.session))