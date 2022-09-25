# Generated by Django 3.2.13 on 2022-08-25 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_data_manager", "0025_edcpermissions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dataquery",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="historicaldataquery",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
    ]