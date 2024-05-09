from functools import wraps
import hashlib
from datetime import date
from flask import app, redirect, request, session, url_for, current_app
import pwnedpasswords
from wtforms import ValidationError
from .. import mail 
from flask_mail import Message

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth_bp.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function 


def custom_amount_validator(form, field):   
    if field.data < 0:
        raise ValidationError('Amount must be positive.')

def custom_date_validator(form, field):
    if field.data <= date.today():
        raise ValidationError('Date must be in the future.')

def custom_password_validator(form, field):
   
    password = field.data

    if not any(char.isdigit() for char in password):
        raise ValidationError('Password must contain at least one digit.')

    if not any(char.isalpha() for char in password):
        raise ValidationError('Password must contain at least one letter.')

    if not any(not char.isalnum() for char in password):
        raise ValidationError('Password must contain at least one special character .')
    print(pwnedpasswords.check(password))
    if pwnedpasswords.check(password)>100:
        raise ValidationError('Password has been compromised. Please choose a different password.')

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)


def hash_password(password, salt):
    hashed_password = hashlib.sha3_256((password + salt + current_app.config['PEPPER']).encode()).hexdigest()
    for i in range(1000):
        hashed_password = hashlib.sha3_256(hashed_password.encode()).hexdigest()
    return hashed_password




