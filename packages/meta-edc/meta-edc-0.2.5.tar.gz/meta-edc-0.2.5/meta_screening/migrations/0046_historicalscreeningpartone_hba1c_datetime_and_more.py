# Generated by Django 4.0.5 on 2022-06-27 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_screening", "0045_historicalscreeningpartone_contact_number_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalscreeningpartone",
            name="hba1c_datetime",
            field=models.DateTimeField(
                blank=True,
                help_text="Date and time of result.",
                null=True,
                verbose_name="HbA1c date and time",
            ),
        ),
        migrations.AddField(
            model_name="historicalscreeningpartthree",
            name="hba1c_datetime",
            field=models.DateTimeField(
                blank=True,
                help_text="Date and time of result.",
                null=True,
                verbose_name="HbA1c date and time",
            ),
        ),
        migrations.AddField(
            model_name="historicalscreeningparttwo",
            name="hba1c_datetime",
            field=models.DateTimeField(
                blank=True,
                help_text="Date and time of result.",
                null=True,
                verbose_name="HbA1c date and time",
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectscreening",
            name="hba1c_datetime",
            field=models.DateTimeField(
                blank=True,
                help_text="Date and time of result.",
                null=True,
                verbose_name="HbA1c date and time",
            ),
        ),
        migrations.AddField(
            model_name="subjectscreening",
            name="hba1c_datetime",
            field=models.DateTimeField(
                blank=True,
                help_text="Date and time of result.",
                null=True,
                verbose_name="HbA1c date and time",
            ),
        ),
    ]
