# auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, User
import logging

# Configuración de logging
logger = logging.getLogger(__name__)

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Verificar si el usuario o email ya existen
        user_by_username = User.query.filter_by(username=username).first()
        user_by_email = User.query.filter_by(email=email).first()

        if user_by_username:
            flash('El nombre de usuario ya está en uso.')
            return redirect(url_for('auth.register'))

        if user_by_email:
            flash('El correo electrónico ya está registrado.')
            return redirect(url_for('auth.register'))

        # Crear nuevo usuario
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        logger.info(f"Usuario registrado: {email}")
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Por favor verifica tus credenciales e intenta nuevamente.')
            return redirect(url_for('auth.login'))

        # Guardar información del usuario en la sesión (para mantener compatibilidad)
        session['user'] = {
            'user_email': user.email,
            'photo_url': user.profile_picture if hasattr(user, 'profile_picture') else None
        }

        login_user(user, remember=remember)
        logger.info(f"Usuario autenticado: {email}")

        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('routes.index')

        return redirect(next_page)

    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    # Limpiar la sesión
    if 'user' in session:
        session.pop('user')

    logout_user()
    flash('Has cerrado sesión correctamente.')
    logger.info("Usuario cerró sesión")
    return redirect(url_for('routes.index'))
