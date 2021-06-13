from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla import filters
from flask_admin.actions import action
from flask_admin import AdminIndexView

from delivery.ext.db.models import User
from delivery.ext.db import db

from flask import flash, Markup, redirect, url_for, request

from flask_login import current_user

from sqlalchemy import event
from werkzeug.security import generate_password_hash


# def format_user(self, request, user, *args):
# return user.email.split("@")[0]


class AdminView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin


class HomeAdminView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('main.login', next=request.url))


class UserAdmin(AdminView):
    """Interface admin de user"""

    @event.listens_for(User.password, 'set', retval=True)
    def hash_user_password(target, value, oldvalue, initiator):
        if value != oldvalue:
            return generate_password_hash(value)
        return value

    column_formatters = {
        # "email": lambda s, r, u, *a: Markup(f'<b>{u.email.split("@")[0]}<b>')
    }

    column_list = ['email', 'name', 'admin']

    column_searchable_list = ['email']

    column_filters = [
        filters.FilterLike(
            User.email,
            "Email",
            options=(("gmail", "Gmail"), ("hotmail", "Hotmail"),
                     ("outlook", "Outlook"))
        ),
        'name',
        'admin'
    ]

    can_edit = False

    @action(
        'togle_admin',
        'Togle admin status',
        'Are you sure?'
    )
    def toggle_admin_status(self, ids):
        users = User.query.filter(User.id.in_(ids)).all()
        for user in users:
            user.admin = not user.admin
        db.session.commit()
        flash(f"{len(users)}Usuário alterados com sucesso.", "success")

    @action("send_email", "send Email to all users", "Are you sure?")
    def send_email(self, ids):
        users = User.query.filter(User.id.in_(ids)).all()
        # 1) redirect para um form para escrever a mensagem do email
        # 2) enviar o email
        flash(f"{len(users)} emails enviados com sucesso.", "success")
