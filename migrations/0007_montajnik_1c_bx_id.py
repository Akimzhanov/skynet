# Generated by Django 3.1.7 on 2023-03-04 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bitrix_report_1c', '0006_auto_20230303_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='montajnik_1c',
            name='bx_id',
            field=models.CharField(max_length=20, null=True),
        ),
    ]