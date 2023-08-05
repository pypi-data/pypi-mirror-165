# Generated by Django 3.2.4 on 2021-07-14 20:19

import uuid

import _socket
import django.db.models.deletion
import django.db.models.manager
import django_audit_fields.fields.hostname_modification_field
import django_audit_fields.fields.userfield
import django_audit_fields.fields.uuid_auto_field
import django_audit_fields.models.audit_model_mixin
import django_crypto_fields.fields.encrypted_char_field
import django_revision.revision_field
import edc_sites.models
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalRandomizationList",
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
                    "assignment",
                    django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                        blank=True, help_text=" (Encryption: RSA local)", max_length=71
                    ),
                ),
                ("randomizer_name", models.CharField(default="default", max_length=50)),
                (
                    "subject_identifier",
                    models.CharField(
                        db_index=True,
                        max_length=50,
                        null=True,
                        verbose_name="Subject Identifier",
                    ),
                ),
                ("sid", models.IntegerField(db_index=True)),
                ("site_name", models.CharField(max_length=100)),
                (
                    "allocation",
                    django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                        blank=True,
                        help_text=" (Encryption: RSA local)",
                        max_length=71,
                        null=True,
                        verbose_name="Original integer allocation",
                    ),
                ),
                ("allocated", models.BooleanField(default=False)),
                ("allocated_datetime", models.DateTimeField(null=True)),
                ("allocated_user", models.CharField(max_length=50, null=True)),
                ("verified", models.BooleanField(default=False)),
                ("verified_datetime", models.DateTimeField(null=True)),
                ("verified_user", models.CharField(max_length=50, null=True)),
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
                    "gender",
                    models.CharField(choices=[("M", "Male"), ("F", "Female")], max_length=25),
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
                    "allocated_site",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="sites.site",
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
            ],
            options={
                "verbose_name": "historical Randomization List (Phase Three)",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="RandomizationList",
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
                    "assignment",
                    django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                        blank=True, help_text=" (Encryption: RSA local)", max_length=71
                    ),
                ),
                ("randomizer_name", models.CharField(default="default", max_length=50)),
                (
                    "subject_identifier",
                    models.CharField(
                        max_length=50,
                        null=True,
                        unique=True,
                        verbose_name="Subject Identifier",
                    ),
                ),
                ("sid", models.IntegerField(unique=True)),
                ("site_name", models.CharField(max_length=100)),
                (
                    "allocation",
                    django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                        blank=True,
                        help_text=" (Encryption: RSA local)",
                        max_length=71,
                        null=True,
                        verbose_name="Original integer allocation",
                    ),
                ),
                ("allocated", models.BooleanField(default=False)),
                ("allocated_datetime", models.DateTimeField(null=True)),
                ("allocated_user", models.CharField(max_length=50, null=True)),
                ("verified", models.BooleanField(default=False)),
                ("verified_datetime", models.DateTimeField(null=True)),
                ("verified_user", models.CharField(max_length=50, null=True)),
                (
                    "gender",
                    models.CharField(choices=[("M", "Male"), ("F", "Female")], max_length=25),
                ),
                (
                    "allocated_site",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="sites.site",
                    ),
                ),
            ],
            options={
                "verbose_name": "Randomization List (Phase Three)",
                "verbose_name_plural": "Randomization List (Phase Three)",
                "ordering": ("site_name", "sid"),
                "permissions": (("display_assignment", "Can display assignment"),),
                "get_latest_by": "modified",
                "abstract": False,
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "unique_together": {("site_name", "sid")},
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("on_site", edc_sites.models.CurrentSiteManager("allocated_site")),
            ],
        ),
    ]
