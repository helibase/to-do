from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from models import db, Task, Category, User
from datetime import datetime
import logging

# Configuración de logging
logger = logging.getLogger(__name__)

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template('home.html')

@routes.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_route():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'create_task':
            title = request.form.get('title')
            description = request.form.get('description')
            due_date_str = request.form.get('due_date')

            due_date = None
            if due_date_str:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d')

            task = Task(
                title=title,
                description=description,
                due_date=due_date,
                user_id=current_user.id
            )

            db.session.add(task)
            db.session.commit()
            logger.info(f"Tarea creada por usuario {current_user.email}: {title}")
            flash('Tarea creada exitosamente!')

        elif action == 'update_task_status':
            task_id = request.form.get('task_id')
            is_completed = request.form.get('is_completed') == 'true'

            task = Task.query.get_or_404(task_id)
            if task.user_id == current_user.id:
                task.completed = is_completed
                db.session.commit()
                logger.info(f"Estado de tarea {task_id} actualizado por usuario {current_user.email}")
                flash('Estado de la tarea actualizado!')
            else:
                logger.warning(f"Intento de actualizar tarea {task_id} por usuario no autorizado {current_user.email}")
                flash('No tienes permiso para modificar esta tarea.')

        elif action == 'delete_task':
            task_id = request.form.get('task_id')

            task = Task.query.get_or_404(task_id)
            if task.user_id == current_user.id:
                db.session.delete(task)
                db.session.commit()
                logger.info(f"Tarea {task_id} eliminada por usuario {current_user.email}")
                flash('Tarea eliminada exitosamente!')
            else:
                logger.warning(f"Intento de eliminar tarea {task_id} por usuario no autorizado {current_user.email}")
                flash('No tienes permiso para eliminar esta tarea.')

        return redirect(url_for('routes.profile_route'))

    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.due_date.asc()).all()
    return render_template('profile.html', tasks=tasks)

# Ruta para categorías (opcional, para implementar más adelante)
@routes.route('/categories', methods=['GET'])
@login_required
def list_categories():
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('categories/index.html', categories=categories)

@routes.route('/categories/new', methods=['GET', 'POST'])
@login_required
def new_category():
    if request.method == 'POST':
        name = request.form.get('name')
        color = request.form.get('color', '#ffffff')

        if not name:
            flash('El nombre de la categoría es obligatorio.')
            return redirect(url_for('routes.new_category'))

        category = Category(name=name, color=color, user_id=current_user.id)

        db.session.add(category)
        db.session.commit()
        logger.info(f"Categoría creada por usuario {current_user.email}: {name}")
        flash('¡Categoría creada exitosamente!')
        return redirect(url_for('routes.list_categories'))

    return render_template('categories/new.html')
