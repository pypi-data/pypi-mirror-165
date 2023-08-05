# Generated by Django 3.2.11 on 2022-03-04 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_screening", "0032_auto_20220304_0501"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalscreeningpartone",
            name="ogtt2_performed",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="No",
                max_length=15,
                verbose_name="In opinion of the clinician, should the OGTT be repeated?",
            ),
        ),
        migrations.AddField(
            model_name="historicalscreeningpartthree",
            name="ogtt2_performed",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="No",
                max_length=15,
                verbose_name="In opinion of the clinician, should the OGTT be repeated?",
            ),
        ),
        migrations.AddField(
            model_name="historicalscreeningparttwo",
            name="ogtt2_performed",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="No",
                max_length=15,
                verbose_name="In opinion of the clinician, should the OGTT be repeated?",
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectscreening",
            name="ogtt2_performed",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="No",
                max_length=15,
                verbose_name="In opinion of the clinician, should the OGTT be repeated?",
            ),
        ),
        migrations.AddField(
            model_name="subjectscreening",
            name="ogtt2_performed",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="No",
                max_length=15,
                verbose_name="In opinion of the clinician, should the OGTT be repeated?",
            ),
        ),
    ]
