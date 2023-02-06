# Generated by Django 3.2.6 on 2021-09-21 01:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("edc_data_manager", "0019_auto_20210510_2036"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataquery",
            name="locked_reason",
            field=models.TextField(
                blank=True,
                help_text="If required, the reason the query cannot be resolved.",
                null=True,
                verbose_name="Reason query locked",
            ),
        ),
        migrations.AddField(
            model_name="historicaldataquery",
            name="locked_reason",
            field=models.TextField(
                blank=True,
                help_text="If required, the reason the query cannot be resolved.",
                null=True,
                verbose_name="Reason query locked",
            ),
        ),
    ]
