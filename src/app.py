import io
from flask import redirect, render_template, request, jsonify, flash, send_file
from db_helper import reset_db
from entities.reference import COMMON_BIBTEX_FIELDS, ReferenceType
from repositories.reference_repository import get_references, create_reference, get_reference_by_key, \
    add_ref_for_storytests, get_references_by_keys
from repositories.reference_repository import delete_reference, update_reference
from config import app, test_env
from util import validate_reference, UserInputError

@app.route("/")
def route_index():
    try:
        references = get_references()
        amount = len(references)
    except Exception as error:
        flash("Could not fetch references: " + str(error))
        references = []
        amount = 0

    return render_template("index.html", references=references, amount=amount)

@app.route("/new_reference")
def route_new_reference():
    field_requirements_map = {ref_type.value: ref_type.field_requirements() for ref_type in list(ReferenceType)}

    return render_template(
        "new_reference.html",
        reference_types=list(ReferenceType),
        reference_fields=COMMON_BIBTEX_FIELDS,
        field_requirements_map=field_requirements_map
    )

@app.route("/create_reference", methods=["POST"])
def route_reference_creation():
    reference_type = request.form.get("reference_type")
    reference_key = request.form.get("reference_key")
    reference_data = {
        key: value for key, value in request.form.items()
        if key not in ("reference_type", "reference_key", "comment") and value.strip() != ""
    }
    comment = request.form.get("comment", "").strip()
    try:
        validate_reference(reference_type, reference_key, reference_data)
        create_reference(reference_type, reference_key, reference_data, comment)
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
    try:
        delete_reference(reference_key)
    except Exception as error:
        flash(f"Error deleting reference: {error}")
    return redirect("/")

@app.route("/edit_reference/<string:reference_key>")
def route_edit_reference(reference_key: str):
    reference = get_reference_by_key(reference_key)
    field_requirements_map = {ref_type.value: ref_type.field_requirements() for ref_type in list(ReferenceType)}
    if reference is None:
        flash("Reference to be edited not found.")
        return redirect("/")
    return render_template("edit_reference.html", reference=reference,
                           reference_types=list(ReferenceType),
                           reference_fields=COMMON_BIBTEX_FIELDS,
                           field_requirements_map=field_requirements_map)

@app.route("/save_edited_reference/<string:old_reference_key>", methods=["POST"])
def route_save_edited_reference(old_reference_key: str):
    reference_type = request.form.get("reference_type")
    new_reference_key = request.form.get("reference_key")
    reference_data = {
        key: value for key, value in request.form.items()
        if key not in ("reference_type", "reference_key", "comment") and value.strip() != ""
    }
    comment = request.form.get("comment", "").strip()

    try:
        validate_reference(reference_type, new_reference_key, reference_data, old_key=old_reference_key)
        update_reference(reference_type, old_reference_key, new_reference_key, reference_data, comment)
        return redirect("/")
    except UserInputError as error:
        flash(str(error))
        return redirect(f"/edit_reference/{old_reference_key}")
    except Exception as error:
        flash(f"Error updating reference: {error}")
        return redirect(f"/edit_reference/{old_reference_key}")

@app.route("/download_bib", methods=["POST"])
def download_bib():
    selected_keys = request.form.getlist('selected_keys')
    try:
        if not selected_keys:
            # Default to all references if none selected
            references = get_references()
        else:
            references = get_references_by_keys(selected_keys)
    except Exception as error:
        flash("Could not fetch references: " + str(error))
        return redirect("/")

    bibtex_content = "\n\n".join(str(r) for r in references)

    #Turn the bibtex_content string into a file-like object, so it can be sent.
    buffer = io.BytesIO()
    buffer.write(bibtex_content.encode("utf-8"))
    buffer.seek(0)

    #Flasks own send_file function, save pop-up and location depends on browser settings.
    return send_file(
        buffer,
        as_attachment=True,
        download_name="references.bib",
        mimetype="application/x-bibtex"
    )

# Routes for testing
if test_env:
    @app.route("/reset_db")
    def route_reset_db():
        reset_db()
        return jsonify({ 'message': "db reset" })

    @app.route("/reference_for_storytest")
    def reference_for_storytest():
        add_ref_for_storytests()
        return redirect("/")
