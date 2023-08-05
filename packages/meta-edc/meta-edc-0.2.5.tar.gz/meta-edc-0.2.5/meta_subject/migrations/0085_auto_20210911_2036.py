# Generated by Django 3.2.6 on 2021-09-11 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0084_auto_20210910_0234"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bloodresultsfbc",
            name="tracking_identifier",
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name="bloodresultsglu",
            name="tracking_identifier",
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name="bloodresultshba1c",
            name="tracking_identifier",
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name="bloodresultsins",
            name="tracking_identifier",
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name="bloodresultslft",
            name="tracking_identifier",
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name="bloodresultslipid",
            name="tracking_identifier",
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name="bloodresultsrft",
            name="tracking_identifier",
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultsfbc",
            name="tracking_identifier",
            field=models.CharField(db_index=True, max_length=32),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultsglu",
            name="tracking_identifier",
            field=models.CharField(db_index=True, max_length=32),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultshba1c",
            name="tracking_identifier",
            field=models.CharField(db_index=True, max_length=32),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultsins",
            name="tracking_identifier",
            field=models.CharField(db_index=True, max_length=32),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultslft",
            name="tracking_identifier",
            field=models.CharField(db_index=True, max_length=32),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultslipid",
            name="tracking_identifier",
            field=models.CharField(db_index=True, max_length=32),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultsrft",
            name="tracking_identifier",
            field=models.CharField(db_index=True, max_length=32),
        ),
    ]
