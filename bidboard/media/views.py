from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from bidboard.media.forms import UploadForm, DeleteForm, EditCampaignForm
from bidboard.helpers.helpers import allowed_file, upload_file
from werkzeug.utils import secure_filename
from bidboard.media.model import Medium, db
from bidboard import clarifai
import random

media_blueprint = Blueprint('media',
                             __name__,
                             template_folder='templates')


@media_blueprint.route("<id>/new", methods=['GET'])
@login_required
def new(id):
    form = UploadForm()
    return render_template('media/upload.html', form=form)


@media_blueprint.route("<id>/upload", methods=['POST'])
@login_required
def upload(id):
    if int(id) == current_user.id:

        # check there is a file, campaign_name and description
        form = UploadForm()
        if "user_media" not in request.files or not form.campaign_name.data or not form.description.data:
            flash("All fields are required!")
            return render_template('media/upload.html', form=form)

        # grab the file, campaign_name and description
        file = request.files["user_media"]
        campaign_name = form.campaign_name.data
        description = form.description.data

        # check there is a name
        if file.filename == "":
            flash("Please give your file a valid name!")
            return render_template('media/upload.html', form=form)

        # check file size
        if len(file.read()) > (15 * 1024 * 1024):
            flash("Please upload a file smaller than 15 MB!")
            return render_template('media/upload.html', form=form)

        # check correct extension and upload if valid
        if file and allowed_file(file.filename):
            file.seek(0)
            serial_filename = f'{current_user.id}.{random.randint(1,100000)}.{file.filename}'
            file.filename = secure_filename(serial_filename)
            upload_file(file)

            new_medium = Medium(
                user_id=id,
                medium_name=str(file.filename),
                campaign_name=campaign_name,
                description=description
            )

            db.session.add(new_medium)
            db.session.commit()

            flash('Media uploaded successfully!')
            # change redirect destination later
            return redirect(url_for('home', id=current_user.id))
        else:
            flash('Upload a valid media format!')
            return render_template('media/upload.html', form=form)

    return redirect(url_for('home', id=current_user.id))
