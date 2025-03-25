# app_init.py
import logging
from flask import Flask, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, UserMixin
from flask_migrate import Migrate
from models import db, User

def create_app():
    # Configurar la aplicación Flask
    app = Flask(__name__, static_folder='static')
    app.secret_key = 'supersecretkey'  # Considera usar una clave más segura en producción
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensiones
    db.init_app(app)
    migrate = Migrate(app, db)

    # Configuración de logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Inicializar LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # Actualizado para usar el blueprint
    login_manager.login_message = "Por favor inicia sesión para acceder a esta página."

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

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

    # Registrar blueprints
    with app.app_context():
        # Importar rutas después de inicializar Flask
        from routes import routes as routes_blueprint
        app.register_blueprint(routes_blueprint)

        # Registrar blueprint de autenticación
        from auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

    return app

# Esta parte se mueve a main.py
# if __name__ == "__main__":
#     app = create_app()
#     app.run(host="0.0.0.0", port=8080, debug=True)
