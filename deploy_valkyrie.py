import boto3, os
from zipfile import ZipFile, ZIP_DEFLATED
from itertools import dropwhile
from io import BytesIO

# Create zip file of the files to be deployed
print('Creating zip')

zip_stream = BytesIO()
zip = ZipFile(zip_stream, mode='w', compression=ZIP_DEFLATED)

for root, dirs, files in os.walk('Deployable'):
    arc_root = ''.join(dropwhile(str.isalnum, root))
    if len(arc_root) > 0:
        arc_root = arc_root[1:]

    for filename in files:
        zip.write(filename=os.path.join(root, filename), arcname=os.path.join(arc_root, filename))

zip.close()
zip_stream.seek(0)

# Create s3 client
print('Creating S3 client')
s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ['aws-access-key'],
    aws_secret_access_key=os.environ['aws-secret-access-key']
)

print('Uploading zip')
s3.upload_fileobj(zip_stream, os.environ['aws-deploy-bucket'], 'latest.zip')