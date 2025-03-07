import logging
from flask import Flask, session, request
from flask_login import LoginManager, login_required, login_user, UserMixin
from models import db, User
from flask_migrate import Migrate

# Configurar la aplicación Flask
app = Flask(__name__, static_folder='static')
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

# Definir el modelo de usuario
class User(UserMixin):
    def __init__(self, id, email, profile_picture=None):
        self.id = id
        self.email = email
        self.profile_picture = profile_picture

    # Método para cargar al usuario por ID
    @staticmethod
    def get(user_id):
        return User.query.get(user_id)


# Cargar el usuario desde la sesión
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# Ruta protegida (requiere autenticación)
@app.route('/profile')
@login_required
def profile():
    return "Hello, this is the profile page!"

# Middleware para crear o actualizar el usuario en la base de datos
@app.after_request
def create_or_update_user(response):
    if 'user' in session and 'user_email' in session['user']:
        email = session['user']['user_email']
        profile_picture = session['user'].get('photo_url')
        with app.app_context():
            user = User.query.filter_by(email=email).first()
            if not user:
                new_user = User(email=email, profile_picture=profile_picture)
                db.session.add(new_user)
                db.session.commit()
                logging.info(f"Created new user: {email}")
            elif user.profile_picture != profile_picture:
                user.profile_picture = profile_picture
                db.session.commit()
                logging.info(f"Updated profile picture for user: {email}")
    return response
