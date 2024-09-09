from flask import Flask, render_template, jsonify, Blueprint, redirect, url_for, request
from wtforms.validators import DataRequired
from app import app, db
from datetime import datetime, date
from wtforms import StringField, SubmitField, DateField, BooleanField, FloatField, IntegerField
from flask_wtf import FlaskForm, CSRFProtect


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
