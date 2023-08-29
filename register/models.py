from django.db import models
import uuid

# Create your models here.


class Team(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    # Team Registration
    team_name = models.CharField()
    total_team_members = models.IntegerField()  # TODO: pasang validator
    # Team Leader
    leader_name = models.CharField()
    leader_university = models.CharField()
    leader_major = models.CharField()
    leader_whatsapp_number = models.CharField()
    leader_email = models.EmailField()
    Leader_address = models.CharField()
    leader_student_id = models.ImageField()
    leader_active_student_proof = models.ImageField()
    leader_3x4_photo = models.ImageField()
    # Team Member 1
    member_1_name = models.CharField()
    member_1_university = models.CharField()
    member_1_major = models.CharField()
    member_1_whatsapp_number = models.CharField()
    member_1_email = models.EmailField()
    member_1_address = models.CharField()
    member_1_student_id = models.ImageField()
    member_1_active_student_proof = models.ImageField()
    member_1_3x4_photo = models.ImageField()
    # Team Member 2
    member_2_name = models.CharField()
    member_2_university = models.CharField()
    member_2_major = models.CharField()
    member_2_whatsapp_number = models.CharField()
    member_2_email = models.EmailField()
    member_2_address = models.CharField()
    member_2_student_id = models.ImageField()
    member_2_active_student_proof = models.ImageField()
    member_2_3x4_photo = models.ImageField()
    # Team Member 3
    member_3_name = models.CharField()
    member_3_university = models.CharField()
    member_3_major = models.CharField()
    member_3_whatsapp_number = models.CharField()
    member_3_email = models.EmailField()
    member_3_address = models.CharField()
    member_3_student_id = models.ImageField()
    member_3_active_student_proof = models.ImageField()
    member_3_3x4_photo = models.ImageField()
    # Payment
    payment_total = models.IntegerField()
    referral_code = models.CharField()
    payment_methods = models.CharField()
    payment_proof = models.ImageField()
