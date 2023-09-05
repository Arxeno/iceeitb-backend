from django.db import models
import uuid
from os.path import join

# from register.custom_storage import CustomMinioStorage
# from gdstorage.storage import GoogleDriveStorage
# import gdstorage
from .custom_storage import MinioStorage

# Define Google Drive Storage
# gd_storage = GoogleDriveStorage()

# Create your models here.


class Competition(models.Model):
    competition_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(verbose_name='Competition', unique=True)
    min_capacity = models.IntegerField()
    max_capacity = models.IntegerField()

    def __str__(self):
        return self.name


class ReferralCode(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    code = models.CharField(verbose_name='Kode Referral')
    is_redeemed = models.BooleanField(
        verbose_name='Sudah digunakan? (Ceklis berarti sudah)')

    def __str__(self):
        return self.code


class Team(models.Model):
    def upload_payment(instance, filename):
        ext = filename.split(".")[-1]

        return join('uploads', instance.team_name, f'payment.{ext}')

    # FIELDS
    team_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    # Team Registration
    team_name = models.CharField(unique=True)
    competition = models.ForeignKey(
        Competition, verbose_name='Cabang lomba', on_delete=models.DO_NOTHING)
    total_team_members = models.IntegerField(editable=False, default=0)

    # Payment
    payment_total = models.IntegerField(verbose_name='Total Pembayaran')
    referral_code = models.CharField(verbose_name='Kode Referral', blank=True)
    payment_methods = models.CharField(verbose_name='Metode Pembayaran')
    payment_proof = models.ImageField(
        verbose_name='Bukti foto pembayaran', upload_to=upload_payment)

    def __str__(self):
        print(self.payment_proof)
        return f'{self.competition.name}_{self.team_name}'


ROLE_CHOICES = [
    ('LEADER', 'Leader'),
    ('MEMBER', 'Member')
]


class Member(models.Model):
    def get_team_name(self):
        return self.team_id.team_name

    # Generate names
    def generate_name_photo_id(self, ext):
        return f'{self.role}_{self.name}_KTM.{ext}'

    def generate_name_photo_proof(self, ext):
        return f'{self.role}_{self.name}_Bukti Mahasiswa aktif.{ext}'

    def generate_name_photo_3x4(self, ext):
        return f'{self.role}_{self.name}_Foto 3x4.{ext}'

    def generate_name_photo_twibbon(self, ext):
        return f'{self.role}_{self.name}_Foto Twibbon.{ext}'

    # Generate paths
    def upload_photo_id(instance, filename):
        ext = filename.split(".")[-1]

        return join('uploads', instance.team_id.team_name, instance.generate_name_photo_id(ext))

    def upload_photo_proof(instance, filename):
        ext = filename.split(".")[-1]

        return join('uploads', instance.team_id.team_name, instance.generate_name_photo_proof(ext))

    def upload_photo_3x4(instance, filename):
        ext = filename.split(".")[-1]

        return join('uploads', instance.team_id.team_name, instance.generate_name_photo_3x4(ext))

    def upload_photo_twibbon(instance, filename):
        ext = filename.split(".")[-1]

        return join('uploads', instance.team_id.team_name, instance.generate_name_photo_twibbon(ext))

    def save_image_files(self, content_files, exts):
        self.student_id.save(
            self.generate_name_photo_id(exts[0]), content_files[0])
        self.active_student_proof.save(
            self.generate_name_photo_proof(exts[1]), content_files[1])
        self.photo_3x4.save(self.generate_name_photo_3x4(
            exts[2]), content_files[2])
        self.photo_twibbon.save(
            self.generate_name_photo_twibbon(exts[3]), content_files[3])

    member_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(verbose_name='Nama')
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(verbose_name="Role",
                            choices=ROLE_CHOICES, default='LEADER')
    university = models.CharField(verbose_name='Universitas')
    major = models.CharField(verbose_name='Jurusan')
    whatsapp_number = models.CharField(
        verbose_name='Nomor WhatsApp')
    email = models.EmailField(verbose_name='Email')
    address = models.CharField(verbose_name='Alamat')
    student_id = models.ImageField(verbose_name='Foto KTM',
                                   upload_to=upload_photo_id)
    active_student_proof = models.ImageField(verbose_name='Bukti Foto Mahasiswa Aktif',
                                             upload_to=upload_photo_proof)
    photo_3x4 = models.ImageField(verbose_name='Foto 3x4',
                                  upload_to=upload_photo_3x4)
    photo_twibbon = models.ImageField(
        verbose_name='Foto Twibbon', upload_to=upload_photo_twibbon)

    # try:
    #     print('hello')
    #     print(team_id.primary_key())
    #     team_name = Team.objects.get(team_id=team_id).team_name
    # except:
    #     team_name = ''

    def __str__(self):
        return f'{self.team_id.competition}_{self.team_id.team_name}_{self.role}_{self.name}'
