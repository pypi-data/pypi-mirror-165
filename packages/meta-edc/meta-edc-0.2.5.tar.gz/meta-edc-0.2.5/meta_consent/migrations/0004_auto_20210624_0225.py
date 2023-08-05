# Generated by Django 3.2.4 on 2021-06-23 23:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_action_item", "0028_auto_20210203_0706"),
        ("meta_consent", "0003_auto_20200325_0901"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="historicalsubjectconsent",
            options={
                "get_latest_by": "history_date",
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Subject Consent",
            },
        ),
        migrations.AlterModelOptions(
            name="subjectconsent",
            options={
                "get_latest_by": "consent_datetime",
                "ordering": ("created",),
                "verbose_name": "Subject Consent",
                "verbose_name_plural": "Subject Consents",
            },
        ),
        migrations.AlterField(
            model_name="historicalsubjectreconsent",
            name="parent_action_identifier",
            field=models.CharField(
                blank=True,
                help_text="action identifier that links to parent reference model instance.",
                max_length=30,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectreconsent",
            name="related_action_identifier",
            field=models.CharField(
                blank=True,
                help_text="action identifier that links to related reference model instance.",
                max_length=30,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="subjectreconsent",
            name="action_item",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_action_item.actionitem",
            ),
        ),
        migrations.AlterField(
            model_name="subjectreconsent",
            name="parent_action_identifier",
            field=models.CharField(
                blank=True,
                help_text="action identifier that links to parent reference model instance.",
                max_length=30,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="subjectreconsent",
            name="parent_action_item",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="edc_action_item.actionitem",
            ),
        ),
        migrations.AlterField(
            model_name="subjectreconsent",
            name="related_action_identifier",
            field=models.CharField(
                blank=True,
                help_text="action identifier that links to related reference model instance.",
                max_length=30,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="subjectreconsent",
            name="related_action_item",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="edc_action_item.actionitem",
            ),
        ),
    ]
