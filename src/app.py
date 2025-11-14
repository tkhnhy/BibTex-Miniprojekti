from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.reference_repository import get_references, create_reference, set_done, db_delete_reference
from config import app, test_env
from util import validate_reference

@app.route("/")
def index():
    references = get_references()
    unfinished = len([reference for reference in references])
    return render_template("index.html", references=references, unfinished=unfinished) 

@app.route("/new_reference")
def new():
    return render_template("new_reference.html")

@app.route("/create_reference", methods=["POST"])
def reference_creation():
    reference_type = request.form.get("reference_type")
    reference_key = request.form.get("reference_key")
    
    reference_data = { 
        key: value for key, value in request.form.items()
        if key not in ("reference_type", "reference_key") and value.strip() != ""
    }
    
    try:
        #validate_reference(content)
        create_reference(reference_type, reference_key, reference_data)
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return  redirect("/new_reference")

@app.route("/toggle_reference/<reference_id>", methods=["POST"])
def toggle_todo(reference_id):
    set_done(reference_id)
    return redirect("/")

@app.route("/confirm_delete/<reference_key>")
def confirm_delete(reference_key):
    references = get_references()
    reference = next((ref for ref in references if ref.reference_key == reference_key), None)
    if reference is None:
        flash("Reference not found.")
        return redirect("/")
    return render_template("delete_reference.html", reference=reference)

@app.route("/delete_reference/<reference_key>", methods=["POST"])
def delete_reference(reference_key):
    db_delete_reference(reference_key)
    return redirect("/")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
