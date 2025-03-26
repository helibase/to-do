# init_db.py
from app_init import create_app
from models import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Base de datos creada exitosamente.")
