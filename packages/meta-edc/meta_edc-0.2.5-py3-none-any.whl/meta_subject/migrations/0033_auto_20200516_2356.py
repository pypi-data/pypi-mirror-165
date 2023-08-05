# Generated by Django 3.0.6 on 2020-05-16 20:56

import uuid

import _socket
import django.contrib.sites.managers
import django.core.validators
import django.db.models.deletion
import django_audit_fields.fields.hostname_modification_field
import django_audit_fields.fields.userfield
import django_audit_fields.fields.uuid_auto_field
import django_audit_fields.models.audit_model_mixin
import django_revision.revision_field
import edc_model.models.fields.other_charfield
import edc_model.validators.date
import edc_protocol.validators
import edc_utils.date
import edc_visit_tracking.managers
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("meta_lists", "0007_auto_20200516_2356"),
        ("sites", "0002_alter_domain_unique"),
        ("meta_subject", "0032_auto_20200515_0307"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="followup",
            name="followup_reason",
        ),
        migrations.RemoveField(
            model_name="historicalfollowup",
            name="followup_reason",
        ),
        migrations.AddField(
            model_name="historicalsubjectvisit",
            name="unschedule_detail",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="If 'unschedule', please provide further details, if any",
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectvisit",
            name="unschedule_self_referral",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="No",
                max_length=25,
                verbose_name="If 'unschedule', is this a self-referral?",
            ),
        ),
        migrations.AddField(
            model_name="subjectvisit",
            name="unschedule_detail",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="If 'unschedule', please provide further details, if any",
            ),
        ),
        migrations.AddField(
            model_name="subjectvisit",
            name="unschedule_self_referral",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="No",
                max_length=25,
                verbose_name="If 'unschedule', is this a self-referral?",
            ),
        ),
        migrations.CreateModel(
            name="MissedVisit",
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
                        blank=True,
                        default=django_audit_fields.models.audit_model_mixin.utcnow,
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        blank=True,
                        default=django_audit_fields.models.audit_model_mixin.utcnow,
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
                (
                    "report_datetime",
                    models.DateTimeField(
                        default=edc_utils.date.get_utcnow,
                        help_text="If reporting today, use today's date/time, otherwise use the date/time this information was reported.",
                        validators=[
                            edc_protocol.validators.datetime_not_before_study_start,
                            edc_model.validators.date.datetime_not_future,
                        ],
                        verbose_name="Report Date",
                    ),
                ),
                (
                    "consent_model",
                    models.CharField(editable=False, max_length=50, null=True),
                ),
                (
                    "consent_version",
                    models.CharField(editable=False, max_length=10, null=True),
                ),
                (
                    "contact_attempted",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")],
                        help_text="Not including pre-appointment reminders",
                        max_length=25,
                        verbose_name="Were any attempts made to contact the participant since the expected appointment date?",
                    ),
                ),
                (
                    "contact_attempts_made",
                    models.IntegerField(
                        blank=True,
                        help_text="Not including pre-appointment reminders",
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Number of attempts made to contact participant since the expected appointment date",
                    ),
                ),
                (
                    "contact_last_date",
                    models.DateField(
                        blank=True,
                        null=True,
                        verbose_name="Date of last telephone contact/attempt",
                    ),
                ),
                (
                    "contact_made",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")],
                        default="No",
                        max_length=25,
                        verbose_name="Was contact finally made with the participant?",
                    ),
                ),
                (
                    "missed_reasons_other",
                    edc_model.models.fields.other_charfield.OtherCharField(
                        blank=True,
                        max_length=35,
                        null=True,
                        verbose_name="If other, please specify ...",
                    ),
                ),
                (
                    "comment",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="Please provide further details, if any",
                    ),
                ),
                (
                    "missed_reasons",
                    models.ManyToManyField(to="meta_lists.SubjectVisitMissedReasons"),
                ),
                (
                    "site",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="sites.Site",
                    ),
                ),
                (
                    "subject_visit",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="meta_subject.SubjectVisit",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
            },
            managers=[
                ("on_site", django.contrib.sites.managers.CurrentSiteManager()),
                ("objects", edc_visit_tracking.managers.CrfModelManager()),
            ],
        ),
        migrations.CreateModel(
            name="HistoricalMissedVisit",
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
                        blank=True,
                        default=django_audit_fields.models.audit_model_mixin.utcnow,
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        blank=True,
                        default=django_audit_fields.models.audit_model_mixin.utcnow,
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
                (
                    "report_datetime",
                    models.DateTimeField(
                        default=edc_utils.date.get_utcnow,
                        help_text="If reporting today, use today's date/time, otherwise use the date/time this information was reported.",
                        validators=[
                            edc_protocol.validators.datetime_not_before_study_start,
                            edc_model.validators.date.datetime_not_future,
                        ],
                        verbose_name="Report Date",
                    ),
                ),
                (
                    "consent_model",
                    models.CharField(editable=False, max_length=50, null=True),
                ),
                (
                    "consent_version",
                    models.CharField(editable=False, max_length=10, null=True),
                ),
                (
                    "history_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "contact_attempted",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")],
                        help_text="Not including pre-appointment reminders",
                        max_length=25,
                        verbose_name="Were any attempts made to contact the participant since the expected appointment date?",
                    ),
                ),
                (
                    "contact_attempts_made",
                    models.IntegerField(
                        blank=True,
                        help_text="Not including pre-appointment reminders",
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Number of attempts made to contact participant since the expected appointment date",
                    ),
                ),
                (
                    "contact_last_date",
                    models.DateField(
                        blank=True,
                        null=True,
                        verbose_name="Date of last telephone contact/attempt",
                    ),
                ),
                (
                    "contact_made",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")],
                        default="No",
                        max_length=25,
                        verbose_name="Was contact finally made with the participant?",
                    ),
                ),
                (
                    "missed_reasons_other",
                    edc_model.models.fields.other_charfield.OtherCharField(
                        blank=True,
                        max_length=35,
                        null=True,
                        verbose_name="If other, please specify ...",
                    ),
                ),
                (
                    "comment",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="Please provide further details, if any",
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
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
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
                        to="sites.Site",
                    ),
                ),
                (
                    "subject_visit",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="meta_subject.SubjectVisit",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical missed visit",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddIndex(
            model_name="missedvisit",
            index=models.Index(
                fields=["subject_visit", "site", "id"],
                name="meta_subjec_subject_74ee6f_idx",
            ),
        ),
    ]
