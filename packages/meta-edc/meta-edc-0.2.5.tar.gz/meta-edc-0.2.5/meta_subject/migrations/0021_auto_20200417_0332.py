# Generated by Django 3.0.4 on 2020-04-17 00:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0020_auto_20200417_0329"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="coronakap",
            name="dia_blood_pressure_r1",
        ),
        migrations.RemoveField(
            model_name="coronakap",
            name="height",
        ),
        migrations.RemoveField(
            model_name="coronakap",
            name="sys_blood_pressure_r1",
        ),
        migrations.RemoveField(
            model_name="coronakap",
            name="weight",
        ),
        migrations.RemoveField(
            model_name="historicalcoronakap",
            name="dia_blood_pressure_r1",
        ),
        migrations.RemoveField(
            model_name="historicalcoronakap",
            name="height",
        ),
        migrations.RemoveField(
            model_name="historicalcoronakap",
            name="sys_blood_pressure_r1",
        ),
        migrations.RemoveField(
            model_name="historicalcoronakap",
            name="weight",
        ),
    ]
