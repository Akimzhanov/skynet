# Generated by Django 3.1.7 on 2023-02-24 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bitrix_1C',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bx_id', models.CharField(max_length=20, null=True)),
                ('title', models.CharField(default='SOME STRING', max_length=30)),
                ('tip_podkl', models.TextField(max_length=200, null=True)),
                ('id_mont', models.TextField(max_length=200, null=True)),
                ('ls_abon', models.TextField(max_length=200, null=True)),
                ('addres', models.TextField(max_length=500, null=True)),
                ('date_tg', models.TextField(max_length=200, null=True)),
                ('date_accept', models.TextField(max_length=200, null=True)),
                ('ovk1', models.TextField(max_length=200, null=True)),
                ('onu', models.TextField(max_length=200, null=True)),
                ('odf', models.TextField(max_length=200, null=True)),
                ('patchcord', models.TextField(max_length=200, null=True)),
                ('router', models.TextField(max_length=200, null=True)),
                ('kronshtein', models.TextField(blank=True, max_length=200, null=True)),
                ('connecter', models.TextField(max_length=200, null=True)),
                ('tv', models.TextField(max_length=200, null=True)),
                ('utp_type', models.TextField(max_length=200, null=True)),
                ('utp_lenght', models.TextField(max_length=200, null=True)),
                ('status', models.TextField(max_length=200, null=True)),
                ('photo', models.URLField(blank=True, max_length=2000, null=True)),
                ('photo2', models.URLField(blank=True, max_length=3000, null=True)),
                ('comments', models.TextField(blank=True, default='new', max_length=200, null=True)),
                ('money', models.TextField(max_length=200, null=True)),
                ('tariff', models.CharField(max_length=50, null=True)),
                ('resolution', models.CharField(max_length=50, null=True)),
                ('rca', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
