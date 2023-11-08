from venv import logger
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import json
import time,sys
from datetime import datetime
from .models import Bitrix_1C,Montajnik_1C
from skynet.models import Waiting
from fast_bitrix24 import Bitrix
from fast_bitrix24 import BitrixAsync
import logging
import requests
from http import HTTPStatus
from urllib import parse as urllib_parse
from django.views.decorators.csrf import csrf_exempt
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
import asyncio
from skynet.models import Tehaccepted, Tvaccepted,Tehwaiting,Tvwaiting
from django.db.models import Max
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from crm_bot.config import TOKEN2
from datetime import date, timedelta

bot = Bot(token=TOKEN2)
dp = Dispatcher(bot)


async def sms_bot(tg, com, deal_id):

        await bot.send_message(tg, f'Ваша заявка на жалобу была успешно обработана! Номер заявки: {deal_id}. Описание заявки {com}')



async def deal_for_bot(deal_id):
    webhook = "" # токен с битрикс24
    if 5==5:
        b = BitrixAsync(webhook)
        method = 'crm.deal.get'
        params = {
         "id": f'{deal_id}',
        }
        test = await b.call(method, params)
        tg = test['UF_CRM_1692786777951']
        com = test['COMMENTS']
        id_deal = test['ID']
        await sms_bot(tg, com, deal_id)
        return test



@csrf_exempt
def tg_sms(request):

     if request.method == 'POST':
        post_data = request.POST.copy()
        deal_id = post_data.get("document_id[2]")
        deal_id =str(deal_id)[5:]
        asyncio.run(deal_for_bot(deal_id))
        print(987654321)


        return HttpResponse(200)

     else:

        return HttpResponse(500)





#logging.getLogger('fast_bitrix24').addHandler(logging.StreamHandler())
webhook = "" # токен с битрикс24

