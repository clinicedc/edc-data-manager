# Generated by Django 2.2.3 on 2019-09-17 19:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("edc_data_manager", "0006_auto_20190917_2133")]

    operations = [
        migrations.AlterField(
            model_name="datadictionary",
            name="model",
            field=models.CharField(help_text="label_lower", max_length=250),
        ),
        migrations.AlterField(
            model_name="historicaldatadictionary",
            name="model",
            field=models.CharField(help_text="label_lower", max_length=250),
        ),
    ]
