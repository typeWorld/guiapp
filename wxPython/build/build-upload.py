import sys
from google.cloud import storage

version = sys.argv[-1]
platform = sys.argv[-1]
ending = "dmg" if platform == "mac" else "exe"

storage_client = storage.Client()
bucket = storage_client.bucket("typeworld2")
blob = bucket.blob(f"downloads/guiapp/TypeWorldApp.{version}.{ending}")
blob.upload_from_filename(filename=f"dmg/TypeWorldApp.{version}.{ending}")
