# Generated by Django 4.0.5 on 2022-07-03 09:35

from django.db import migrations, models
import django.db.models.deletion
import edc_model.validators.date


class Migration(migrations.Migration):

    dependencies = [
        ("meta_lists", "0012_auto_20210728_1809"),
        ("meta_prn", "0036_remove_endofstudy_meta_prn_en_id_a50384_idx_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="endofstudy",
            name="delivery_date",
            field=models.DateField(
                blank=True,
                help_text="A delivery CRF must be on file",
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="Date of delivery, if applicable",
            ),
        ),
        migrations.AddField(
            model_name="endofstudy",
            name="pregnancy_date",
            field=models.DateField(
                blank=True,
                help_text="A UPT CRF must be on file. Use UPT date or, if UPT not done, use report date on last UPT CRF.",
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="Date pregnancy reported/UPT, if applicable",
            ),
        ),
        migrations.AddField(
            model_name="historicalendofstudy",
            name="delivery_date",
            field=models.DateField(
                blank=True,
                help_text="A delivery CRF must be on file",
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="Date of delivery, if applicable",
            ),
        ),
        migrations.AddField(
            model_name="historicalendofstudy",
            name="pregnancy_date",
            field=models.DateField(
                blank=True,
                help_text="A UPT CRF must be on file. Use UPT date or, if UPT not done, use report date on last UPT CRF.",
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="Date pregnancy reported/UPT, if applicable",
            ),
        ),
        migrations.AlterField(
            model_name="endofstudy",
            name="clinical_withdrawal_reason",
            field=models.CharField(
                blank=True,
                choices=[
                    ("diabetes", "Patient developed diabetes"),
                    ("kidney_disease", "Development of chronic kidney disease"),
                    ("liver_disease", "Development of chronic liver disease"),
                    ("toxicity", "Patient experienced an unacceptable toxicity"),
                    (
                        "intercurrent_illness",
                        "Intercurrent illness which prevents further treatment",
                    ),
                    ("investigator_decision", "Investigator decision"),
                    (
                        "OTHER",
                        "Other condition that justifies the discontinuation of treatment in the clinician’s opinion (specify below)",
                    ),
                ],
                max_length=25,
                null=True,
                verbose_name="If withdrawn on CLINICAL grounds, please specify PRIMARY reason...",
            ),
        ),
        migrations.AlterField(
            model_name="endofstudy",
            name="death_date",
            field=models.DateField(
                blank=True,
                help_text="A Death report must be on file",
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="Date of death, if applicable",
            ),
        ),
        migrations.AlterField(
            model_name="endofstudy",
            name="offstudy_reason",
            field=models.ForeignKey(
                limit_choices_to={
                    "name__in": [
                        "completed_followup",
                        "delivery",
                        "pregnancy",
                        "clinical_withdrawal",
                        "clinical_endpoint",
                        "LTFU",
                        "dead",
                        "withdrawal",
                        "late_exclusion",
                        "transferred",
                        "OTHER",
                    ]
                },
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="meta_lists.offstudyreasons",
                verbose_name="Reason patient was terminated from the study",
            ),
        ),
        migrations.AlterField(
            model_name="historicalendofstudy",
            name="clinical_withdrawal_reason",
            field=models.CharField(
                blank=True,
                choices=[
                    ("diabetes", "Patient developed diabetes"),
                    ("kidney_disease", "Development of chronic kidney disease"),
                    ("liver_disease", "Development of chronic liver disease"),
                    ("toxicity", "Patient experienced an unacceptable toxicity"),
                    (
                        "intercurrent_illness",
                        "Intercurrent illness which prevents further treatment",
                    ),
                    ("investigator_decision", "Investigator decision"),
                    (
                        "OTHER",
                        "Other condition that justifies the discontinuation of treatment in the clinician’s opinion (specify below)",
                    ),
                ],
                max_length=25,
                null=True,
                verbose_name="If withdrawn on CLINICAL grounds, please specify PRIMARY reason...",
            ),
        ),
        migrations.AlterField(
            model_name="historicalendofstudy",
            name="death_date",
            field=models.DateField(
                blank=True,
                help_text="A Death report must be on file",
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="Date of death, if applicable",
            ),
        ),
        migrations.AlterField(
            model_name="historicalendofstudy",
            name="offstudy_reason",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                limit_choices_to={
                    "name__in": [
                        "completed_followup",
                        "delivery",
                        "pregnancy",
                        "clinical_withdrawal",
                        "clinical_endpoint",
                        "LTFU",
                        "dead",
                        "withdrawal",
                        "late_exclusion",
                        "transferred",
                        "OTHER",
                    ]
                },
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="meta_lists.offstudyreasons",
                verbose_name="Reason patient was terminated from the study",
            ),
        ),
    ]
