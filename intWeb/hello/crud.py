#from intWeb import get_hello_model,  storage, login_required_auth
from flask import flash,Blueprint, current_app, redirect, render_template, request, \
    session, url_for,send_file,Flask,send_from_directory
import os
import zipfile
import datetime
from urllib.parse import quote
from intWeb.hello.models import Todo,db
crud = Blueprint('crud', __name__)

@crud.route("/")
def show_all():
    return render_template(
        "hello/show_all.html", todos=Todo.query.order_by(Todo.pub_date.desc()).all()
    )

@crud.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        if not request.form["title"]:
            flash("Title is required", "error")
        elif not request.form["text"]:
            flash("Text is required", "error")
        else:
            todo = Todo(request.form["title"], request.form["text"])
            db.session.add(todo)
            db.session.commit()
            flash("Todo item was successfully created")
            return redirect(url_for("hello.show_all"))
    return render_template("hello/new.html")


@crud.route("/update", methods=["POST"])
def update_done():
    for todo in Todo.query.all():
        todo.done = f"done.{todo.id}" in request.form
    flash("Updated status")
    db.session.commit()
    return redirect(url_for("hello.show_all"))

