import os
from bidboard import S3_KEY, S3_SECRET, S3_BUCKET
import boto3
import botocore
from flask import redirect, url_for


# user details validation helper
def validation_preparation(func):
    def wrapper(obj, key, value):
        try:
            obj.validation_errors
        except AttributeError:
            obj.validation_errors = []
        return func(obj, key, value)

    return wrapper


# Image upload helpers
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'tiff', 'gif', 'avi', 'mp4', 'mov'])
image_extensions = set(['png', 'jpg', 'jpeg', 'tiff', 'gif'])
video_extensions = set(['avi', 'mp4', 'mov'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


s3 = boto3.client(
    's3',
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)


def upload_file(file, bucket_name=S3_BUCKET, acl="public-read"):
    # Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        # This is to catch all exception
        print(e)
        return redirect(url_for('home'))  # change redirect destination later


def delete_file(file_name):
    s3.delete_object(
        Bucket=S3_BUCKET,
        Key=file_name)
