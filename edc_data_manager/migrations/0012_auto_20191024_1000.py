# Generated by Django 2.2.6 on 2019-10-24 07:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("edc_data_manager", "0011_auto_20191018_2220")]

    operations = [
        migrations.AlterField(
            model_name="dataquery",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.Site",
            ),
        )
    ]
