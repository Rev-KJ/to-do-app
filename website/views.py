from flask import Blueprint, redirect, render_template, url_for, request
from .models import Todo
from . import db
from datetime import datetime

my_view = Blueprint("my_view", __name__)

@my_view.route("/")
def home():
    todo_list = Todo.query.all()
    message = request.args.get('message', None)
    return render_template("index.html", todo_list=todo_list, message = message)

@my_view.route("/add", methods=["POST"])
def add():
    try:
        task = request.form.get("task")
        existing_todo = Todo.query.filter_by(task=task).first()
        if existing_todo:
            message = "Task already exists."
            return redirect(url_for("my_view.home", message=message))
        new_todo = Todo(task=task)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("my_view.home"))
    except:
        message = "There was an error adding your task. Please try again"
        return redirect(url_for("my_view.home", message=message))

@my_view.route("/update/<todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("my_view.home"))

@my_view.route("/delete/<todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("my_view.home"))

@my_view.route('/')
def index():
    datetime_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('index.html', datetime=datetime_str)

@my_view.route("/edit/<int:todo_id>", methods=["GET", "POST"])
def edit_task(todo_id):
    if request.method == "GET":
        todo = Todo.query.get(todo_id)
        if todo:
            return render_template("edit_task.html", todo=todo)
        else:
            return "Task not found", 404
    elif request.method == "POST":
        todo = Todo.query.get(todo_id)
        if todo:
            new_task_content = request.form.get("task")
            existing_task = Todo.query.filter_by(task=new_task_content).first()
            if existing_task and existing_task.id != todo_id:
                return "Task already exists with the same content, please return to the previous page and try again", 400
            todo.task = new_task_content
            db.session.commit()
            return redirect(url_for("my_view.home"))
        else:
            return "Task not found", 404

