from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SelectField, FieldList, FormField, Form, validators


class TilausForm(Form):
    """Subform.

    CSRF is disabled for this subform (using `Form` as parent class) because
    it is never used by itself.
    """
    orderCode = StringField('Runner name')

class TilausMainForm(FlaskForm):
    """Parent form."""
    osat = FieldList(
        FormField(TilausForm),
        min_entries=1,
        max_entries=20
    )