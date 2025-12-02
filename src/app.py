import io
from flask import redirect, render_template, request, jsonify, flash, send_file
from db_helper import reset_db
from entities.reference import COMMON_BIBTEX_FIELDS, ReferenceType, Reference
from repositories.reference_repository import get_references, create_reference, get_reference_by_key, \
    add_ref_for_storytests, get_references_by_keys, get_filtered_references
from repositories.reference_repository import delete_reference, update_reference
from repositories.tag_repository import get_tags_with_counts
from config import app, test_env
from util import validate_reference, UserInputError

@app.route("/", methods=["GET", "POST"])
def route_index():
    """
    Displays the main page with a list of all references, optionally filtered by type or tag.

    This route extracts filter parameters from the query string (reference_type[] and tag[]) via
    request.args.getlist(). If filters are present, it retrieves filtered references from the
    database; otherwise, it fetches all references. The route also loads all existing tags with
    their usage counts for display in the filter sidebar.

    Returns:
        Rendered index.html template with the references list, available reference types, and tags.
    """
    # The filter is a list of tuples in format: (filter type, list of filter values).
    filters = []
    selected_types = request.args.getlist("reference_type[]")
    selected_tags = request.args.getlist("tag[]")
    if selected_types:
        filters.append(("type", selected_types))
    if selected_tags:
        filters.append(("tag", selected_tags))

    try:
        if not filters:
            references = get_references()
        else:
            references = get_filtered_references(filters)
        tags = get_tags_with_counts()
    except Exception as error:
        flash("Could not fetch references: " + str(error))
        references = []
        tags = []

    return render_template("index.html", references=references,
                            reference_types=list(ReferenceType), tags=tags)

@app.route("/new_reference")
def route_new_reference():
    """
    Displays the form for creating a new bibliographic reference.

    This route prepares and passes to the template all necessary data for reference creation:
    available reference types (e.g., article, book), common BibTeX fields, and a mapping of
    field requirements for each reference type. This allows the frontend to dynamically show
    which fields are required based on the selected reference type.

    Returns:
        Rendered new_reference.html template with reference types, fields, and field requirements.
    """
    field_requirements_map = {ref_type.value: ref_type.field_requirements() for ref_type in list(ReferenceType)}

    return render_template(
        "new_reference.html",
        reference_types=list(ReferenceType),
        reference_fields=COMMON_BIBTEX_FIELDS,
        field_requirements_map=field_requirements_map
    )

@app.route("/create_reference", methods=["POST"])
def route_reference_creation():
    """
    Handles the creation of a new bibliographic reference from form data.

    This route receives form data via request.form containing: reference_type, reference_key,
    optional tags (as a list), comment, and all other BibTeX fields (author, title, etc.).
    It extracts and validates this data, then creates a new reference in the database. If
    validation fails (e.g., duplicate key, missing required fields), a flash message is shown
    and the user is redirected back to the creation form.

    Returns:
        Redirect to the main index page on success, or back to the new_reference form on error.
    """
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
    """
    Displays a confirmation page before deleting a reference.

    This route receives the reference_key as a URL path parameter, fetches the corresponding
    reference from the database, and displays a confirmation page showing the reference details.
    If the reference is not found, a flash message is shown and the user is redirected to the
    main index page.

    Args:
        reference_key: The unique citation key of the reference to be deleted.

    Returns:
        Rendered delete_reference.html template with reference details, or redirect to index.
    """
    reference = get_reference_by_key(reference_key)
    if reference is None:
        flash("Reference to be deleted not found.")
        return redirect("/")
    return render_template("delete_reference.html", reference=reference)

@app.route("/delete_reference/<string:reference_key>", methods=["POST"])
def route_delete_reference(reference_key: str):
    """
    Deletes a reference from the database.

    This route receives the reference_key as a URL path parameter from a form POST request
    (typically submitted from the delete confirmation page). It calls the repository function
    to delete the reference and its associated tag links from the database, then redirects
    back to the main index page. Any errors during deletion are shown as flash messages.

    Args:
        reference_key: The unique citation key of the reference to delete.

    Returns:
        Redirect to the main index page.
    """
    try:
        delete_reference(reference_key)
    except Exception as error:
        flash(f"Error deleting reference: {error}")
    return redirect("/")

@app.route("/edit_reference/<string:reference_key>")
def route_edit_reference(reference_key: str):
    """
    Displays the form for editing an existing reference.

    This route receives the reference_key as a URL path parameter, fetches the reference and
    its current data from the database, and displays an edit form pre-populated with the
    existing values. It also loads available tags, reference types, common BibTeX fields, and
    field requirements for the template. If the reference is not found, a flash message is
    shown and the user is redirected to the main index.

    Args:
        reference_key: The unique citation key of the reference to edit.

    Returns:
        Rendered edit_reference.html template with reference data and form options.
    """
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
    """
    Saves changes to an existing reference.

    This route receives the old_reference_key as a URL path parameter (to identify the original
    reference) and new data via request.form: reference_type, reference_key (which may be changed),
    tags list, comment, and all BibTeX fields. It validates the new data and updates the reference
    in the database, including updating the reference-tag associations. On validation or database
    errors, flash messages are shown and the user is redirected back to the edit form.

    Args:
        old_reference_key: The original citation key of the reference being edited.

    Returns:
        Redirect to the main index page on success, or back to the edit form on error.
    """
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
    """
    Downloads selected references as a BibTeX file.

    This route receives a list of reference keys via request.form.getlist('selected_keys') from
    checkboxes on the main page. If no keys are selected, all references are exported. The
    selected references are fetched from the database, converted to BibTeX format strings, and
    combined into a single .bib file. The file is sent to the browser as a downloadable attachment.

    Returns:
        A downloadable references.bib file, or redirect to index on error.
    """
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
    """
    Uploads and imports references from a BibTeX file.

    This route receives a file upload via request.files['file'] from a file input on the main
    page. It validates that a file was selected, then resets the database and parses the uploaded
    .bib file content. Each BibTeX entry is parsed using Reference.from_bibtex() and saved to
    the database via create_reference(). On success or failure, appropriate flash messages are
    displayed and the user is redirected to the main index page.

    Returns:
        Redirect to the main index page.
    """
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
        reset_db()
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

# Routes for testing
if test_env:
    @app.route("/reset_db")
    def route_reset_db():
        """
        Resets the database to its initial empty state (test environment only).

        This route is only available when the TEST_ENV environment variable is set to true.
        It calls reset_db() to drop and recreate all database tables, clearing all data.
        Used by automated tests to ensure a clean state before each test run.

        Returns:
            JSON response with a message confirming the database was reset.
        """
        reset_db()
        return jsonify({ 'message': "db reset" })

    @app.route("/reference_for_storytest")
    def reference_for_storytest():
        """
        Creates a predefined test reference for story tests (test environment only).

        This route is only available when the TEST_ENV environment variable is set to true.
        It bypasses the frontend form and directly creates a sample book reference in the
        database using add_ref_for_storytests(). This allows Robot Framework story tests
        to set up test data without going through the UI.

        Returns:
            Redirect to the main index page.
        """
        add_ref_for_storytests()
        return redirect("/")
