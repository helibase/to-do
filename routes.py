from flask import render_template, session, redirect, url_for, make_response, request
from functools import wraps
from app_init import app
from database_operations import create_task, get_user_tasks, update_task_status, delete_task

def with_sidebar(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return render_template(f.__name__.replace('_route', '.html'), with_sidebar=True)
    return decorated_function

@app.route("/")
def home_route():
    return render_template("home.html", with_sidebar=False)

@app.route("/profile", methods=['GET', 'POST'])
def profile_route():
    if 'user' not in session:
        return redirect(url_for('home_route'))
    
    user_email = session['user']['user_email']
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'create_task':
            title = request.form.get('title')
            description = request.form.get('description')
            due_date_str = request.form.get('due_date')
            
            from database_operations import get_user_by_email
            user = get_user_by_email(user_email)
            
            if user:
                from datetime import datetime
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
                create_task(user['id'], title, description, due_date)
        
        elif action == 'update_task_status':
            task_id = request.form.get('task_id')
            is_completed = request.form.get('is_completed') == 'true'
            update_task_status(task_id, is_completed)
        
        elif action == 'delete_task':
            task_id = request.form.get('task_id')
            delete_task(task_id)
        
        return redirect(url_for('profile_route'))
    
    from database_operations import get_user_by_email
    user = get_user_by_email(user_email)
    tasks = get_user_tasks(user['id']) if user else []
    
    return render_template("profile.html", with_sidebar=True, tasks=tasks)

@app.route("/logout", methods=['POST'])
def logout_route():
    session.clear()
    return redirect(url_for('home_route'))