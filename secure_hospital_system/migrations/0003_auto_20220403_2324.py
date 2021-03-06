# Generated by Django 3.2.5 on 2022-04-03 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secure_hospital_system', '0002_shsuser_email_confirmed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu_mapping',
            name='is_default',
        ),
        migrations.AddField(
            model_name='patient',
            name='emergency_contact_gender',
            field=models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('OTHER', 'OTHER')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='gender',
            field=models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('OTHER', 'OTHER')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='doctor_availability_booked',
            name='appointment_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='records',
            name='document',
            field=models.TextField(max_length=1000, null=True),
        ),
    ]
