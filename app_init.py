import logging
from flask import Flask, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, UserMixin
from flask_migrate import Migrate
from models import db, User  # Importamos el modelo User desde models.py


# Configurar la aplicación Flask
app = Flask(__name__, static_folder='static')
# Importar rutas después de inicializar Flask
from routes import *
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
db.init_app(app)

# Configuración de migraciones
migrate = Migrate(app, db)

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirigir a /login si no está autenticado

# Función para cargar un usuario por ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Asegurar que user_id sea un entero



# Middleware para crear o actualizar el usuario en la base de datos
@app.after_request
def create_or_update_user(response):
    if 'user' in session and 'user_email' in session['user']:
        email = session['user']['user_email']
        profile_picture = session['user'].get('photo_url')

        user = User.query.filter_by(email=email).first()
        if not user:
            new_user = User(email=email, profile_picture=profile_picture)
            db.session.add(new_user)
            db.session.commit()
            logger.info(f"Created new user: {email}")
        elif user.profile_picture != profile_picture:
            user.profile_picture = profile_picture
            db.session.commit()
            logger.info(f"Updated profile picture for user: {email}")
    return response

# Iniciar la app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
