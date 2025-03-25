# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con las tareas (un usuario puede tener muchas tareas)
    tasks = db.relationship('Task', backref='owner', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.Integer, default=1)  # 1=Baja, 2=Media, 3=Alta

    # Clave foránea para relacionar con el usuario
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    # Clave foránea para relacionar con la categoría (lo implementaremos después)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

    def __repr__(self):
        return f'<Task {self.title}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(7), default="#ffffff")  # Color en formato hexadecimal

    # Relación con las tareas (una categoría puede tener muchas tareas)
    tasks = db.relationship('Task', backref='category', lazy='dynamic')
    # Clave foránea para relacionar con el usuario
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f'<Category {self.name}>'
