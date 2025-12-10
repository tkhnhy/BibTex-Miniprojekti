import io
from flask import redirect, render_template, request, jsonify, flash, send_file
from db_helper import reset_db
from entities.reference import COMMON_BIBTEX_FIELDS, ReferenceType, Reference
from repositories.reference_repository import (
    get_references, create_reference, get_reference_by_key,
    add_ref_for_storytests, get_references_by_keys, get_filtered_references,
    delete_reference, delete_references, update_reference
)
from repositories.tag_repository import get_tags_with_counts, delete_tag, rename_tag
from config import app, test_env
from util import validate_reference, fetch_doi_bibtex, extract_doi, UserInputError

@app.route("/", methods=["GET"])
def route_index():
    # The filter is a list of tuples in format: (filter type, list of filter values).
    filters = []
    selected_types = request.args.getlist("reference_type[]")
    selected_tags = request.args.getlist("tag[]")
    print(request.args)
    selected_field = request.args.get("keyword_field")
    allowed_search_fields = {"any", "author", "title", "publisher", "year", "key"}
    if selected_field and selected_field not in allowed_search_fields:
        selected_field = None
    selected_keyword = request.args.get("keyword_value", "").strip() or None

    sort_by = request.args.get("sort_by")

    if selected_types:
        filters.append(("type", selected_types))
    if selected_tags:
        filters.append(("tag", selected_tags))
    if selected_keyword and selected_field:
        filters.append(("keyword", (selected_field, selected_keyword)))
    try:
        if not filters:
            references = get_references(sort_by)
        else:
            references = get_filtered_references(filters, sort_by)
        tags = get_tags_with_counts()
    except Exception as error:
        flash("Could not fetch references: " + str(error))
        references = []
        tags = []

    return render_template("index.html", references=references,
                            reference_types=list(ReferenceType), tags=tags,
                            sort_selected=sort_by)

@app.route("/new_reference")
def route_new_reference():
    field_requirements_map = {ref_type.value: ref_type.field_requirements() for ref_type in list(ReferenceType)}

    return render_template(
        "new_reference.html",
        reference_types=list(ReferenceType),
        reference_fields=COMMON_BIBTEX_FIELDS,
        field_requirements_map=field_requirements_map
    )

@app.route("/fetch_doi", methods=["POST"])
def route_fetch_doi():
    """
    Fetch endpoint for getting BibTeX data for a given DOI.
    Returns a JSON response with the BibTeX data or an error message.
    """
    payload = request.get_json(silent=True) or request.form
    raw = (payload.get("doi") or payload.get("DOI") or "").strip()
    doi = extract_doi(raw)

    if not doi:
        return jsonify({"error": "Missing DOI"}), 400

    bibtex = fetch_doi_bibtex(doi)
    if bibtex is None:
        return jsonify({"error": "Could not fetch BibTeX for DOI"}), 502

    try:
        reference = Reference.from_bibtex(0, bibtex)
    except ValueError:
        return jsonify({"error": "Fetched BibTeX is invalid"}), 502

    return jsonify({"type": reference.type.value, "key": reference.key, "content": reference.content}), 200

@app.route("/create_reference", methods=["POST"])
def route_reference_creation():
    reference_type = request.form.get("reference_type")
    # print("reference_type:", reference_type)
    reference_key = request.form.get("reference_key")
    tags = request.form.getlist("tags")
    reference_data = {
        key: value for key, value in request.form.items()
        if key not in ("reference_type", "reference_key", "comment", "tags") and value.strip() != ""
    }
    comment = request.form.get("comment", "").strip()
    try:
        validate_reference(reference_type, reference_key, reference_data)
        create_reference(reference_type, reference_key, reference_data, tags, comment)
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

@app.route("/confirm_delete_selected", methods=["POST"])
def route_confirm_delete_selected():
    selected_keys = request.form.getlist('selected_keys')
    if not selected_keys:
        flash("No references selected.")
        return redirect("/")

    try:
        references = get_references_by_keys(selected_keys)
        if not references:
            flash("No valid references selected for deletion.")
            return redirect("/")
    except Exception as error:
        flash("Could not fetch references: " + str(error))
        return redirect("/")

    return render_template("confirm_delete_selected.html", references=references)

