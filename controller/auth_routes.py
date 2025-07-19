from main import app
from flask import render_template, redirect,request,flash,session,url_for
from controller.models import *

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'user_email' in session:
            flash('You are already logged in!', 'info')
            return redirect(url_for('home'))
        
        return render_template('login.html')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #Data Validation
        if not email or not password:
            flash('Please enter email and password!!', 'error')
            return redirect(url_for('login'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return redirect(url_for('login'))
        
        if '@' not in email:
            flash('Please enter a valid email address!', 'error')
            return redirect(url_for('login'))
        
       
        user = User.query.filter_by(user_email=email).first()

        if not user:
            flash('User not registered! Please register first.', 'error')
            return redirect(url_for('login'))
        
        if user.user_password != password:
            flash('Password is wrong! Please try again.', 'error')
            return redirect(url_for('login'))
        
        session['user_email'] = user.user_email
        session['user_role'] = user.role.name
        flash('Login successful!', 'success')


        return redirect(url_for('home'))  


@app.route('/logout')
def logout():
    session.pop('user_email', None)
    session.pop('user_role', None)
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        if 'user_email' in session:
            flash('You are already logged in!', 'info')
            return redirect(url_for('home'))
        return render_template('signup.html')
    
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        name = request.form.get('full_name')
        address = request.form.get('address')
        pincode = request.form.get('pincode')

        #Data Validation
        if not email or not password :
            flash('All fields are compulsory!', 'error')
            return redirect(url_for('signup'))
        
        if len(password) < 8:
            flash('Password must be at least 6 characters long!', 'error')
            return redirect(url_for('signup'))
        
        if '@' not in email:
            flash('Please enter a valid email address!', 'error')
            return redirect(url_for('signup'))
        
        if password!= confirm_password:
            flash("Password and Confirm Password doesn't match!")
            return redirect(url_for('signup'))

        # Check if user already exists
        user = User.query.filter_by(user_email=email).first()
        if user:
            flash('User already exists! Please log in.', 'error')
            return redirect(url_for('login'))

        # Create new user
        role = Role.query.filter_by(name='user').first()
        user = User(
            user_email=email,
            user_password=password,
            user_name=name,
            user_address=address,
            user_pincode=pincode,
            role_id=role.id if role else 2  # Fallback to 2 if 'user' role not found
        
        )
        
        db.session.add(user)
        db.session.commit()

        flash('User successfully registered, Now log in !', 'success')
        return redirect(url_for('login'))



