# Generated by Django 2.2.3 on 2019-09-17 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edc_data_manager', '0005_auto_20190826_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datadictionary',
            name='help_text',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='historicaldatadictionary',
            name='help_text',
            field=models.TextField(null=True),
        ),
    ]
