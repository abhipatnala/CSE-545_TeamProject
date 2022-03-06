# Generated by Django 3.2.5 on 2022-02-20 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('doctor_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('specialization', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('patient_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=400)),
                ('zipcode', models.CharField(max_length=5)),
                ('patient_insurance_provider_id', models.CharField(max_length=15)),
                ('civil_status', models.CharField(max_length=15)),
                ('emergency_contact_firstname', models.CharField(max_length=25)),
                ('emergency_contact_lastname', models.CharField(max_length=25)),
                ('emergency_contact_info', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('shift_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('shift_type', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Records',
            fields=[
                ('records_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('document_type', models.CharField(choices=[('D', 'Diagnosis'), ('P', 'Prescription'), ('L', 'LabReport')], max_length=1)),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_portal.doctor')),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_portal.patient')),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_portal.user'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='shift_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_portal.shift'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_portal.user'),
        ),
    ]
