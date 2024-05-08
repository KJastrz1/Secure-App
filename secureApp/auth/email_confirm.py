from flask import Blueprint, current_app as app, flash, redirect, render_template, url_for
from itsdangerous import URLSafeTimedSerializer

from secureApp.utils.utils import send_email
from ..models import db, User



email_confirm_bp = Blueprint('email_confirm_bp', __name__)

@email_confirm_bp.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = verify_confirmation_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('auth_bp.login'))

    user = User.query.filter_by(email=email).first_or_404()
    if user.emailConfirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.emailConfirmed = True
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('auth_bp.login'))


def send_confirmation_email(new_user):
            
        token = generate_confirmation_token(new_user.email)

        confirm_url = url_for('email_confirm_bp.confirm_email', token=token, _external=True)
    
        template = render_template('activate_email.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(new_user.email, subject, template)  


    
    
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def verify_confirmation_token(token, expiration=3600*24):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
        token,
        salt=app.config['SECURITY_PASSWORD_SALT'],
        max_age=expiration
        )
    except:
        return False
    return email


