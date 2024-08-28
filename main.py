from flask import Flask, render_template, jsonify, Blueprint, redirect, url_for, request
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, DateField, BooleanField, FloatField, IntegerField
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


class Purchase(db.Model):
    purchase_id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey(Buyer.buyer_id), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.product_id), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.Date)

    def __init__(self, buyer_id, product_id, amount, purchase_date):
        self.buyer_id = buyer_id
        self.product_id = product_id
        self.purchase_date = purchase_date
        self.amount = amount


class PurchaseForm(FlaskForm):
    buyer = IntegerField('buyer', validators=[DataRequired()])
    product = IntegerField('product', validators=[DataRequired()])
    purchase_date = DateField('Purchase Date', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/purchases_page', methods=['GET', 'POST'])
def purchases_page():
    form = PurchaseForm()
    if form.validate_on_submit():
        purchase = Purchase(buyer_id=form.buyer.data, product_id=form.product.data,
                            purchase_date=form.purchase_date.data, amount=form.amount.data)
        db.session.add(purchase)
        db.session.commit()
        return redirect(url_for('purchases_page'))
    purchases = Purchase.query.all()
    return render_template('purchases_page.html', form=form, purchases=purchases)


@app.route('/update_purchase/<int:purchase_id>', methods=['GET', 'POST'])
def update_purchase(purchase_id):
    purchase = Purchase.query.get_or_404(purchase_id)
    form = PurchaseForm(obj=purchase)
    if form.validate_on_submit():
        purchase.product_id = form.product.data
        purchase.buyer_id = form.buyer.data
        purchase.amount = form.amount.data
        purchase.purchase_date = form.purchase_date.data
        db.session.commit()
        return redirect(url_for('purchases_page'))
    return render_template('update_purchase.html', form=form)


@app.route('/delete_purchase/<int:purchase_id>', methods=['POST'])
def delete_purchase(purchase_id):
    purchase = Purchase.query.get_or_404(purchase_id)
    db.session.delete(purchase)
    db.session.commit()
    return redirect(url_for('purchases_page'))


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


def create_report(purchase_date):
    purchases = Purchase.query.filter(Purchase.purchase_date == purchase_date).all()
    buyers = list()
    total_price = 0.0
    for purchase in purchases:
        buyer = Buyer.query.get_or_404(purchase.buyer_id)
        buyers.append(f'{buyer.lastname}, {buyer.firstname}')

        product = Product.query.get_or_404(purchase.product_id)
        total_price += product.selling_price * purchase.amount

    return buyers, total_price


class DateForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/report_page', methods=['GET', 'POST'])
def report_page():
    form = DateForm()

    if form.validate_on_submit():
        purchase_date = form.date.data
        buyers, total_price = create_report(purchase_date)
        return render_template('report_page.html', form=form, buyers=buyers, total_price=total_price)
    return render_template('report_page.html', form=form)


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