@app.route("/delete_reference/<string:reference_key>", methods=["POST"])
def route_delete_reference(reference_key):
    try:
        delete_reference(reference_key)
    except Exception as error:
        flash(f"Error deleting reference: {error}")
    return redirect("/")

@app.route("/delete_selected", methods=["POST"])
def route_delete_selected():
    selected_keys = request.form.getlist('selected_keys')
    if not selected_keys:
        flash("No references selected.")
        return redirect("/")
    try:
        references = get_references_by_keys(selected_keys)
        if not references:
            flash("No valid references selected for deletion.")
        else:
            valid_keys = [ref.key for ref in references]
            delete_references(valid_keys)
            flash(f"Successfully deleted {len(valid_keys)} reference(s).")
    except Exception as error:
        flash(f"Error deleting references: {error}")
    return redirect("/")

@app.route("/edit_reference/<string:reference_key>")
def route_edit_reference(reference_key: str):
    reference = get_reference_by_key(reference_key)
    tags = get_tags_with_counts()
    field_requirements_map = {ref_type.value: ref_type.field_requirements() for ref_type in list(ReferenceType)}
    if reference is None:
        flash("Reference to be edited not found.")
        return redirect("/")
    return render_template("edit_reference.html", reference=reference,
                           reference_types=list(ReferenceType),
                           reference_fields=COMMON_BIBTEX_FIELDS,
                           field_requirements_map=field_requirements_map,
                           tags=tags)

@app.route("/save_edited_reference/<string:old_reference_key>", methods=["POST"])
def route_save_edited_reference(old_reference_key: str):
    reference_type = request.form.get("reference_type")
    new_reference_key = request.form.get("reference_key")
    tags = request.form.getlist("tags")
    reference_data = {
        key: value for key, value in request.form.items()
        if key not in ("reference_type", "reference_key", "comment", "tags") and value.strip() != ""
    }
    comment = request.form.get("comment", "").strip()

    try:
        validate_reference(reference_type, new_reference_key, reference_data, old_key=old_reference_key)
        update_reference(reference_type, old_reference_key, new_reference_key, reference_data, tags, comment)
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

@app.route("/upload_bib", methods=["POST"])
def upload_bib():
    if 'file' not in request.files:
        flash("No file part in the request.")
        return redirect("/")

    file = request.files['file']
    if file.filename == '':
        flash("No selected file.")
        return redirect("/")

    if not file:
        return redirect("/")

    try:
        content = file.read().decode("utf-8")
        entries = content.split("\n@")

        for i, entry in enumerate(entries):
            if i > 0:
                entry = "@" + entry
            reference = Reference.from_bibtex(i, entry)
            if reference:
                create_reference(
                    reference.type.value,
                    reference.key,
                    reference.content,
                    tags=[],
                    comment=reference.comment
                )
        flash("File uploaded and references imported successfully.")
    except Exception as error:
        flash(f"Error processing file: {error}")

    return redirect("/")

@app.route("/tag_management")
def route_tag_management():
    tags = get_tags_with_counts()
    return render_template("tag_management.html", tags=tags)

@app.route("/delete_tag/<string:tag_name>", methods=["POST"])
def route_delete_tag(tag_name: str):
    try:
        delete_tag(tag_name)
    except Exception as error:
        flash(f"Error deleting tag: {error}")
    return redirect("/tag_management")

@app.route("/rename_tag/<string:old_tag_name>", methods=["POST"])
def route_rename_tag(old_tag_name: str):
    new_tag_name = request.form.get("new_tag_name", "").strip()
    if not new_tag_name:
        flash("New tag name cannot be empty.")
        return redirect("/tag_management")
    try:
        rename_tag(old_tag_name, new_tag_name)
    except Exception as error:
        flash(f"Error renaming tag: {error}")
    return redirect("/tag_management")


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
