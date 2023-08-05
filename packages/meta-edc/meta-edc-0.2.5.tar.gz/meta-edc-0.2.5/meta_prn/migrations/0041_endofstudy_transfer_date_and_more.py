# Generated by Django 4.0.5 on 2022-07-03 19:15

import _socket
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_audit_fields.fields.hostname_modification_field
import django_audit_fields.fields.userfield
import django_audit_fields.fields.uuid_auto_field
import django_audit_fields.models.audit_model_mixin
import django_crypto_fields.fields.encrypted_text_field
import django_revision.revision_field
import edc_action_item.models.action_model_mixin
import edc_model.models.fields.other_charfield
import edc_model.validators.date
import edc_sites.models
import edc_utils.date
import simple_history.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("edc_action_item", "0028_auto_20210203_0706"),
        ("meta_lists", "0013_transferreasons_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "meta_prn",
            "0040_remove_historicaloffstudymedication_expected_restart_date_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="endofstudy",
            name="transfer_date",
            field=models.DateField(
                blank=True,
                help_text="A Transfer form must be on file.",
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="Date of transfer, if applicable",
            ),
        ),
        migrations.AddField(
            model_name="historicalendofstudy",
            name="transfer_date",
            field=models.DateField(
                blank=True,
                help_text="A Transfer form must be on file.",
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="Date of transfer, if applicable",
            ),
        ),
        migrations.AlterField(
            model_name="endofstudy",
            name="clinical_withdrawal_reason",
            field=models.CharField(
                blank=True,
                choices=[
                    ("kidney_disease", "Development of chronic kidney disease"),
                    ("liver_disease", "Development of chronic liver disease"),
                    (
                        "intercurrent_illness",
                        "Intercurrent illness which prevents further treatment",
                    ),
                    ("investigator_decision", "Investigator decision (specify below)"),
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
            name="offstudy_reason",
            field=models.ForeignKey(
                limit_choices_to={
                    "name__in": [
                        "clinical_withdrawal",
                        "completed_followup",
                        "dead",
                        "delivery",
                        "diabetes",
                        "late_exclusion",
                        "LTFU",
                        "OTHER",
                        "pregnancy",
                        "toxicity",
                        "transferred",
                        "withdrawal",
                    ]
                },
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="meta_lists.offstudyreasons",
                verbose_name="Reason patient was terminated from the study",
            ),
        ),
        migrations.AlterField(
            model_name="endofstudy",
            name="toxicity_withdrawal_reason",
            field=models.CharField(
                blank=True,
                choices=[
                    ("lactic_acidosis", "Development of lactic acidosis or hyperlactatemia"),
                    ("hepatomegaly", "Development of hepatomegaly with steatosis"),
                    ("OTHER", "Other (specify below)"),
                ],
                max_length=25,
                null=True,
                verbose_name=" Patient experienced an unacceptable toxicity, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="historicalendofstudy",
            name="clinical_withdrawal_reason",
            field=models.CharField(
                blank=True,
                choices=[
                    ("kidney_disease", "Development of chronic kidney disease"),
                    ("liver_disease", "Development of chronic liver disease"),
                    (
                        "intercurrent_illness",
                        "Intercurrent illness which prevents further treatment",
                    ),
                    ("investigator_decision", "Investigator decision (specify below)"),
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
            name="offstudy_reason",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                limit_choices_to={
                    "name__in": [
                        "clinical_withdrawal",
                        "completed_followup",
                        "dead",
                        "delivery",
                        "diabetes",
                        "late_exclusion",
                        "LTFU",
                        "OTHER",
                        "pregnancy",
                        "toxicity",
                        "transferred",
                        "withdrawal",
                    ]
                },
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="meta_lists.offstudyreasons",
                verbose_name="Reason patient was terminated from the study",
            ),
        ),
        migrations.AlterField(
            model_name="historicalendofstudy",
            name="toxicity_withdrawal_reason",
            field=models.CharField(
                blank=True,
                choices=[
                    ("lactic_acidosis", "Development of lactic acidosis or hyperlactatemia"),
                    ("hepatomegaly", "Development of hepatomegaly with steatosis"),
                    ("OTHER", "Other (specify below)"),
                ],
                max_length=25,
                null=True,
                verbose_name=" Patient experienced an unacceptable toxicity, please specify ...",
            ),
        ),
        migrations.CreateModel(
            name="SubjectTransfer",
            fields=[
                (
                    "revision",
                    django_revision.revision_field.RevisionField(
                        blank=True,
                        editable=False,
                        help_text="System field. Git repository tag:branch:commit.",
                        max_length=75,
                        null=True,
                        verbose_name="Revision",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow
                    ),
                ),
                (
                    "user_created",
                    django_audit_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user created",
                    ),
                ),
                (
                    "user_modified",
                    django_audit_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user modified",
                    ),
                ),
                (
                    "hostname_created",
                    models.CharField(
                        blank=True,
                        default=_socket.gethostname,
                        help_text="System field. (modified on create only)",
                        max_length=60,
                    ),
                ),
                (
                    "hostname_modified",
                    django_audit_fields.fields.hostname_modification_field.HostnameModificationField(
                        blank=True,
                        help_text="System field. (modified on every save)",
                        max_length=50,
                    ),
                ),
                ("device_created", models.CharField(blank=True, max_length=10)),
                ("device_modified", models.CharField(blank=True, max_length=10)),
                (
                    "id",
                    django_audit_fields.fields.uuid_auto_field.UUIDAutoField(
                        blank=True,
                        editable=False,
                        help_text="System auto field. UUID primary key.",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("subject_identifier", models.CharField(max_length=50, unique=True)),
                ("tracking_identifier", models.CharField(max_length=32, unique=True)),
                ("action_identifier", models.CharField(max_length=50, unique=True)),
                (
                    "parent_action_identifier",
                    models.CharField(
                        blank=True,
                        help_text="action identifier that links to parent reference model instance.",
                        max_length=30,
                        null=True,
                    ),
                ),
                (
                    "related_action_identifier",
                    models.CharField(
                        blank=True,
                        help_text="action identifier that links to related reference model instance.",
                        max_length=30,
                        null=True,
                    ),
                ),
                ("action_item_reason", models.TextField(editable=False, null=True)),
                (
                    "report_datetime",
                    models.DateTimeField(
                        default=edc_utils.date.get_utcnow, verbose_name="Report Date and Time"
                    ),
                ),
                (
                    "transfer_date",
                    models.DateField(
                        default=edc_utils.date.get_utcnow, verbose_name="Transfer date"
                    ),
                ),
                (
                    "initiated_by",
                    models.CharField(
                        choices=[
                            ("patient", "Patient"),
                            ("clinician", "Attending Clinician / Healthcare worker"),
                            ("OTHER", "Other"),
                        ],
                        max_length=25,
                        verbose_name="Who initiated the transfer request",
                    ),
                ),
                (
                    "initiated_by_other",
                    edc_model.models.fields.other_charfield.OtherCharField(
                        blank=True,
                        max_length=35,
                        null=True,
                        verbose_name="If other, please specify ...",
                    ),
                ),
                (
                    "transfer_reason_other",
                    edc_model.models.fields.other_charfield.OtherCharField(
                        blank=True,
                        max_length=35,
                        null=True,
                        verbose_name="If other, please specify ...",
                    ),
                ),
                (
                    "may_return",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No"), ("not_sure", "Not sure")],
                        max_length=15,
                        verbose_name="Is the participant likely to transfer back before the end of their stay in the trial?",
                    ),
                ),
                (
                    "may_contact",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")],
                        max_length=15,
                        verbose_name="Is the participant willing to be contacted at the end of the study?",
                    ),
                ),
                (
                    "comment",
                    django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(
                        blank=True,
                        help_text=" (Encryption: AES local)",
                        max_length=71,
                        verbose_name="Additional Comments",
                    ),
                ),
                (
                    "action_item",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="edc_action_item.actionitem",
                    ),
                ),
                (
                    "parent_action_item",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="edc_action_item.actionitem",
                    ),
                ),
                (
                    "related_action_item",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="edc_action_item.actionitem",
                    ),
                ),
                (
                    "site",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="sites.site",
                    ),
                ),
                (
                    "transfer_reason",
                    models.ManyToManyField(
                        to="meta_lists.transferreasons", verbose_name="Reason for transfer"
                    ),
                ),
            ],
            options={
                "verbose_name": "Subject Transfer",
                "verbose_name_plural": "Subject Transfers",
                "ordering": ("-modified", "-created"),
                "get_latest_by": "modified",
                "abstract": False,
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
            },
            managers=[
                ("on_site", edc_sites.models.CurrentSiteManager()),
                (
                    "objects",
                    edc_action_item.models.action_model_mixin.ActionItemModelManager(),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HistoricalSubjectTransfer",
            fields=[
                (
                    "revision",
                    django_revision.revision_field.RevisionField(
                        blank=True,
                        editable=False,
                        help_text="System field. Git repository tag:branch:commit.",
                        max_length=75,
                        null=True,
                        verbose_name="Revision",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow
                    ),
                ),
                (
                    "user_created",
                    django_audit_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user created",
                    ),
                ),
                (
                    "user_modified",
                    django_audit_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user modified",
                    ),
                ),
                (
                    "hostname_created",
                    models.CharField(
                        blank=True,
                        default=_socket.gethostname,
                        help_text="System field. (modified on create only)",
                        max_length=60,
                    ),
                ),
                (
                    "hostname_modified",
                    django_audit_fields.fields.hostname_modification_field.HostnameModificationField(
                        blank=True,
                        help_text="System field. (modified on every save)",
                        max_length=50,
                    ),
                ),
                ("device_created", models.CharField(blank=True, max_length=10)),
                ("device_modified", models.CharField(blank=True, max_length=10)),
                (
                    "id",
                    django_audit_fields.fields.uuid_auto_field.UUIDAutoField(
                        blank=True,
                        db_index=True,
                        editable=False,
                        help_text="System auto field. UUID primary key.",
                    ),
                ),
                ("subject_identifier", models.CharField(db_index=True, max_length=50)),
                ("tracking_identifier", models.CharField(db_index=True, max_length=32)),
                ("action_identifier", models.CharField(db_index=True, max_length=50)),
                (
                    "parent_action_identifier",
                    models.CharField(
                        blank=True,
                        help_text="action identifier that links to parent reference model instance.",
                        max_length=30,
                        null=True,
                    ),
                ),
                (
                    "related_action_identifier",
                    models.CharField(
                        blank=True,
                        help_text="action identifier that links to related reference model instance.",
                        max_length=30,
                        null=True,
                    ),
                ),
                ("action_item_reason", models.TextField(editable=False, null=True)),
                (
                    "history_id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "report_datetime",
                    models.DateTimeField(
                        default=edc_utils.date.get_utcnow, verbose_name="Report Date and Time"
                    ),
                ),
                (
                    "transfer_date",
                    models.DateField(
                        default=edc_utils.date.get_utcnow, verbose_name="Transfer date"
                    ),
                ),
                (
                    "initiated_by",
                    models.CharField(
                        choices=[
                            ("patient", "Patient"),
                            ("clinician", "Attending Clinician / Healthcare worker"),
                            ("OTHER", "Other"),
                        ],
                        max_length=25,
                        verbose_name="Who initiated the transfer request",
                    ),
                ),
                (
                    "initiated_by_other",
                    edc_model.models.fields.other_charfield.OtherCharField(
                        blank=True,
                        max_length=35,
                        null=True,
                        verbose_name="If other, please specify ...",
                    ),
                ),
                (
                    "transfer_reason_other",
                    edc_model.models.fields.other_charfield.OtherCharField(
                        blank=True,
                        max_length=35,
                        null=True,
                        verbose_name="If other, please specify ...",
                    ),
                ),
                (
                    "may_return",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No"), ("not_sure", "Not sure")],
                        max_length=15,
                        verbose_name="Is the participant likely to transfer back before the end of their stay in the trial?",
                    ),
                ),
                (
                    "may_contact",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")],
                        max_length=15,
                        verbose_name="Is the participant willing to be contacted at the end of the study?",
                    ),
                ),
                (
                    "comment",
                    django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(
                        blank=True,
                        help_text=" (Encryption: AES local)",
                        max_length=71,
                        verbose_name="Additional Comments",
                    ),
                ),
                ("history_date", models.DateTimeField()),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "action_item",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="edc_action_item.actionitem",
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "parent_action_item",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="edc_action_item.actionitem",
                    ),
                ),
                (
                    "related_action_item",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="edc_action_item.actionitem",
                    ),
                ),
                (
                    "site",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="sites.site",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical Subject Transfer",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
