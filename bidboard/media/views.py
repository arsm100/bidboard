from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from bidboard.media.forms import UploadForm, DeleteForm, EditCampaignForm
from bidboard.helpers.helpers import allowed_file, upload_file, image_extensions, video_extensions
from werkzeug.utils import secure_filename
from bidboard.media.model import Medium, db
from bidboard import clarifai, workflow, ClImage, ClVideo, general_model, nsfw_model, moderation_model
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
            flash('Media uploaded successfully and content review is in progress!')

            if new_medium.medium_name.rsplit('.', 1)[1] in image_extensions:
                content_review = workflow.predict(
                    [ClImage(url=new_medium.medium_url)])
                outputs = content_review['results'][0]['outputs']
                final_concepts = {}
                for output in outputs:
                    concepts = output['data']['concepts']
                    final_concepts[output['model']['name']] = {}
                    for concept in concepts:
                        final_concepts[output['model']['name']
                                       ][concept['name']] = concept['value']

            else:
                content_review = moderation_model.predict(
                    [ClVideo(url=new_medium.medium_url)])
                frames = content_review['outputs'][0]['data']['frames']
                final_concepts = {}
                for frame in frames:
                    concepts = frame['data']['concepts']
                    final_concepts[frame['frame_info']['index']] = {}
                    for concept in concepts:
                        final_concepts[frame['frame_info']['index']
                                       ][concept['name']] = concept['value']

            new_medium.concepts = final_concepts
            db.session.add(new_medium)
            db.session.commit()

            moderation = new_medium.concepts['moderation']
            if new_medium.concepts['nsfw-v1.0']['nsfw'] < 0.3 and moderation['gore']+moderation['explicit']+moderation['drug'] < 0.3:
                new_medium.is_approved = True
                db.session.add(new_medium)
                db.session.commit()

            # change redirect destination later
            return redirect(url_for('home', id=current_user.id))
        else:
            flash('Upload a valid media format!')
            return render_template('media/upload.html', form=form)

    return redirect(url_for('home', id=current_user.id))
