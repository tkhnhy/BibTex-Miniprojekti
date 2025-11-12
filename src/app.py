from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.todo_repository import get_todos, create_todo, set_done
from config import app, test_env
from util import validate_todo

@app.route("/")
def index():
    todos = get_todos()
    unfinished = len([todo for todo in todos])
    return render_template("index.html", todos=todos, unfinished=unfinished) 

@app.route("/new_todo")
def new():
    return render_template("new_todo.html")

@app.route("/create_todo", methods=["POST"])
def todo_creation():
    citation_type = request.form.get("citation_type")
    citation_key = request.form.get("citation_key")
    data = request.form.get("data")
    try:
        #validate_todo(content)
        create_todo(citation_type, citation_key, data)
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return  redirect("/new_todo")

@app.route("/toggle_todo/<todo_id>", methods=["POST"])
def toggle_todo(todo_id):
    set_done(todo_id)
    return redirect("/")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
