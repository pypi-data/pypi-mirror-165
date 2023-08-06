"""
Functions for interacting with GCP cloud storage
"""
#####################################################
#           Imports                                 #
#####################################################

# import os
from google.cloud import storage
# import logging

#####################################################
#           Classes                                 #
#####################################################


class gs():
    def __init__(self, creds_file: str, creds_info: str) -> None:
        if creds_file is not None:
            self.client = storage.Client().from_service_account_json(creds_file)
        if creds_info is not None:
            self.client = storage.Client().from_service_account_info(creds_info)

    def check_file_exists(self, bucket_name: str, name: str):
        bucket = self.client.bucket(bucket_name)
        stats = storage.Blob(bucket=bucket, name=name).exists(self.client)
        return stats

    def list_dir(self, bucket_name, path, keys_only=True):
        blobs = self.client.list_blobs(
            bucket_name,
            prefix=path,
            delimiter=None)
        blob_names = [blob.name for blob in blobs]
        if keys_only:
            blob_names = [blob_name.split("/")[-1] for blob_name in blob_names]
        return blob_names

    def download_dir(self, region, bucket_name, s3_loc, save_loc):
        pass

    def upload_dir(self, bucket_name, local_dir, gs_loc):
        pass

    def remove_file(self, bucket_name, gs_loc):
        bucket = self.client.get_bucket(bucket_name)
        blob = bucket.blob(gs_loc)
        blob.delete()

    def download_file(self, bucket_name, gs_loc, save_loc):
        bucket = self.client.get_bucket(bucket_name)
        blob = bucket.get_blob(gs_loc)
        blob.download_to_filename(save_loc)

    def upload_file(self, bucket_name, gs_loc, local_loc) -> None:
        bucket = self.client.get_bucket(bucket_name)
        blob = bucket.blob(gs_loc)
        blob.upload_from_filename(local_loc)
