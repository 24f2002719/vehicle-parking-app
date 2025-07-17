from flask import Flask, render_template
from controller.database import db
from controller.config import Config
from controller.models import *



app = Flask(__name__,template_folder='templates',static_folder='static')
app.config.from_object(Config)
# configure the SQLite database, relative to the app instance folder
# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.sqlite3'
db.init_app(app)

with app.app_context():
    db.create_all()

    if Role.query.first() is None:
        admin_role = Role(name='admin')
        user_role = Role(name='user')
        db.session.add_all([admin_role, user_role])

    admin_user = User.query.filter_by(user_email = 'admin@gmail.com').first()
    if not admin_user:
        admin_user = User(
            user_email = 'admin@gmail.com',
            user_password = 'admin123',
            user_name = 'Admin',
            # user_address = 'Admin Address',
            # user_pincode = '123456',
            role = admin_role
            )
        db.session.add(admin_user)

    
    db.session.commit()

@app.route('/')
def index():
    return render_template('hello.html')

@app.route('/about')
def about():
    return "About"

if __name__ == "__main__" :
    app.run()