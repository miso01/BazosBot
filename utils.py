import re
from flask import flash


def get_category_text_from_category_section_value(bazos_http, section_value, category_value):
    """ We don't have access to <option> text, so in order to get category text
        we have to download categories again and choose value according to the
        section and category value"""
    fetched_categories = bazos_http.fetch_bazos_categories(section_value)
    category_list_tuple = [item for item in fetched_categories if item[0] == category_value]
    return category_list_tuple[0][1]


def flash_forms_errors(form):
    for fld, msg in form.errors.items():
        print("fild je " + str(fld) + " a msg je " + str(msg))
        flash(message=msg)


def get_number_between_forward_slashes(text):
    m = re.search(r'/(\d+)/', text)
    return m.group(1)
