from flask import Flask, render_template, jsonify, Blueprint, redirect, url_for, request
from wtforms.validators import DataRequired
from app import app, db
from datetime import datetime, date
from wtforms import StringField, SubmitField, DateField, BooleanField, FloatField, IntegerField
from flask_wtf import FlaskForm, CSRFProtect
from product import Product
from buyer import Buyer


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
