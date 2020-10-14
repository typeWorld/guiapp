import os
import sys
from google.cloud import storage

version = sys.argv[-2]
platform = sys.argv[-1]
ending = "dmg" if platform == "mac" else "exe"

# Google Cloud Storage
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "typeworld2-559c851e351b.json"

storage_client = storage.Client()
bucket = storage_client.bucket("typeworld2")
blobPath = f"downloads/guiapp/TypeWorldApp.{version}.{ending}"
blob = bucket.get_blob(blobPath)
if blob:
    print(f"File {blobPath} already exists in Cloud Storage.")
    sys.exit(1)
