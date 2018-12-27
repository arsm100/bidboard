from flask_wtf import FlaskForm
from flask_wtf.csrf import CsrfProtect
from wtforms import FileField, StringField, TextAreaField, PasswordField, SubmitField


class UploadForm(FlaskForm):
    user_media = FileField('User Media')
    campaign_name = StringField('Campaign Name')
    description = TextAreaField('Description')
    submit = SubmitField('Submit')


class EditCampaignForm(FlaskForm):
    campaign_name = StringField('Campaign Name')
    description = TextAreaField('Description')
    submit = SubmitField('Submit')


class DeleteForm(FlaskForm):
    submit = SubmitField('Submit')
