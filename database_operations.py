from models import db, User, Task
from datetime import datetime

def create_user(email, profile_picture=None):
    new_user = User(email=email, profile_picture=profile_picture)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return {
            'id': user.id,
            'email': user.email,
            'profile_picture': user.profile_picture
        }
    return None

def update_user_profile_picture(email, profile_picture):
    user = User.query.filter_by(email=email).first()
    if user:
        user.profile_picture = profile_picture
        db.session.commit()
        return True
    return False

def create_task(user_id, title, description=None, due_date=None):
    new_task = Task(
        title=title, 
        description=description, 
        user_id=user_id, 
        due_date=due_date
    )
    db.session.add(new_task)
    db.session.commit()
    return new_task

def get_user_tasks(user_id):
    return Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()

def update_task_status(task_id, is_completed):
    task = Task.query.get(task_id)
    if task:
        task.is_completed = is_completed
        db.session.commit()
        return True
    return False

def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return True
    return False