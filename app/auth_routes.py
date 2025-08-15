# auth_routes.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app.models import User, users_collection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.get_by_email(email)

        if user and user.check_password(password):
            login_user(user) # Inicia la sesión para el usuario
            return redirect(url_for('main.home'))
        else:
            flash('Email o contraseña incorrectos.')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if User.get_by_email(email):
            flash('Este email ya está registrado.')
            return redirect(url_for('auth.register'))

        new_user_data = {'email': email}
        new_user = User(new_user_data)
        new_user.set_password(password)
        
        users_collection.insert_one({
            'email': new_user.email,
            'password_hash': new_user.password_hash
        })

        flash('¡Registro exitoso! Por favor, inicia sesión.')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/logout')
@login_required # Solo usuarios logueados pueden desloguearse
def logout():
    logout_user()
    return redirect(url_for('auth.login'))