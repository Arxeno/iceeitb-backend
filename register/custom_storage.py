from django.conf import settings
from django.core.files.storage import Storage
from minio import Minio
from minio.error import S3Error
from django.core.files.base import File
from django.core.exceptions import ImproperlyConfigured


class MinioStorage(Storage):
    def __init__(self, minio_client=None):
        if minio_client is None:
            self.minio_client = Minio(
                endpoint=settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=True,
            )
        else:
            self.minio_client = minio_client

        self.bucket_name = settings.MINIO_BUCKET_NAME

    def _open(self, name, mode='rb'):
        try:
            response = self.minio_client.get_object(
                bucket_name=settings.MINIO_BUCKET_NAME, object_name=name)

            file = File(response)

            file.name = name
            return file
        except S3Error as e:
            # Handle any exceptions raised during the file retrieval
            raise IOError(f"Error opening file from Minio: {str(e)}")

    def _save(self, name, content):
        # Implement file save logic here
        unique_name = f'{name}'

        try:
            self.minio_client.put_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=unique_name,
                data=content,
                length=content.size,
                content_type=content.content_type)
            return unique_name
        except S3Error as e:
            # Handle any exceptions raised during the upload
            raise IOError(f"Error uploading file to Minio: {str(e)}")

    def delete(self, name):
        # Implement file delete logic here
        try:
            # Check if the file exists before attempting to delete it
            if not self.exists(name):
                raise FileNotFoundError(f"File not found: {name}")

            # Delete the file from Minio
            self.minio_client.remove_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=name
            )
        except S3Error as e:
            # Handle any exceptions raised during the file deletion
            raise IOError(f"Error deleting file from Minio: {str(e)}")

    def exists(self, name):
        # Implement file existence check logic here
        try:
            # Check if the file exists in Minio
            self.minio_client.stat_object(
                bucket_name=self.bucket_name,
                object_name=name
            )
            return True
        except S3Error:
            # The file does not exist in Minio
            return False
        except ImproperlyConfigured as e:
            # Handle any configuration issues (e.g., missing bucket) gracefully
            raise ImproperlyConfigured(f"Minio configuration error: {str(e)}")

    def url(self, name):
        # Generate and return a URL for the file
        return f'{settings.DJANGO_DOMAIN}/{name}'
