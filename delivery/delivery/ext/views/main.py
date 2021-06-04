from flask import Blueprint, current_app, render_template, redirect, request, url_for, flash, send_from_directory
from flask_login import current_user, login_required, login_user
from flask_login.utils import login_required, logout_user

from delivery.ext.db import db
from delivery.ext.db.models import User, Items, Store
from delivery.ext.auth.form import UserForm, LoginForm
from delivery.ext.auth.controller import create_user, save_user_picture, list_image


main = Blueprint("main", __name__)


@main.before_request
def before_request():
    if current_user.is_authenticated:
        if request.endpoint == 'main.login':
            return redirect(url_for("page.index"))


@main.route("/cadastro", methods=["GET", "POST"])
def signup():
    form = UserForm()

    if form.validate_on_submit():
        try:
            create_user(
                name=form.name.data,
                email=form.email.data,
                password=form.password.data,
            )
            foto = request.files.get('foto')
            if foto:
                save_user_picture(
                    foto.filename,
                    foto
                )
            flash('Cadastrado com Sucesso! Por favor faça o login.', 'success')
            return redirect(url_for(".login"))
        except Exception:
            flash("Este email já esta cadastrado!   ", "danger")
            return redirect(url_for('.signup'))

    return render_template("login/userform.html", form=form)


@main.route("/entrar", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User()
        auth = user.auth(form.email.data, form.password.data)

        if not auth:
            flash("suas credênciais estão incorretas!", "danger")
            return redirect(url_for('.login'))

        login_user(auth)
        return redirect(url_for('page.index'))

    return render_template('login/efectlogin.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))

@main.route('/alimento/<id>', methods=['GET', ])
def foods_id(id):
    items = Items.query.filter_by(id=id).first()
    nome_arquivo = list_image(id)

    return render_template('order/foods.html', items=items, capa_item=nome_arquivo)

@main.route('/restaurants_items/<id>', methods=['GET',])
def restaurants_items(id):
    stores = Store.query.filter_by(id=id).first()
    item = Items.query.all()
    return render_template('restaurants_items.html', item=item, stores=stores)

@main.route('/carrinho', methods=['GET', 'POST'])
def cart():
    items = Items.query.all()

    return render_template('order/cart.html', items=items)
