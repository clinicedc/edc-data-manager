# Generated by Django 3.2.13 on 2022-07-04 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_data_manager", "0022_alter_dataquery_recipients_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="historicaldatadictionary",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Data Dictionary Item",
                "verbose_name_plural": "historical Data Dictionary Items",
            },
        ),
        migrations.AlterModelOptions(
            name="historicaldataquery",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Data Query",
                "verbose_name_plural": "historical Data Queries",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalqueryrule",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Query Rule",
                "verbose_name_plural": "historical Query Rules",
            },
        ),
        migrations.AlterField(
            model_name="historicaldatadictionary",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicaldataquery",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalqueryrule",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
    ]
