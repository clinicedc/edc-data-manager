# Generated by Django 3.0.4 on 2020-03-27 11:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("edc_data_manager", "0015_auto_20200227_2327"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalqueryrule",
            name="rule_handler_name",
            field=models.CharField(
                choices=[("do_nothing", "Do Nothing"), ("default", "Default")],
                default="default",
                max_length=150,
            ),
        ),
        migrations.AlterField(
            model_name="queryrule",
            name="rule_handler_name",
            field=models.CharField(
                choices=[("do_nothing", "Do Nothing"), ("default", "Default")],
                default="default",
                max_length=150,
            ),
        ),
    ]
