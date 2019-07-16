# Generated by Django 2.2.2 on 2019-07-16 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("edc_data_manager", "0009_auto_20190713_2119")]

    operations = [
        migrations.AlterUniqueTogether(
            name="datadictionary", unique_together={("model", "field_name")}
        ),
        migrations.AddIndex(
            model_name="queryrule",
            index=models.Index(
                fields=["title", "active"], name="edc_data_ma_title_c3118f_idx"
            ),
        ),
    ]
