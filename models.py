from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Inicializa la base de datos
db = SQLAlchemy()

# Definición del modelo de usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    profile_picture = db.Column(db.String(255))
    tasks = db.relationship('Task', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

# Definición del modelo de tarea
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.title}>'
