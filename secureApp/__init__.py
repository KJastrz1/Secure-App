from flask import Flask
from flask_migrate import Migrate
from flask_mail import Mail
from .models import db
import os
from dotenv import load_dotenv


load_dotenv()

mail=Mail()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['PEPPER'] = os.environ.get('PEPPER')
    app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT')
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_USER')


    db.init_app(app)
    migrate = Migrate(app, db)
    mail.init_app(app)

    with app.app_context():
        from .auth.auth import auth_bp
        from .auth.email_confirm import email_confirm_bp
        from .loans.loans import loans_bp
        from .general.general import general_bp
        from .auth.reset_password import reset_password_bp
   
        app.register_blueprint(auth_bp)
        app.register_blueprint(email_confirm_bp)
        app.register_blueprint(loans_bp)
        app.register_blueprint(general_bp)
        app.register_blueprint(reset_password_bp)

    return app
