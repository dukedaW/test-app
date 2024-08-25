from flask import Flask, render_template, jsonify, Blueprint, redirect, url_for, request

from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, BooleanField
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


class Products(db.Model):
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


@app.route('/', methods=['GET', 'POST'])
def index():
    form = BuyerForm()
    if form.validate_on_submit():
        buyer = Buyer(firstname=form.firstname.data, lastname=form.lastname.data, birth_date=form.birthday.data,
                      sex=form.sex.data, consent=form.consent.data)
        db.session.add(buyer)
        db.session.commit()
        return redirect(url_for('index'))
    buyers = Buyer.query.all()
    return render_template('index.html', form=form, buyers=buyers)


@app.route('/delete/<int:buyer_id>')
def delete(buyer_id):
    buyer = Buyer.query.get_or_404(buyer_id)
    db.session.delete(buyer)
    db.session.commit()
    return redirect(url_for('index'))


class BuyerForm(FlaskForm):
    firstname = StringField('name', validators=[DataRequired()])
    lastname = StringField('last name', validators=[DataRequired()])
    sex = StringField('sex', validators=[DataRequired()])
    birthday = DateField('Date of birth', validators=[DataRequired()])
    # email = StringField('Email', validators=[DataRequired()])
    consent = BooleanField('Consent for data processing', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/update_buyer/<int:buyer_id>', methods=['GET', 'POST'])
def update(buyer_id):
    buyer = Buyer.query.get_or_404(buyer_id)
    form = BuyerForm(obj=buyer)
    if form.validate_on_submit():
        buyer.firstname = form.firstname.data
        buyer.lastname = form.lastname.data
        buyer.sex = form.sex.data
        buyer.consent = form.consent.data
        buyer.birth_date = form.birthday.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_buyer.html', form=form)


def create_tables():
    db.create_all()


def fill_db():
    prod = Products('banana', 10.0, 12.0)
    db.session.add(prod)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(host='127.0.0.1', debug=True)
