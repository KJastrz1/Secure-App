from flask import Blueprint, current_app as app, render_template, flash, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, DateField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo, Email
from sqlalchemy.orm import session
import os
from datetime import datetime, timedelta
from flask import session, redirect, url_for
from ..models import db, User, LoginAttempt
import requests

from .email_confirm import send_confirmation_email 
from secureApp.utils.utils import custom_password_validator, hash_password 

auth_bp = Blueprint('auth_bp', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=4, max=40)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm): 
        email = StringField('Email', validators=[InputRequired(), Length(min=4, max=40)])
        password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80),custom_password_validator])
        confirm = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=80), EqualTo('password', message='Passwords must match.')])
        submit = SubmitField('Register')
        
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        
        if user:            
            lockout_time = 5  
            if user.last_failed_login and (datetime.now() - user.last_failed_login) < timedelta(minutes=lockout_time) and user.failed_login_attempts >= 4:
                flash('Account temporarily locked due to too many failed login attempts. Please try again later.', 'error')
                return redirect(url_for('auth_bp.login'))


            stored_salt, stored_hash = user.password.split(':')         
            hashed_password = hash_password(form.password.data, stored_salt)

            ip_address ='83.9.109.176'
            print(ip_address)
            response=requests.get('http://ip-api.com/json/'+ip_address) 
            print(response)          
            if response.status_code == 200:
                response_dict = response.json()
                print("Response Dictionary:", response_dict)
            else:
                print("Failed to get location data")
                response_dict = {}
            login_attempt = LoginAttempt(
                    user_id=user.id,
                    ip_address=ip_address,
                    latitude=response_dict["lat"],
                    longitude=response_dict["lon"],
                    country=response_dict["country"],
                    city=response_dict["city"])
            
            if hashed_password == stored_hash:
              
                user.failed_login_attempts = 0
                user.last_failed_login = None                
                session['user_id'] = user.id
                login_attempt.success = True
                db.session.add(login_attempt)
                db.session.commit()
                return redirect(url_for('general_bp.dashboard'))
            else:
                user.failed_login_attempts = user.failed_login_attempts+1
                user.last_failed_login = datetime.now()
                login_attempt.success = False
                db.session.add(login_attempt)
                db.session.commit()        
        flash("Email or password incorrect", 'error')
        return redirect(url_for('auth_bp.login'))

    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():   
    try:
        form = RegisterForm()
        if form.validate_on_submit(): 
        
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user is not None:
                flash('Email already registered.', 'error')
                return redirect(url_for('auth_bp.register'))   
            
            salt = os.urandom(16).hex() 
                   
            hashed_password=hash_password(form.password.data, salt)
            hashed_password = salt + ':' + hashed_password
            new_user = User(email=form.email.data, password=hashed_password)
            db.session.add(new_user)

            send_confirmation_email(new_user)
            flash('Confirmation email has been sent to you', 'success')
            db.session.commit()
            return redirect(url_for('auth_bp.login'))
    except ValidationError as e:
        print(e)
        flash(str(e), 'error')
        return redirect(url_for('auth_bp.register'))

    return render_template('register.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('general_bp.home'))