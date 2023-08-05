# Generated by Django 3.2.4 on 2021-08-01 17:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0068_auto_20210728_1809"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalmnsi",
            name="calculated_patient_history_score",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(13),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="historicalmnsi",
            name="calculated_physical_assessment_score",
            field=models.DecimalField(
                blank=True,
                decimal_places=1,
                max_digits=3,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(10.0),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="mnsi",
            name="calculated_patient_history_score",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(13),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="mnsi",
            name="calculated_physical_assessment_score",
            field=models.DecimalField(
                blank=True,
                decimal_places=1,
                max_digits=3,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(10.0),
                ],
            ),
        ),
    ]
