# Generated by Django 4.2.4 on 2023-09-22 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_remove_referralcode_is_redeemed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='referral_code',
            field=models.CharField(blank=True, null=True, verbose_name='Kode Referral'),
        ),
    ]