async def hydra_one_time_services(deal_id,ls_abon,router,tv,ovk,utp):
        
    hoper_url = '' # api hydra
    hoper_login = '' #login hydra
    hoper_password = '' # password hydra
    http_timeout = 1000
    http_session = requests.Session()
    http_session.headers.update(
        {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
    )
    auth_url = urllib_parse.urljoin(hoper_url, 'login')
    auth_params = {'session': {'login': hoper_login, 'password': hoper_password}}
    response = http_session.post(
        auth_url,
        timeout=http_timeout,
        json=auth_params,
        verify=False,
    )

    if response.status_code != HTTPStatus.CREATED:
        logger.error(
            'Auth error ({0}): {1}'.format(response.status_code, response.content),
        )
        sys.exit(1)
   # logger.debug(response.content)

    auth_result = json.loads(response.content)
    auth_token = auth_result['session']['token']


    http_session.headers.update(
        {'Authorization': 'Token token={0}'.format(auth_token)},
    )


    organizations_url = urllib_parse.urljoin(hoper_url, f'search?query={ls_abon}''')

    response = http_session.get(
        organizations_url,
        timeout=http_timeout,
        verify=False,
        params={

        }
    )
   # print(response)
    if response.status_code == HTTPStatus.OK:

        # search_results = json.loads(response.content)
        search_results = json.loads(response.content)['search_results']
        print(search_results)
        for entity in search_results:
            customers = (entity['n_result_id'])
            account_id = (entity['n_entity_id'])
        customers = customers 
        account_id = account_id 

    else:
        logger.warning(
            'Invalid response ({0}): {1}'.format(
                response.status_code,
                response.content,
            ),
        )
    organizations_url = urllib_parse.urljoin(hoper_url, f'subjects/customers/{customers}/contracts'  '')


    response = http_session.get(
        organizations_url,
        timeout=http_timeout,
        params={

        }
    )

    if response.status_code == HTTPStatus.OK:

        search_results = json.loads(response.content)['contracts']

        service_id_hydra = search_results[0]
        contract = (service_id_hydra['n_doc_id'])



        async def one_time_service(deal_id,service_id, n_quant, n_unit_id, customers):

            now = datetime.now()
            service_id_hydra = now.strftime("%Y-%m-%dT%H:%M:%S+06:00")
            time.sleep(1)
            service_id_hydra1 = now.strftime("%Y-%m-%dT%H:%M:%S+06:00")
            organizations_url = urllib_parse.urljoin(hoper_url, f'subjects/customers/{customers}/subscriptions/')
            response = http_session.post(
                organizations_url,
                timeout=http_timeout,
                verify=False,
                json=
                {
                    "subscription": {

                        "n_service_id": service_id,
                        'n_account_id': account_id,  # licevoi schet
                        "n_contract_id": contract,
                        'n_customer_id': customers,  # id licevoi schet
                        "d_begin": f'{service_id_hydra}',
                        "d_end": f'{service_id_hydra1}',
                        'n_quant': n_quant,
                        'n_unit_id': n_unit_id,
                        "fl_one_off": "Y"

                    },

                }

            )

            print(response.status_code)
            if response.status_code == 201:
                search_results = json.loads(response.content)
                webhook = "" # токен с битрикс24
                if (service_id ==131322401):
                    type = f"Подключение 1500с ,потрачено  более 350м овк" 
                elif (service_id ==130952801):
                    type = f"UTP:  {n_quant}м." 



       
                b = BitrixAsync(webhook)
                method = 'crm.livefeedmessage.add'
                params = {'fields': {

            "POST_TITLE": "Списание ТМЦ",
            "MESSAGE": f"ТМЦ списано : {type }",
            "ENTITYTYPEID": 2,
            'ENTITYID': deal_id,


        }}
                test = await b.call(method, params)


        async def one_time_service_device(deal_id,service_id, customers):
            now = datetime.now()
            service_id_hydra = now.strftime("%Y-%m-%dT%H:%M:%S+06:00")
            time.sleep(1)
            service_id_hydra1 = now.strftime("%Y-%m-%dT%H:%M:%S+06:00")
            organizations_url = urllib_parse.urljoin(hoper_url, f'subjects/customers/{customers}/subscriptions/')
            response = http_session.post(
                organizations_url,
                timeout=http_timeout,
                verify=False,
                json=
                {

                    "subscription": {
                        # "n_service_id": 130952801,#router kabel itp
                        "n_service_id": service_id,
                        'n_account_id': account_id,  # licevoi schet
                        "n_contract_id": contract,
                        'n_customer_id': customers,  # id licevoi schet
                        "d_begin": f'{service_id_hydra}',
                        "d_end": f'{service_id_hydra1}',
                        "fl_one_off": "Y",
                      

                    },

                }

            )
            if response.status_code == 201:
                search_results = json.loads(response.content)
                webhook = "" # токен с битрикс24
                if (service_id ==51621801):
                    type = f"Роутер Tp-link за 1500 с." 
                elif (service_id ==51596501):
                    type = f"Роутер Snr за 1500 с." 
                elif (service_id ==1018257701):
                    type = f"Роутер за 2500 с." 
                elif (service_id ==52195301):
                    type = f"ТВ приставка за 3000 с." 
                elif (service_id ==131322401):
                    type = f"Подключение за 1500с ,свыше 350метров  ОВ-1" 






                print(type)
                b = BitrixAsync(webhook)
                method = 'crm.livefeedmessage.add'
                params = {'fields': {

            "POST_TITLE": "Списание ТМЦ",
            "MESSAGE": f"ТМЦ списано : {type}",
            "ENTITYTYPEID": 2,
            'ENTITYID': deal_id,


        }}
                test = await b.call(method, params)
                print("test  списание")


        if response.status_code == HTTPStatus.OK:
            search_results = json.loads(response.content)

        organizations_url = urllib_parse.urljoin(hoper_url, f'subjects/customers/{customers}/subscriptions/'  '')


        response = http_session.get(
            organizations_url,
            timeout=http_timeout,
            verify=False,
            params={

            }
        )


        router = router
        ovk = int(ovk)
        utp = float(utp)
        tv = tv
        print(router,tv,ovk)
        if response.status_code == HTTPStatus.OK:
            search_results = json.loads(response.content)['subscriptions']
            print(search_results)
            if (search_results == []):
                print("tess")
                service_id1 = 51621801  # router  tp link 1500
                service_id2 = 51596501  # router  snr 1500
                service_id3 = 1018257701  # router  tp link 2500
                service_id4 = 52195301  # router  gbox3000
                service_id5 = 794398401  # ovkA
                service_id6 = 130952801  # utp
                service_id7 = 131322401 # ovk 350 >1500c

                if (router == "Роутер TP-Link 841 выкуп" or router == "Роутер TP-Link 844 выкуп"):
                    service_id = 51621801  # type service
                    await one_time_service_device(deal_id,service_id, customers)
                if router == 'Роутер SNR выкуп':
                    service_id = 51596501  # type service
                    await one_time_service_device(deal_id,service_id, customers)
                if (router == 'Роутер TP-Link c24 выкуп' or router == 'Роутер TP-Link c54 выкуп'):
                    service_id = 1018257701  # type service

                    await   one_time_service_device(deal_id,service_id, customers)
                if (tv == 'Приставка Imaqliq Q-box выкуп' or tv == 'Приставка Imaqliq G-box выкуп'):
                    service_id = 52195301  # type service
                    #  n_unit_id = 3009# wt1009. metr3009
                    await  one_time_service_device(deal_id,service_id, customers)
                if (ovk > 350):
                     service_id = 131322401 # type service
                     n_quant = 1
                     n_unit_id = 1009
                     await   one_time_service(deal_id,service_id, n_quant, n_unit_id, customers)
                if (utp > 10):
                    service_id = 130952801  # type service
                    n_quant = utp - 10  # kol-vo
                    n_unit_id = 3009  # wt1009. metr3009
                    await  one_time_service(deal_id,service_id, n_quant, n_unit_id, customers)



            else:
                service_id_hydra = []
                for entity in search_results:
                    a = (entity['n_service_id'])

                    service_id_hydra.append(a)



                print(service_id_hydra)

                if (router == "Роутер TP-Link 841 выкуп" or router == "Роутер TP-Link 844 выкуп"):
                        service_id = 51621801  # type service
                        if (service_id not in service_id_hydra):
                               await  one_time_service_device(deal_id,service_id, customers)

                if router == 'Роутер SNR выкуп':

                        service_id = 51596501  # type service
                        if (service_id not in service_id_hydra):
                            await  one_time_service_device(deal_id,service_id, customers)

                if (router == 'Роутер TP-Link c24 выкуп' or router == 'Роутер TP-Link c54 выкуп'):

                        service_id = 1018257701  # type service
                        if (service_id not in service_id_hydra):
                             await   one_time_service_device(deal_id,service_id, customers)

                if (tv == 'Приставка Imaqliq Q-box выкуп' or tv == 'Приставка Imaqliq G-box выкуп'):
                        service_id = 52195301  # type service
                        if (service_id not in service_id_hydra):
                             await  one_time_service_device(deal_id,service_id, customers)
                print(ovk)
                if (ovk > 350):
                        service_id = 131322401 # type service
                        if (service_id not in service_id_hydra):
                             n_quant = 1
                             n_unit_id = 1009
                             await   one_time_service(deal_id,service_id, n_quant, n_unit_id, customers)

                if (utp > 10):
                        service_id = 130952801  # type service
                        if (service_id not in service_id_hydra):
                            n_quant = utp - 10  # kol-vo
                            n_unit_id = 3009  # wt1009. metr3009
                            await   one_time_service(deal_id,service_id, n_quant, n_unit_id, customers)
                                


async def teh_hydra_one_time_services(deal_id,ls_abon,type_of_work):
        
    hoper_url = '' #api hydrA
    hoper_login = '' #login hydra
    hoper_password = '' #password hydra
    http_timeout = 1000
    http_session = requests.Session()
    http_session.headers.update(
        {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
    )
    auth_url = urllib_parse.urljoin(hoper_url, 'login')
    auth_params = {'session': {'login': hoper_login, 'password': hoper_password}}
    response = http_session.post(
        auth_url,
        timeout=http_timeout,
        json=auth_params,
        verify=False,
    )

    if response.status_code != HTTPStatus.CREATED:
        logger.error(
            'Auth error ({0}): {1}'.format(response.status_code, response.content),
        )
        sys.exit(1)


    auth_result = json.loads(response.content)
    auth_token = auth_result['session']['token']
    print(auth_token)

    http_session.headers.update(
        {'Authorization': 'Token token={0}'.format(auth_token)},
    )


    organizations_url = urllib_parse.urljoin(hoper_url, f'search?query={ls_abon}''')

    response = http_session.get(
        organizations_url,
        timeout=http_timeout,
        verify=False,
        params={

        }
    )
    print(response)
    if response.status_code == HTTPStatus.OK:


        search_results = json.loads(response.content)['search_results']
        print(search_results)
        for entity in search_results:
            customers = (entity['n_result_id'])
            account_id = (entity['n_entity_id'])

    else:
        logger.warning(
            'Invalid response ({0}): {1}'.format(
                response.status_code,
                response.content,
            ),
        )
    organizations_url = urllib_parse.urljoin(hoper_url, f'subjects/customers/{customers}/contracts'  '')


    response = http_session.get(
        organizations_url,
        timeout=http_timeout,
        params={

        }
    )

    if response.status_code == HTTPStatus.OK:

        search_results = json.loads(response.content)['contracts']

        service_id_hydra = search_results[0]
        contract = (service_id_hydra['n_doc_id'])


        

        async def teh_one_time_service_device(deal_id,service_id, customers):
            now = datetime.now()
            service_id_hydra = now.strftime("%Y-%m-%dT%H:%M:%S+06:00")
            time.sleep(1)
            service_id_hydra1 = now.strftime("%Y-%m-%dT%H:%M:%S+06:00")
            organizations_url = urllib_parse.urljoin(hoper_url, f'subjects/customers/{customers}/subscriptions/')
            response = http_session.post(
                organizations_url,
                timeout=http_timeout,
                verify=False,
                json=
                {

                    "subscription": {
                        # "n_service_id": 130952801,#router kabel itp
                        "n_service_id": service_id,
                        'n_account_id': account_id,  # licevoi schet
                        "n_contract_id": contract,
                        'n_customer_id': customers,  # id licevoi schet
                        "d_begin": f'{service_id_hydra}',
                        "d_end": f'{service_id_hydra1}',
                        'n_quant': 1,
                        'n_unit_id': 1009,

                        "fl_one_off": "Y"

                    },

                }

            )
            print("******ПОДПИСКА**********")
            print(response.status_code)
            if response.status_code == 201:
                search_results = json.loads(response.content)
                webhook = "" # токен с битрикс24
                if (service_id ==6309722601):
                    type = f"Замена ONU" 
                elif (service_id ==6309796001):
                    type = f"Замена ONU (БЕСПЛАТНО)" 
                elif (service_id ==6309764101):
                    type = f"Замена БП/POE" 
                elif (service_id ==6309729801):
                    type = f"Замена ТВ-приставки" 
                elif (service_id ==6309785001):
                    type = f"Замена ТВ-приставки (БЕСТПЛАТНО)" 
                elif (service_id ==6309748101):
                    type = f"Замена патчкорда" 
                elif (service_id ==6309778301):
                    type = f"Замена пульта" 
                elif (service_id ==6309727901):
                    type = f"Замена роутера" 
                elif (service_id ==6309792901):
                    type = f"Замена роутера (БЕСПЛАТНО)" 
                elif (service_id ==5959765201):
                    type = f"Настройка роутера" 
                elif (service_id ==6309800301):
                    type = f"Настройка ТВ-приложения" 
                elif (service_id ==6309732001):
                    type = f"Переварка на муфте" 
                elif (service_id ==6309734901):
                    type = f"Переварка на муфте и у абонента" 
                elif (service_id ==6309714801):
                    type = f"Переварка у абонента" 
                elif (service_id ==6309715001):
                    type = f"Переобжатие коннектора" 
                elif (service_id ==6309737001):
                    type = f"Перетяжка абонентского кабеля" 
                elif (service_id ==6309746201):
                    type = f"Юстировка" 








       
                b = BitrixAsync(webhook)
                method = 'crm.livefeedmessage.add'
                params = {'fields': {

            "POST_TITLE": "По техподу  оказаны  следующие услуги",
            "MESSAGE": f"По техподу (домен битрикс24)/{deal_id}/  оказаны  следующие услуги: Наименование услуги: {type}",
            "ENTITYTYPEID": 2,
            'ENTITYID': deal_id,


        }}
                test = await b.call(method, params)



        if response.status_code == HTTPStatus.OK:
            search_results = json.loads(response.content)


        organizations_url = urllib_parse.urljoin(hoper_url, f'subjects/customers/{customers}/subscriptions/'  '')


        response = http_session.get(
            organizations_url,
            timeout=http_timeout,
            verify=False,
            params={

            }
        )


        router = type_of_work
        if response.status_code == HTTPStatus.OK:
            search_results = json.loads(response.content)['subscriptions']
            print(search_results)
            if (5==5):
                print("tess")
                print(router)


                if router == "Замена ONU":
                       service_id = 6309722601  # type service
                       await  teh_one_time_service_device(deal_id,service_id, customers)
                       service_id_onu = 6309796001
                       await  teh_one_time_service_device(deal_id,service_id_onu, customers)

                elif router == "Замена ONU (БЕСПЛАТНО)":
                       service_id = 6309796001
                       await  teh_one_time_service_device(deal_id,service_id, customers)

                elif router == "Замена БП/Замена PoE":
                       service_id = 6309764101
                       await  teh_one_time_service_device(deal_id,service_id, customers)

                elif router == "Замена ТВ приставки":
                       service_id = 6309729801
                       await  teh_one_time_service_device(deal_id,service_id, customers)

                elif router == "Замена ТВ приставки (БЕСПЛАТНО)":
                       service_id = 6309785001
                       await  teh_one_time_service_device(deal_id,service_id, customers)

                elif router == "Замена патчкорда":
                       service_id = 6309748101
                       await  teh_one_time_service_device(deal_id,service_id, customers)

                elif router == "Замена пульта":
                       service_id = 6309778301 #6309727901  6309817901
                       await  teh_one_time_service_device(deal_id,service_id, customers)
                       service_id_pult = 130967601
                       await  teh_one_time_service_device(deal_id,service_id_pult, customers)

                elif router == "Замена роутера":
                       service_id = 6309727901
                       await  teh_one_time_service_device(deal_id,service_id, customers)

                elif router == "Замена роутера (БЕСПЛАТНО)":
                       service_id = 6309792901
                       await  teh_one_time_service_device(deal_id,service_id, customers)

                elif router == "Настройка роутера":
                       print(router)
                       print("aasasasasa")
                       service_id = 5959765201
                       await  teh_one_time_service_device(deal_id,service_id, customers)

                elif router == "Настройка ТВ-приложения":
                       service_id = 6309731801
                       await  teh_one_time_service_device(deal_id,service_id, customers)

                elif router == "Переварка на муфте":
                       service_id = 6309732001
                       await  teh_one_time_service_device(deal_id,service_id, customers)

                elif router == "Переварка на муфте и у абонента":
                       service_id = 6309734901
                       await  teh_one_time_service_device(deal_id,service_id, customers)

                elif router == "Переварка у абонента":
                       service_id = 6309714801
                       await  teh_one_time_service_device(deal_id,service_id, customers)

                elif router == "Переобжатие коннектора":
                       service_id = 6309715001
                       await  teh_one_time_service_device(deal_id,service_id, customers)

                elif router == "Перетяжка абонентского кабеля":
                       service_id = 6309737001
                       await  teh_one_time_service_device(deal_id,service_id, customers)

                elif router == "Юстировка":
                       service_id = 6309746201
                       await  teh_one_time_service_device(deal_id,service_id, customers)

            else:
                service_id_hydra = []
                for entity in search_results:
                    a = (entity['n_service_id'])

                    service_id_hydra.append(a)



                print(service_id_hydra)

async def check_1c(bitrix_id):
    webhook = "" # токен с битрикс24
    b = BitrixAsync(webhook)
    method = 'crm.deal.update'
    params = {
        "ID": bitrix_id,
        "fields":{
            'UF_CRM_1695209211336': 'Да'
        }
    }
    test = await b.call(method, params, raw=True)

    return test

async def bitrix_1c_s(deal_id):
         if 5==5:
            print(000000000)
            b = BitrixAsync(webhook)
            method = 'crm.deal.get'
            params = {
             "id": f'{deal_id}',
               'fields': {


               }}
            test = await b.call(method, params)

            data_deal = test2 = test['UF_CRM_1678857157479']
            tariff = test['UF_CRM_1674019947476']
            router = test['UF_CRM_1674019983286']
            tv = test['UF_CRM_1674021434343']
            money = test['UF_CRM_1674020024342']
            ls_abon = test['UF_CRM_1674020039851']
            ovk = test['UF_CRM_1674024846']
            type_ovk = test['UF_CRM_1678688870894']
            utp = test['UF_CRM_1674024869']
            connecter = test['UF_CRM_1674024888']
            kronshtein = test['UF_CRM_1674024900']
            resolution = test['UF_CRM_1675112283593']
            onu1 = test['UF_CRM_1676284927600']
            onu = test['UF_CRM_1697553012305']
            odf = test['UF_CRM_1676284943120']
            rca = test['UF_CRM_1676285387280']
            bitrix_id = test['ID']
            addres = test['UF_CRM_1674993837284']
            planado_id = test['UF_CRM_1677475668343']
            photo = test['UF_CRM_1674019907309']
            patchcord = test ['UF_CRM_1677815485633']
            sklad = test ['UF_CRM_1669625413673']
            utp_type = '000000651'
            print (type(patchcord ))
            if onu == 'ONU WISPEN XPON 1GX':
                   onu = '000002084'
            elif onu =='ONU BDCOM GPON 1G'  or onu1 =='1':
                 onu = '000000009'
            else: 
               onu = '0'


            sklad = test ['UF_CRM_1669625413673']
            if sklad == '4813':
                 sklad = '000000006'
            elif sklad =='4814':
                 sklad = '000005637'
            elif sklad =='4812':
                 sklad = '000167713'
            elif sklad =='4811':
                 sklad = '000012986'
            elif sklad =='4810':
                 sklad = '000002439'
            elif sklad =='4809':
                 sklad = '000006321'


            if router == 'Роутер SNR ВП' or router =='Роутер SNR выкуп' or router =='Роутер SNR' or router =='Да ВП' or router =='Да выкуп':
                 router1 = '000000669'
            elif router =='Роутер TP-Link 841 ВП' or  router == 'Роутер TP-Link 841 выкуп' or  router == 'Роутер TP-Link 841' :
                 router1 = '000000014'
            elif router =='Роутер TP-Link 844 ВП' or  router == 'Роутер TP-Link 844 выкуп' or  router == 'Роутер TP-Link 844':
                 router1 = '000001373'  
            elif router =='Роутер TP-Link c24 выкуп' or router =='Роутер TP-Link c24':
                 router1 = '000001376'       
            elif router =='Роутер TP-Link c54 выкуп' or router =='Роутер TP-Link c54' :
                 router1 = '000001396'  
            else : router1 = '0'

            if tv  == 'Приставка Imaqliq Q-box ВП' or tv =='Приставка Imaqliq Q-box выкуп' or tv =='Приставка Imaqliq Q-box':
                 tv1 = '000000850'
            elif tv =='Приставка ВП' or  tv == 'Приставка выкуп' :
                 tv1 = '000000850'
            elif tv =='Приставка Imaqliq Q-box ВП' or  tv == 'Приставка Imaqliq Q-box выкуп' :
                 tv1 = '000000850'
            elif tv =='Приставка Imaqliq G-box ВП' or  tv == 'Приставка Imaqliq G-box выкуп' or  tv == 'Приставка Imaqliq G-box':
                 tv1 = '000001345'
            else: tv1 = '0'
            if patchcord == 'Патчкорд оптический SC-SC/UPC 2м':   
                patchcord = '000000754'
            elif patchcord =='Патчкорд оптический SC-SC/UPC 3м':
                patchcord = '000000090'
           
            if type_ovk == 'Кабель ОВК - 1 волокно':
                type_ovk = '000000113'
            elif type_ovk == 'Кабель ОВК -2 волокно':
                type_ovk = '000000799'


            async def main(deal_id):
                if 5 == 5:
                    b = BitrixAsync(webhook)
                    method = 'crm.deal.get'
                    params = {
                     "id": f'{deal_id}',
                      'fields': {


                        }}
                    test = await b.call(method, params)
                    a = test['UF_CRM_1675110342']
        

                    async def main2(a):
                         method = 'crm.deal.userfield.get'
                         params = {
                         "id": 1517}

                         test =await b.call(method, params)

                         test2 = test['LIST']
          
                         for i in test2:

                              if  i['ID']==a:
                                   return i['VALUE']

                    x = await main2(a)
                    return x
            if test['TITLE'] == 'Демонтаж':

                dismantling = '1'
            else:
                dismantling = '0'
            y = await main(deal_id)

            t=Montajnik_1C.objects.get(fio_mont=y)
            chat_id=t.id_mont

            if not Bitrix_1C.objects.filter(bx_id=bitrix_id):
                b = Bitrix_1C.objects.create(dismantling=dismantling,utp_type=utp_type,type_ovk=type_ovk, patchcord = patchcord , planado_id=planado_id,id_mont=chat_id ,date_tg=data_deal[:-15],photo=photo,kronshtein=kronshtein,addres=addres[:-2],bx_id=bitrix_id,tariff=tariff, router=router1, tv=tv1, money=money[:-4], ls_abon=ls_abon, ovk1=ovk, utp_lenght=utp, connecter=connecter , resolution=resolution, onu=onu, odf=odf,rca=rca,sklad=sklad)
                await check_1c(bitrix_id)
                await hydra_one_time_services(deal_id,ls_abon,router,tv,ovk,utp)


            else:
                
                deal_bitrix_1c = Bitrix_1C.objects.filter(bx_id=bitrix_id).update(dismantling=dismantling,utp_type=utp_type,type_ovk=type_ovk, patchcord = patchcord , planado_id=planado_id,id_mont=chat_id, photo=photo,kronshtein=kronshtein,addres=addres[:-2],bx_id=bitrix_id,tariff=tariff, router=router1, tv=tv1, money=money[:-4], ls_abon=ls_abon, ovk1=ovk, utp_lenght=utp, connecter=connecter , resolution=resolution, onu=onu, odf=odf,rca=rca,sklad=sklad)
                print (deal_bitrix_1c)
                deal_bitrix_1c.save()
           


@csrf_exempt
def bitrix_1c(request):

     if request.method == 'POST':
        post_data = request.POST.copy()
        deal_id = post_data.get("document_id[2]")
        deal_id =str(deal_id)[5:]
        asyncio.run(bitrix_1c_s(deal_id))


        return HttpResponse(200)

     else:

        return HttpResponse(500)




async def main(deal_id):
    if 5 == 5:
        b = BitrixAsync(webhook)
        method = 'crm.deal.get'
        params = {
         "id": f'{deal_id}',
          'fields': {
            }}
        test = await b.call(method, params)
        a = test['UF_CRM_1675110342']
        async def main2(a):
             method = 'crm.deal.userfield.get'
             params = {
             "id": 1517}
             test =await b.call(method, params)
             test2 = test['LIST']

             for i in test2:
                  if  i['ID']==a:
                       return i['VALUE']
        x = await main2(a)
        return x




@csrf_exempt
def teh_1c(request):

     if request.method == 'POST':
        post_data = request.POST.copy()
        deal_id = post_data.get("document_id[2]")
        deal_id =str(deal_id)[5:]
        asyncio.run(bitrix_teh(deal_id))


        return HttpResponse(200)

     else:

        return HttpResponse(500)



async def bitrix_teh(deal_id):
    b = BitrixAsync(webhook)
    method = 'crm.deal.get'
    params = {
      'id': f'{deal_id}',
        'fields':{}}
    data_deal = await b.call(method, params)

    bx_id = data_deal['ID']
    ls_abon = data_deal['UF_CRM_1673255771']
    addres = data_deal['UF_CRM_1674993837284']
    date_close = data_deal['UF_CRM_1685356551883']
    ovk1 = data_deal['UF_CRM_1681124615212']
    onu1 = data_deal['UF_CRM_1676284927600']
    onu = data_deal['UF_CRM_1697553012305']
    odf = data_deal['UF_CRM_1676284943120']
    patchcord = data_deal['UF_CRM_1677815485633']
    router = data_deal['UF_CRM_1674019983286']
    kronshtein = data_deal['UF_CRM_1674024900']
    connecter = data_deal['UF_CRM_1674024888']
    tv = data_deal['UF_CRM_1674021434343']
    utp_type = '000000651'
    utp_length = data_deal['UF_CRM_1674024869']
    status = '0'
    title = data_deal['UF_CRM_1677475668343']
    photo = data_deal['UF_CRM_1683019024843']
    comments = data_deal['COMMENTS']
    money = data_deal['UF_CRM_1674020024342']
    type_ovk = data_deal['UF_CRM_1678688870894']
    type_of_work = data_deal['UF_CRM_1678770251758']
    dismantling = '2'

    sklad = data_deal['UF_CRM_1669625413673']
    if sklad == '4813':
         sklad = '000000006'
    elif sklad =='4814':
         sklad = '000005637'
    elif sklad =='4812':
         sklad = '000167713'
    elif sklad =='4811':
         sklad = '000012986'
    elif sklad =='4810':
         sklad = '000002439'
    elif sklad =='4809':
         sklad = '000006321'

    #списание  за тмц в  техподах

    if onu == 'ONU WISPEN XPON 1GX':
               onu = '000002084'
    elif onu =='ONU BDCOM GPON 1G'  or onu1 =='1':
                 onu = '000000009'
    else: 
       onu = '0'
    

    if router == 'Роутер SNR ВП' or router =='Роутер SNR выкуп' or router =='Да ВП' or router =='Да выкуп':
         router1 = '000000669'
    elif router =='Роутер TP-Link 841 ВП' or  router == 'Роутер TP-Link 841 выкуп' :
         router1 = '000000014'
    elif router =='Роутер TP-Link 844 ВП' or  router == 'Роутер TP-Link 844 выкуп' :
         router1 = '000001373'  
    elif router =='Роутер TP-Link c24 выкуп' :
         router1 = '000001376'       
    elif router =='Роутер TP-Link c54 выкуп' :
         router1 = '000001396'  
    else : router1 = ''
    if tv  == 'Приставка Imaqliq Q-box ВП' or tv =='Приставка Imaqliq Q-box выкуп':
         tv1 = '000000850'
    elif tv =='Приставка ВП' or  tv == 'Приставка выкуп' :
         tv1 = '000000850'
    elif tv =='Приставка Imaqliq Q-box ВП' or  tv == 'Приставка Imaqliq Q-box выкуп' :
         tv1 = '000000850'
    elif tv =='Приставка Imaqliq G-box ВП' or  tv == 'Приставка Imaqliq G-box выкуп' :
         tv1 = '000001345'
    else: tv1 = ''
    if patchcord == 'Патчкорд оптический SC-SC/UPC 2м':   
        patchcord = '000000754'
    elif patchcord =='Патчкорд оптический SC-SC/UPC 3м':
        patchcord = '000000090'
    else:
        patchcord = '0'
    
    if type_ovk == 'Кабель ОВК - 1 волокно':
        type_ovk = '000000113'
    elif type_ovk == 'Кабель ОВК -2 волокно':
        type_ovk = '000000799'


    y = await main(deal_id)
    print(y)
    print(type(y))
    t=Montajnik_1C.objects.get(fio_mont=y)
    chat_id=t.id_mont



    if not Bitrix_1C.objects.filter(bx_id=bx_id):
        tehpod = Bitrix_1C.objects.create(dismantling=dismantling,bx_id=bx_id, id_mont=chat_id, ls_abon=ls_abon, addres=addres[:-2], date_tg=date_close[:-15], ovk1=ovk1, onu=onu, odf=odf, patchcord=patchcord, router=router1, kronshtein=kronshtein, connecter=connecter, tv=tv1, utp_type=utp_type, status=status,utp_lenght=utp_length, planado_id=title, photo=photo,  comments=comments, money=money[:-4],type_ovk=type_ovk,sklad=sklad)
        print("*********************"+type_of_work)
        await teh_hydra_one_time_services(deal_id,ls_abon,type_of_work)
        print("*********************"+type_of_work)
    else:
        teh_bitrix_1c = Bitrix_1C.objects.filter(bx_id=bx_id).update(dismantling=dismantling,id_mont=chat_id, ls_abon=ls_abon, addres=addres[:-2], date_tg=date_close[:-15], ovk1=ovk1, onu=onu, odf=odf, patchcord=patchcord, router=router1, kronshtein=kronshtein, connecter=connecter, tv=tv1, utp_type=utp_type, status=status,utp_lenght=utp_length, planado_id=title, photo=photo,  comments=comments, money=money[:-4],type_ovk=type_ovk,sklad=sklad)
        teh_bitrix_1c.save()



@csrf_exempt
def date_tehpod(request):

     if request.method == 'POST':
        post_data = request.POST.copy()
        deal_id = post_data.get("document_id[2]")
        deal_id =str(deal_id)[5:]
        asyncio.run(date_tp(deal_id))


        return HttpResponse(200)

     else:

        return HttpResponse(500)




async def date_tp(deal_id):
    webhook = "" # токен с битрикс24
    b = BitrixAsync(webhook)
    method = 'crm.deal.get'
    params = {
      'id': f'{deal_id}',
        'fields':{}}
    data_deal = await b.call(method, params)

    bx_id = data_deal['ID']
    ls_abon = data_deal['UF_CRM_1673255771']
      
    hoper_url = '' #api hydra
    hoper_login = '' #login hydra
    hoper_password = '' #login hydra
    http_timeout = 1000
    http_session = requests.Session()
    http_session.headers.update(
        {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
    )
    auth_url = urllib_parse.urljoin(hoper_url, 'login')
    auth_params = {'session': {'login': hoper_login, 'password': hoper_password}}
    response = http_session.post(
        auth_url,
        timeout=http_timeout,
        json=auth_params,
        verify=False,
    )

    if response.status_code != HTTPStatus.CREATED:
        logger.error(
            'Auth error ({0}): {1}'.format(response.status_code, response.content),
        )
        sys.exit(1)
    logger.debug(response.content)

    auth_result = json.loads(response.content)
    auth_token = auth_result['session']['token']


    http_session.headers.update(
        {'Authorization': 'Token token={0}'.format(auth_token)},
    )


    organizations_url = urllib_parse.urljoin(hoper_url, f'search?query={ls_abon}''')

    response = http_session.get(
        organizations_url,
        timeout=http_timeout,
        verify=False,
        params={

        }
    )
    print(response)
    if response.status_code == HTTPStatus.OK:


        search_results = json.loads(response.content)['search_results']
        print(search_results)
        for entity in search_results:
            customers = (entity['n_result_id'])
            
    else:
        logger.warning(
            'Invalid response ({0}): {1}'.format(
                response.status_code,
                response.content,
            ),
        )
    organizations_url = urllib_parse.urljoin(hoper_url, f'subjects/customers/{customers}/subscriptions'  '')


    response = http_session.get(
        organizations_url,
        timeout=http_timeout,
        params={

        }
    )

    if response.status_code == HTTPStatus.OK:

        search_results = json.loads(response.content)['subscriptions']
        service_id_hydra = search_results[0]
        for entity in search_results:
           d_begin = (entity['d_begin'][:10])
           print(d_begin)
           break
        webhook = "" # токен с битрикс24
        b = BitrixAsync(webhook)
        print (d_begin)
        method = 'crm.deal.update'
        params = {
        "ID": bx_id,
        "fields":{
            'UF_CRM_1678857157479': f'{d_begin}'
        }
    }
        test = await b.call(method, params, raw=True)

        return test



@csrf_exempt
def tv_1c(request):
     if request.method == 'POST':
        post_data = request.POST.copy()
        deal_id = post_data.get("document_id[2]")
        deal_id =str(deal_id)[5:]
        print(deal_id)

        asyncio.run(bitrix_tv(deal_id))

        return HttpResponse(200)

     else:

        return HttpResponse(500)

async def bitrix_tv(deal_id):
    b = BitrixAsync(webhook)
    method = 'crm.deal.get'
    params = {
      'id': f'{deal_id}',
        'fields':{}}
    data_deal = await b.call(method, params)
    print(data_deal)

    bx_id = data_deal['ID']
    ls_abon = data_deal['UF_CRM_1673255771']
    addres = data_deal['UF_CRM_1674993837284']
    date_close = data_deal['UF_CRM_1685356551883']
    ovk1 = '0'
    onu = '0'
    odf = '0'
    patchcord = '0'
    router = data_deal['UF_CRM_1674019983286']
    kronshtein = '0'
    connecter = data_deal['UF_CRM_1674024888']
    tv = data_deal['UF_CRM_1674021434343']
    utp_type = '000000651'
    utp_length = data_deal['UF_CRM_1674024869']
    status = '0'
    title = data_deal['UF_CRM_1677475668343']
    photo = data_deal['UF_CRM_1674019907309']
    comments = data_deal['COMMENTS']
    money = data_deal['UF_CRM_1674020024342']
    dismantling = '3'
    sklad = data_deal['UF_CRM_1669625413673']
    if sklad == '4813':
          sklad = '000000006'
    elif sklad =='4814':
        sklad = '000005637'
    elif sklad =='4812':
        sklad = '000167713'
    elif sklad =='4811':
        sklad = '000012986'
    elif sklad =='4810':
        sklad = '000002439'
    elif sklad =='4809':
      sklad = '000006321'



    if router == 'Роутер SNR ВП' or router =='Роутер SNR выкуп' or router =='Да ВП' or router =='Да выкуп':
         router1 = '000000669'
    elif router =='Роутер TP-Link 841 ВП' or  router == 'Роутер TP-Link 841 выкуп' :
         router1 = '000000014'
    elif router =='Роутер TP-Link 844 ВП' or  router == 'Роутер TP-Link 844 выкуп' :
         router1 = '000001373'  
    elif router =='Роутер TP-Link c24 выкуп' :
         router1 = '000001376'       
    elif router =='Роутер TP-Link c54 выкуп' :
         router1 = '000001396'  
    else : router1 = ''
    if tv  == 'Приставка Imaqliq Q-box ВП' or tv =='Приставка Imaqliq Q-box выкуп':
         tv1 = '000000850'
    elif tv =='Приставка ВП' or  tv == 'Приставка выкуп' :
         tv1 = '000000850'
    elif tv =='Приставка Imaqliq Q-box ВП' or  tv == 'Приставка Imaqliq Q-box выкуп' :
         tv1 = '000000850'
    elif tv =='Приставка Imaqliq G-box ВП' or  tv == 'Приставка Imaqliq G-box выкуп' :
         tv1 = '000001345'
    else: tv1 = ''


    y = await main(deal_id)
    print(y)
    print(type(y))
    t=Montajnik_1C.objects.get(fio_mont=y)
    chat_id=t.id_mont

  


    if not Bitrix_1C.objects.filter(bx_id=bx_id):
        tehpod = Bitrix_1C.objects.create(dismantling=dismantling,bx_id=bx_id, id_mont=chat_id, ls_abon=ls_abon, addres=addres[:-2], date_tg=date_close[:-15], ovk1=ovk1, onu=onu, odf=odf, patchcord=patchcord, router=router1, kronshtein=kronshtein, connecter=connecter, tv=tv1, utp_type=utp_type, status=status,utp_lenght=utp_length, planado_id=title, photo=photo,  comments=comments, money=money[:-4],sklad=sklad)
 
        ovk = 0
        utp_length = int(utp_length) + 10
        utp_length = str (utp_length)
        await hydra_one_time_services(deal_id,ls_abon,router,tv,ovk,utp_length)



    else:
        teh_bitrix_1c = Bitrix_1C.objects.filter(bx_id=bx_id).update(dismantling=dismantling,id_mont=chat_id, ls_abon=ls_abon, addres=addres[:-2], date_tg=date_close[:-15], ovk1=ovk1, onu=onu, odf=odf, patchcord=patchcord, router=router1, kronshtein=kronshtein, connecter=connecter, tv=tv1, utp_type=utp_type, status=status,utp_lenght=utp_length, planado_id=title, photo=photo,  comments=comments, money=money[:-4],sklad=sklad)
        teh_bitrix_1c.save()








            

