import os
from wtforms import PasswordField, StringField, ValidationError
from ..models import db, User  
from flask import flash, render_template, redirect, url_for, current_app
from itsdangerous import URLSafeTimedSerializer
from secureApp.utils.utils import custom_password_validator, hash_password, send_email
from wtforms.validators import InputRequired
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import Length, EqualTo
from flask import Blueprint

reset_password_bp = Blueprint('reset_password_bp', __name__)

class EmailForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=4, max=40)])
    submit = SubmitField('Reset Password')

class NewPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[InputRequired(), Length(min=8, max=80), custom_password_validator])
    confirm = PasswordField('Confirm New Password', validators=[InputRequired(), Length(min=8, max=80),EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Change Password')

@reset_password_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = EmailForm()

    if form.validate_on_submit():   
 
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('Email not found.', 'error')
            return render_template('reset_password.html', form=form)

        token = generate_reset_token(user.email)
 
        send_password_reset_email(user.email, token)

    
        flash('Password reset instructions have been sent to your email.', 'success')
        return redirect(url_for('auth_bp.login'))

    return render_template('reset_password.html', form=form)


@reset_password_bp.route('/new_password/<token>', methods=['GET', 'POST'])
def new_password(token):
    email = verify_reset_token(token)

    if not email:
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('auth_bp.login'))
    form=NewPasswordForm()
    try:
        if form.validate_on_submit():         
            user = User.query.filter_by(email=email).first()
            salt= os.urandom(16).hex()
            hashed_password = hash_password(form.password.data, salt)
            hashed_password = salt + ':' + hashed_password
            user.password = hashed_password
            db.session.commit()
            flash('Password updated successfully.', 'success')
            return redirect(url_for('auth_bp.login'))

    except ValidationError as e:
        print(e)
        flash(str(e), 'error')
        return redirect(url_for('reset_password_set_new.html'))
    
    return render_template('reset_password_set_new.html', form=form)


def send_password_reset_email(to, token):
    reset_url = url_for('reset_password_bp.new_password', token=token, _external=True)

    subject = "Password Reset Request"
    template=render_template('reset_password_email.html', reset_url=reset_url)
   
    send_email(to, subject, template)
    
    
    
def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
        token,
        salt=current_app.config['SECURITY_PASSWORD_SALT'],
        max_age=expiration
        )
    except:
        return False
    return email


    
