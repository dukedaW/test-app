from flask import Flask, render_template, jsonify, Blueprint, redirect, url_for, request
from wtforms.validators import DataRequired
from app import app, db
from datetime import datetime, date
from wtforms import StringField, SubmitField, DateField, BooleanField, FloatField, IntegerField
from flask_wtf import FlaskForm, CSRFProtect


class Buyer(db.Model):
    __tablename__ = 'buyers'

    buyer_id = db.Column(db.Integer, primary_key=True)

    firstname = db.Column(db.String(100), nullable=False)

    lastname = db.Column(db.String(100), nullable=False)

    birth_date = db.Column(db.DATE, nullable=False)

    sex = db.Column(db.CHAR, nullable=False)

    reg_date = db.Column(db.DATE, nullable=False)

    consent = db.Column(db.BOOLEAN)

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


class BuyerForm(FlaskForm):
    firstname = StringField('name', validators=[DataRequired()])
    lastname = StringField('last name', validators=[DataRequired()])
    sex = StringField('sex', validators=[DataRequired()])
    birthday = DateField('Date of birth', validators=[DataRequired()])
    # email = StringField('Email', validators=[DataRequired()])
    consent = BooleanField('Consent for data processing', validators=[DataRequired()])
    submit = SubmitField('Submit')


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
