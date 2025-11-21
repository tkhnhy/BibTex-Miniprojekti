from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from entities.reference import ReferenceType
from repositories.reference_repository import get_references, create_reference, get_reference_by_key, delete_reference
from config import app, test_env
from util import validate_reference, UserInputError

@app.route("/")
def route_index():
    references = get_references()
    amount = len(references)
    return render_template("index.html", references=references, amount=amount)

@app.route("/new_reference")
def route_new_reference():
    return render_template("new_reference.html", reference_types=list(ReferenceType))

@app.route("/create_reference", methods=["POST"])
def route_reference_creation():
    reference_type = request.form.get("reference_type")
    reference_key = request.form.get("reference_key")
    reference_data = {
        key: value for key, value in request.form.items()
        if key not in ("reference_type", "reference_key") and value.strip() != ""
    }

    try:
        validate_reference(reference_type, reference_key, reference_data)
        create_reference(reference_type, reference_key, reference_data)
        return redirect("/")
    except UserInputError as error:
        flash(str(error))
        return redirect("/new_reference")

@app.route("/confirm_delete/<string:reference_key>")
def route_confirm_delete(reference_key: str):
    reference = get_reference_by_key(reference_key)
    if reference is None:
        flash("Reference to be deleted not found.")
        return redirect("/")
    return render_template("delete_reference.html", reference=reference)

@app.route("/delete_reference/<string:reference_key>", methods=["POST"])
def route_delete_reference(reference_key):
    delete_reference(reference_key)
    return redirect("/")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def route_reset_db():
        reset_db()
        return jsonify({ 'message': "db reset" })
