from django.db import models


class Supervizer(models.Model):

    REGION_CHOICES = (
        ('Chui', 'Чуйская'),
        ('Ysyk_kol', 'Ысык-колская'),
        ('Naryn', 'Нарынская'),
        ('Jalal_abad', 'Джалал-Абадская'),
        ('Batken', 'Баткенская'),
        ('Osh', 'Ошская'),
        ('Talas', 'Таласская')
    )

    region = models.CharField(max_length=50, choices=REGION_CHOICES)
    supervizer_id = models.BigIntegerField(default=0000)
    supervizer_surname = models.CharField(max_length=100, primary_key=True)

    def __str__(self) -> str:
        return self.supervizer_surname

    

class Agent(models.Model):


    bx_id = models.CharField(max_length=50, default=6666)
    teleid = models.CharField(max_length=50)
    supervizer = models.CharField(max_length=10, blank=True)
    surname = models.CharField(max_length=50)
    supervizer_surname = models.ForeignKey(
        to=Supervizer,
        on_delete=models.CASCADE,
        related_name='super_id'
    )  

    def __str__(self) -> str:
        return self.surname








