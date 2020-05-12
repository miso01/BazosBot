from flask import flash


def flash_forms_errors(form):
    for fld, msg in form.errors.items():
        flash(category=fld, message=msg)
