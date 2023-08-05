# Generated by Django 3.2.7 on 2021-11-04 11:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_protocol_violation", "0003_auto_20211104_1456"),
        ("meta_prn", "0014_auto_20211003_1709"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalprotocoldeviationviolation",
            name="violation",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_protocol_violation.protocolviolations",
                verbose_name="Type of violation",
            ),
        ),
        migrations.AlterField(
            model_name="historicalprotocoldeviationviolation",
            name="violation_type",
            field=models.CharField(
                blank=True,
                choices=[
                    (
                        "failure_to_obtain_informed_consent",
                        "Failure to obtain informed consent",
                    ),
                    (
                        "enrollment_of_ineligible_patient",
                        "Enrollment of ineligible patient",
                    ),
                    (
                        "screening_procedure not done",
                        "Screening procedure required by protocol not done",
                    ),
                    (
                        "screening_or_on-study_procedure",
                        "Screening or on-study procedure/lab work required not done",
                    ),
                    (
                        "incorrect_research_treatment",
                        "Incorrect research treatment given to patient",
                    ),
                    (
                        "procedure_not_completed",
                        "On-study procedure required by protocol not completed",
                    ),
                    ("visit_non-compliance", "Visit non-compliance"),
                    ("medication_stopped_early", "Medication stopped early"),
                    ("medication_noncompliance", "Medication_noncompliance"),
                    (
                        "national_regulations_not_met",
                        "Standard WPD, ICH-GCP, local/national regulations not met",
                    ),
                    ("OTHER", "Other"),
                    ("N/A", "Not applicable"),
                ],
                default="QUESTION_RETIRED",
                max_length=75,
                null=True,
                verbose_name="Type of violation",
            ),
        ),
        migrations.AlterField(
            model_name="historicalprotocoldeviationviolation",
            name="violation_type_other",
            field=models.CharField(
                blank=True,
                default="QUESTION_RETIRED",
                max_length=75,
                null=True,
                verbose_name="If other, please specify",
            ),
        ),
        migrations.AlterField(
            model_name="protocoldeviationviolation",
            name="violation",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="edc_protocol_violation.protocolviolations",
                verbose_name="Type of violation",
            ),
        ),
        migrations.AlterField(
            model_name="protocoldeviationviolation",
            name="violation_type",
            field=models.CharField(
                blank=True,
                choices=[
                    (
                        "failure_to_obtain_informed_consent",
                        "Failure to obtain informed consent",
                    ),
                    (
                        "enrollment_of_ineligible_patient",
                        "Enrollment of ineligible patient",
                    ),
                    (
                        "screening_procedure not done",
                        "Screening procedure required by protocol not done",
                    ),
                    (
                        "screening_or_on-study_procedure",
                        "Screening or on-study procedure/lab work required not done",
                    ),
                    (
                        "incorrect_research_treatment",
                        "Incorrect research treatment given to patient",
                    ),
                    (
                        "procedure_not_completed",
                        "On-study procedure required by protocol not completed",
                    ),
                    ("visit_non-compliance", "Visit non-compliance"),
                    ("medication_stopped_early", "Medication stopped early"),
                    ("medication_noncompliance", "Medication_noncompliance"),
                    (
                        "national_regulations_not_met",
                        "Standard WPD, ICH-GCP, local/national regulations not met",
                    ),
                    ("OTHER", "Other"),
                    ("N/A", "Not applicable"),
                ],
                default="QUESTION_RETIRED",
                max_length=75,
                null=True,
                verbose_name="Type of violation",
            ),
        ),
        migrations.AlterField(
            model_name="protocoldeviationviolation",
            name="violation_type_other",
            field=models.CharField(
                blank=True,
                default="QUESTION_RETIRED",
                max_length=75,
                null=True,
                verbose_name="If other, please specify",
            ),
        ),
    ]
