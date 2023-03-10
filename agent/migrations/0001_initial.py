# Generated by Django 4.1.6 on 2023-02-15 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Supervizer",
            fields=[
                (
                    "region",
                    models.CharField(
                        choices=[
                            ("Chui", "Чуйская"),
                            ("Ysyk_kol", "Ысык-колская"),
                            ("Naryn", "Нарынская"),
                            ("Jalal_abad", "Джалал-Абадская"),
                            ("Batken", "Баткенская"),
                            ("Osh", "Ошская"),
                            ("Talas", "Таласская"),
                        ],
                        max_length=50,
                    ),
                ),
                ("supervizer_id", models.BigIntegerField(default=0)),
                (
                    "supervizer_surname",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Agent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bx_id", models.CharField(default=6666, max_length=50)),
                ("teleid", models.CharField(max_length=50)),
                ("supervizer", models.CharField(blank=True, max_length=10)),
                ("surname", models.CharField(max_length=50)),
                (
                    "supervizer_surname",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="super_id",
                        to="agent.supervizer",
                    ),
                ),
            ],
        ),
    ]
