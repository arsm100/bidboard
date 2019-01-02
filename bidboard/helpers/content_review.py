from bidboard.helpers.helpers import image_extensions
from bidboard import db, workflow, moderation_model, ClImage, ClVideo


def review_media(new_medium):
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

        new_medium.concepts = final_concepts
        db.session.add(new_medium)
        db.session.commit()

        moderation = new_medium.concepts['moderation']
        illegal = new_medium.concepts['illegal']
        if new_medium.concepts['nsfw-v1.0']['nsfw'] < 0.5 \
                and moderation['gore']+moderation['explicit']+moderation['drug'] < 0.5\
                and illegal['smoking']+illegal['cigs']+illegal['guns']+illegal['weapons'] < 0.5:
            new_medium.is_approved = True
            db.session.add(new_medium)
            db.session.commit()

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

        video_frames = list(new_medium.concepts.items())
        new_medium.is_approved = True
        for video_frame in video_frames:
            if video_frame[1]['gore'] + video_frame[1]['drug'] + video_frame[1]['explicit'] > 0.5:
                new_medium.is_approved = False
                break

        db.session.add(new_medium)
        db.session.commit()
