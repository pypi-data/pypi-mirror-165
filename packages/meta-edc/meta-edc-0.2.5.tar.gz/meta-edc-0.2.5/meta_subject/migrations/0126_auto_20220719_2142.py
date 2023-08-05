# Generated by Django 3.2.11 on 2022-07-19 18:42

from django.db import migrations


def update_egfr_drop_action(apps, schema_editor):
    action_item_model_cls = apps.get_model("edc_action_item.actionitem")
    crf_metadata_model_cls = apps.get_model("edc_metadata.crfmetadata")
    action_item_model_cls.objects.filter(
        reference_model="meta_subject.egfrnotification"
    ).update(reference_model="meta_subject.egfrdropnotification")
    crf_metadata_model_cls.objects.filter(model="meta_subject.egfrnotification").update(
        model="meta_subject.egfrdropnotification"
    )


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0125_auto_20220719_2134"),
    ]

    operations = [migrations.RunPython(update_egfr_drop_action)]
