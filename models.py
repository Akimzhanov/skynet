from .utils import get_data
from django.db import models
import asyncio
from fast_bitrix24 import Bitrix




class Montajnik_1C(models.Model):
    bx_id = models.CharField(max_length=20, null=True)
    fio_mont = models.TextField(max_length=200, null=True) 
    id_mont = models.TextField(max_length = 200,null=True) 

    def __str__(self):
        return str(self.fio_mont)

    def save(self, *args, **kwargs):
                
            async def main():
                if not self.bx_id:
                    webhook = "" # токен с битрикс24
                    b = Bitrix(webhook)
                    method = 'crm.deal.userfield.update'
                    params = {
                        "id": 1517,
                        'fields': {
                            "LIST": [{"VALUE": f'{self.fio_mont}'}]

                        }}

                    
                    test = await b.call(method, params)
                    return test 
                else:
                    webhook = "" # токен с битрикс24
                    b = Bitrix(webhook)
                    method = 'crm.deal.userfield.update'
                    params = {
                        "id": 1517,
                        'fields': {
                            "LIST": [{"ID": f'{self.bx_id}'},
                                {"VALUE": f'{self.fio_mont}'}]

                        }}

                    test = await b.call(method, params)
                    
                    return test                            
            asyncio.run(main())

            async def main2():

                webhook = "" # токен с битрикс24
                b = Bitrix(webhook)
                method = 'crm.deal.userfield.get'
                params = {
                    "id": 1517}

                test = await b.call(method, params)

                test2 = test['LIST']
                for i in test2:

                    if i['VALUE']==self.fio_mont:
                        print(i['ID'])
                        self.bx_id = i['ID']
            asyncio.run(main2())
            return super().save(*args, **kwargs)

    class Meta:
         verbose_name = 'Монтажники'
         verbose_name_plural = 'Монтажники'


class Bitrix_1C(models.Model):
    planado_id = models.CharField(max_length=10, null=True) 
    bx_id = models.CharField(max_length=20, null=True) 
    id_mont = models.TextField(max_length = 200,null=True) 
    ls_abon= models.TextField(max_length = 200,null=True) 
    addres = models.TextField(max_length = 500,null=True)
    date_tg = models.CharField(max_length=30, null=True)
    date_accept = models.TextField(max_length = 200,null=True)  
    ovk1 = models.TextField(max_length = 200,null=True)
    type_ovk = models.TextField(max_length=200, null=True)
    onu  = models.TextField(max_length = 200,null=True) 
    odf = models.TextField(max_length = 200,null=True)
    patchcord = models.TextField(max_length = 200,null=True) 
    router = models.TextField(max_length = 200,null=True)
    kronshtein = models.TextField(max_length = 200,null=True,blank=True)
    connecter= models.TextField(max_length = 200,null=True)
    tv = models.TextField(max_length = 200,null=True)
    utp_type = models.TextField(max_length = 200,null=True)
    utp_lenght = models.TextField(max_length = 200,null=True)
    status = models.TextField(max_length = 200,null=True, default=0)
    photo = models.URLField(max_length = 2000,blank=True,null=True)
    photo2 = models.URLField(max_length = 3000,null=True, blank=True)
    comments = models.TextField(max_length = 200,default='new',null=True, blank=True)
    money = models.TextField(max_length = 200,null=True)
    tariff = models.CharField(max_length=50, null=True)
    resolution = models.CharField(max_length=50, null=True)
    rca = models.CharField(max_length=50, null=True)
    check_one_time_servise = models.CharField(max_length=2, default=0)
    dismantling = models.CharField(max_length=20, default=0)
    montajnik = models.ForeignKey(Montajnik_1C, on_delete=models.SET_NULL, null=True, blank=True)
    sklad = models.CharField(max_length=20, default=0)

    def __str__(self):
        if self.montajnik:
            return str(self.montajnik.fio_mont)
        else:
            return self.bx_id

    def save(self, *args, **kwargs):
        if not self.date_tg:
            a = get_data()
            self.date_tg = a
        super().save(*args, **kwargs)

    class Meta:
         verbose_name = 'Отчеты монтажников'
         verbose_name_plural = 'Отчеты монтажников'


class Change_raz(models.Model):
    chislo = models.IntegerField()

    def __str__(self):
        return str(self.chislo) 










