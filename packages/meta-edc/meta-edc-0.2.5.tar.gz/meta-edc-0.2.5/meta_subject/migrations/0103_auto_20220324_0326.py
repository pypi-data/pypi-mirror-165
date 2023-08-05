# Generated by Django 3.2.11 on 2022-03-24 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0102_auto_20220324_0304"),
    ]

    operations = [
        migrations.AlterField(
            model_name="delivery",
            name="info_not_available_reason",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="If the report was not available, please explain?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldelivery",
            name="info_not_available_reason",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="If the report was not available, please explain?",
            ),
        ),
    ]
