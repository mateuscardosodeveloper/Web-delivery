from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from delivery.ext.db import db
from delivery.ext.db.models import Category
from delivery.ext.db.models import Store
from delivery.ext.db.models import Items
from delivery.ext.db.models import Order
from delivery.ext.db.models import OrderItems
from delivery.ext.db.models import Checkout
from delivery.ext.db.models import Address
from delivery.ext.auth.admin import HomeAdminView

from delivery.ext.auth.admin import AdminView


admin = Admin(url='/entrar', index_view=HomeAdminView(name='Home'))


def init_app(app):
    admin.name = "CodeFoods"
    admin.template_mode = "bootstrap2"
    admin.init_app(app)

    admin.add_view(AdminView(Category, db.session))
    admin.add_view(AdminView(Store, db.session))
    admin.add_view(AdminView(Items, db.session))
    admin.add_view(AdminView(Order, db.session))
    admin.add_view(AdminView(OrderItems, db.session))
    admin.add_view(AdminView(Checkout, db.session))
    admin.add_view(AdminView(Address, db.session))
