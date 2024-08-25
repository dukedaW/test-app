from flask import Flask, render_template, jsonify, Blueprint, redirect, url_for, request

from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, BooleanField, FloatField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task2.db"
app.config['SECRET_KEY'] = 'key'
db = SQLAlchemy(app)


class Buyer(db.Model):
    __tablename__ = 'buyers'

    buyer_id = db.Column(db.Integer, primary_key=True)

    firstname = db.Column(db.String(100), nullable=False)

    lastname = db.Column(db.String(100), nullable=False)

    birth_date = db.Column(db.DATE, nullable=False)

    sex = db.Column(db.CHAR, nullable=False)

    reg_date = db.Column(db.DATE, nullable=False)

    consent = db.Column(db.BOOLEAN, nullable=False)

    def __init__(self, firstname, lastname, birth_date, sex, consent):
        self.firstname = firstname
        self.lastname = lastname
        self.birth_date = birth_date
        self.sex = sex
        self.consent = consent
        self.reg_date = datetime.today()

    def __repr__(self):
        return (f'({self.buyer_id}, {self.firstname}, {self.lastname}, {self.birth_date}, {self.sex}, {self.reg_date}, '
                f'{self.consent})')


class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    purchase_cost = db.Column(db.FLOAT)

    selling_price = db.Column(db.FLOAT)

    def __init__(self, name, purchase_cost, selling_price):
        self.name = name
        self.purchase_cost = purchase_cost
        self.selling_price = selling_price

    def __repr__(self):
        return f'({self.product_id}, {self.name}, {self.purchase_cost}, {self.selling_price})'


class ProductForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    purchase_cost = FloatField('purchase cost', validators=[DataRequired()])
    selling_price = FloatField('selling price', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/buyers_page', methods=['GET', 'POST'])
def buyers_page():
    form = BuyerForm()
    if form.validate_on_submit():
        buyer = Buyer(firstname=form.firstname.data, lastname=form.lastname.data, birth_date=form.birthday.data,
                      sex=form.sex.data, consent=form.consent.data)
        db.session.add(buyer)
        db.session.commit()
        return redirect(url_for('buyers_page'))
    buyers = Buyer.query.all()
    return render_template('buyers_page.html', form=form, buyers=buyers)


@app.route('/delete_buyer/<int:buyer_id>', methods=['POST'])
def delete_buyer(buyer_id):
    buyer = Buyer.query.get_or_404(buyer_id)
    db.session.delete(buyer)
    db.session.commit()
    return redirect(url_for('buyers_page'))


class BuyerForm(FlaskForm):
    firstname = StringField('name', validators=[DataRequired()])
    lastname = StringField('last name', validators=[DataRequired()])
    sex = StringField('sex', validators=[DataRequired()])
    birthday = DateField('Date of birth', validators=[DataRequired()])
    # email = StringField('Email', validators=[DataRequired()])
    consent = BooleanField('Consent for data processing', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/update_buyer/<int:buyer_id>', methods=['GET', 'POST'])
def update_buyer(buyer_id):
    buyer = Buyer.query.get_or_404(buyer_id)
    form = BuyerForm(obj=buyer)
    if form.validate_on_submit():
        buyer.firstname = form.firstname.data
        buyer.lastname = form.lastname.data
        buyer.sex = form.sex.data
        buyer.consent = form.consent.data
        buyer.birth_date = form.birthday.data
        db.session.commit()
        return redirect(url_for('buyers_page'))
    return render_template('update_buyer.html', form=form)


'''
    Products
'''


@app.route('/products_page', methods=['GET', 'POST'])
def products_page():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, purchase_cost=form.purchase_cost.data,
                          selling_price=form.selling_price.data)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('products_page'))
    products = Product.query.all()
    return render_template('products_page.html', form=form, products=products)


@app.route('/update_product/<int:product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.selling_price = form.selling_price.data
        product.purchase_cost = form.purchase_cost.data
        db.session.commit()
        return redirect(url_for('products_page'))
    return render_template('update_product.html', form=form)


@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('products_page'))


def create_tables():
    db.create_all()


def fill_db():
    prod = Product('banana', 10.0, 12.0)
    db.session.add(prod)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(host='127.0.0.1', debug=True)
