# Generated by Django 3.2.11 on 2022-07-22 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0133_auto_20220722_2140"),
    ]

    operations = [
        migrations.AddField(
            model_name="bloodresultsrft",
            name="old_egfr_drop_value",
            field=models.DecimalField(
                decimal_places=4,
                editable=False,
                help_text="incorrect ckd-epi calculation (w/ 1.150 as ethnicity factor)",
                max_digits=10,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsrft",
            name="old_egfr_value",
            field=models.DecimalField(
                decimal_places=4,
                editable=False,
                help_text="incorrect ckd-epi calculation (w/ 1.150 as ethnicity factor)",
                max_digits=8,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsrft",
            name="old_egfr_drop_value",
            field=models.DecimalField(
                decimal_places=4,
                editable=False,
                help_text="incorrect ckd-epi calculation (w/ 1.150 as ethnicity factor)",
                max_digits=10,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsrft",
            name="old_egfr_value",
            field=models.DecimalField(
                decimal_places=4,
                editable=False,
                help_text="incorrect ckd-epi calculation (w/ 1.150 as ethnicity factor)",
                max_digits=8,
                null=True,
            ),
        ),
    ]
