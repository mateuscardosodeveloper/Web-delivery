import wtforms as wtf
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from delivery.ext.db.models import Store, User, Category, Address, OrderItems, Order, Items
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class UserForm(FlaskForm):
    name = wtf.StringField("Nome", [wtf.validators.DataRequired()])
    email = wtf.StringField(
        "Email", [wtf.validators.DataRequired(), wtf.validators.Email()])
    password = wtf.PasswordField("Senha", [wtf.validators.DataRequired()])
    foto = FileField("Foto")


class LoginForm(FlaskForm):
    email = wtf.StringField(
        "Email", [wtf.validators.DataRequired(), wtf.validators.Email()]
    )
    password = wtf.PasswordField("Senha", [wtf.validators.DataRequired()])


class CategoryForm(FlaskForm):
    name = wtf.StringField("Nome", [wtf.validators.DataRequired()])
    on_menu = wtf.BooleanField("On-menu", default=True)


class CategoryEditForm(FlaskForm):
    name = wtf.StringField("Nome", [wtf.validators.DataRequired()])
    on_menu = wtf.BooleanField("On-menu")


class StoresForm(FlaskForm):
    name_store = wtf.StringField(
        "Nome da Loja", [wtf.validators.DataRequired()])
    category_id = QuerySelectField(
        query_factory=lambda: Category.query.all(), allow_blank=False, get_label='name')
    active = wtf.BooleanField("Ativo", default=True)


class StoreEditForm(FlaskForm):
    name_store = wtf.StringField(
        "Nome da Loja", [wtf.validators.DataRequired()])
    category_id = QuerySelectField(query_factory=lambda: Category.query.all(
    ), allow_blank=True, get_label='name', blank_text='Selecione uma Categoria')
    user_id = QuerySelectField(query_factory=lambda: User.query.all(
    ), allow_blank=True, blank_text='Seleciona um usuário')
    active = wtf.BooleanField("Ativo")


class ItemsForm(FlaskForm):
    name = wtf.StringField("Nome", [wtf.validators.DataRequired()])
    image = wtf.FileField("Image", [wtf.validators.DataRequired()])
    price = wtf.FloatField("Preço", [wtf.validators.DataRequired()])
    quantity = wtf.IntegerField("Quantidade", [wtf.validators.DataRequired()])
    description = wtf.TextAreaField ("Descrição", [wtf.validators.DataRequired()])
    store_id = QuerySelectField(
        'ID da loja', query_factory=lambda: Store.query.all())
    available = wtf.BooleanField("Disponivel", default=True)


class ItemsEditForm(FlaskForm):
    name = wtf.StringField("Nome", [wtf.validators.DataRequired()])
    image = FileField("Image")
    price = wtf.FloatField("Preço", [wtf.validators.DataRequired()])
    quantity = wtf.IntegerField("Quantidade", [wtf.validators.DataRequired()])
    description = wtf.TextAreaField("Descrição", [wtf.validators.DataRequired()])
    store_id = QuerySelectField('ID da loja', query_factory=lambda: Store.query.all(
    ), allow_blank=True, blank_text='Selecione uma loja')
    available = wtf.BooleanField("Disponivel")


class AddressForm(FlaskForm):
    zip_code = wtf.StringField("CEP", [wtf.validators.DataRequired()])
    state = wtf.StringField("Estado")
    city = wtf.StringField("Cidade")
    address = wtf.StringField("Endereço", [wtf.validators.DataRequired()])
    number_house = wtf.IntegerField("N°", [wtf.validators.DataRequired()])


class AddressEditForm(FlaskForm):
    zip_code = wtf.StringField("CEP", [wtf.validators.DataRequired()])
    state = wtf.StringField("Estado")
    city = wtf.StringField("Cidade")
    address = wtf.StringField("Endereço", [wtf.validators.DataRequired()])
    number_house = wtf.IntegerField("N°", [wtf.validators.DataRequired()])


class OrderForm(FlaskForm):
    created_at = wtf.StringField("Data e Hora")
    completed = wtf.BooleanField("Comprado")
    store_id = QuerySelectField(
        "ID da Loja", query_factory=lambda: Store.query.all())


class OrderEditForm(FlaskForm):
    created_at = wtf.StringField("Data e Hora")
    completed = wtf.BooleanField("Comprado")
    store_id = QuerySelectField("ID da Loja", query_factory=lambda: Store.query.all(
    ), allow_blank=True, blank_text='Selecione uma loja')


class OrderItemsForm(FlaskForm):
    order_id = QuerySelectField(
        "ID ordem de compra", query_factory=lambda: Order.query.all())
    items_id = QuerySelectField(
        "ID do tipo de menu", query_factory=lambda: Items.query.all())
    quant = wtf.IntegerField("Quantidade", [wtf.validators.DataRequired()])
