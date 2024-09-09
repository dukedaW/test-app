from flask import Flask, render_template, jsonify, Blueprint, redirect, url_for, request
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, DateField, BooleanField, FloatField, IntegerField
from wtforms.validators import DataRequired
from app import app, db
from buyer import Buyer
from purchase import Purchase
from product import Product


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
