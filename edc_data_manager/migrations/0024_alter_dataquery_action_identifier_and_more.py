# Generated by Django 4.0.7 on 2022-08-23 13:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("edc_data_manager", "0023_auto_20220704_1841"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dataquery",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name="historicaldataquery",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50),
        ),
    ]
