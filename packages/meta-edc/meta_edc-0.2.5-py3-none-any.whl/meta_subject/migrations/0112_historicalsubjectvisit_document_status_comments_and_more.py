# Generated by Django 4.0.5 on 2022-06-24 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0111_alter_followupvitals_severe_htn_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalsubjectvisit",
            name="document_status_comments",
            field=models.TextField(
                blank=True,
                help_text="for example, why some data is still pending",
                null=True,
                verbose_name="Any comments related to status of this document",
            ),
        ),
        migrations.AddField(
            model_name="subjectvisit",
            name="document_status_comments",
            field=models.TextField(
                blank=True,
                help_text="for example, why some data is still pending",
                null=True,
                verbose_name="Any comments related to status of this document",
            ),
        ),
    ]
