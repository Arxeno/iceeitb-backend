import os
import shutil
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from register.models import Team, Member


@receiver(pre_delete, sender=Team)
def delete_team_files(sender, instance, **kwargs):
    if os.path.isdir(f'uploads/{instance.team_name}'):
        shutil.rmtree(f'uploads/{instance.team_name}')


@receiver(pre_delete, sender=Member)
def delete_member_files(sender, instance, **kwargs):
    os.remove(instance.student_id.path)
    os.remove(instance.active_student_proof.path)
    os.remove(instance.photo_3x4.path)
    os.remove(instance.photo_twibbon.path)
