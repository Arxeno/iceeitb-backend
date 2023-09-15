import os
import shutil
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from register.models import Team, Member
from .custom_storage import MinioStorage
from django.conf import settings


@receiver(pre_delete, sender=Team)
def delete_team_files(sender, instance, **kwargs):
    try:
        minio_client = MinioStorage()
        minio_client.delete(instance.payment_proof.url.replace(
            f'{settings.DJANGO_DOMAIN}/', ''))
    except:
        print(f"payment.png for {instance.team_name} is not exist.")


@receiver(pre_delete, sender=Member)
def delete_member_files(sender, instance, **kwargs):
    try:
        minio_client = MinioStorage()
        minio_client.delete(instance.student_id.url.replace(
            f'{settings.DJANGO_DOMAIN}/', ''))
        minio_client.delete(instance.active_student_proof.url.replace(
            f'{settings.DJANGO_DOMAIN}/', ''))
        minio_client.delete(instance.photo_3x4.url.replace(
            f'{settings.DJANGO_DOMAIN}/', ''))
        minio_client.delete(instance.photo_twibbon.url.replace(
            f'{settings.DJANGO_DOMAIN}/', ''))
    except:
        print(f"some files for {instance.name} is not exist.")

    # os.remove(instance.student_id.path)
    # os.remove(instance.active_student_proof.path)
    # os.remove(instance.photo_3x4.path)
    # os.remove(instance.photo_twibbon.path)
