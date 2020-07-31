import os, sys

version = sys.argv[-1]

# Google Cloud Storage
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'typeworld2-559c851e351b.json'
from google.cloud import storage
storage_client = storage.Client()
bucket = storage_client.bucket('typeworld2')
blobPath = f'downloads/guiapp/TypeWorldApp.{version}.dmg'
blob = bucket.get_blob(blobPath)
if blob:
    print(f'File {blobPath} already exists in Cloud Storage. WARNING: This should have been checked in the beginning of the build process already. If you see this at the end of the build process, this should mean that someone else has uploaded that file in the meantime.')
    sys.exit(1)
