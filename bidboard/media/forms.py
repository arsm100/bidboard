from flask_wtf import FlaskForm
from flask_wtf.csrf import CsrfProtect
from wtforms import FileField, PasswordField, SubmitField


class UploadForm(FlaskForm):
    user_media = FileField('User Media')
    submit = SubmitField('Submit')


class DeleteForm(FlaskForm):
    submit = SubmitField('Submit')
