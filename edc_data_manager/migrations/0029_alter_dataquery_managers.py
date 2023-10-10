# Generated by Django 4.2.1 on 2023-07-07 19:32

from django.db import migrations
import django.db.models.manager
import edc_sites.model_mixins


class Migration(migrations.Migration):
    dependencies = [
        (
            "edc_data_manager",
            "0028_alter_dataquery_options_alter_queryrule_options_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="dataquery",
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("on_site", edc_sites.model_mixins.CurrentSiteManager()),
            ],
        ),
    ]