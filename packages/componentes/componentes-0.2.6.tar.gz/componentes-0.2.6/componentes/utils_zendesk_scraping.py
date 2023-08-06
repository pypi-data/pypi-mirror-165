import requests
import base64
import sys
import numpy as np
import pandas as pd
import requests
import warnings
import sys
from pymongo import MongoClient
from pycarol import ApiKeyAuth, Carol, Staging
from pycarol.bigquery import BQ
import json
from pathlib import Path
import pandas as pd


def extrair_dados_zendesk(cookies, url, principal='results'):
    resultado = {'status':False, 'descricao':'', 'dados':{}, 'stack':''}
    try:
        print('Extraindo dados da Zendesk')
        response = requests.get(url, cookies=cookies)
        resp_json = json.loads(response.text)
        possui_prox_pag = resp_json.get('meta',{}).get('has_more',False)
        print(f'Quantidade de registros encontrados: {len(resp_json.get(principal,{}))}')
        if possui_prox_pag is True:
            print('Possui proxima Página')
            url_proxima_pagina = resp_json.get('links',{}) .get('next','')
            contador = 2
            i =1
            for i in range(contador):
                print(f'Percorrendo página: {i+1}')
                if len(resp_json.get(principal,{}))>0 and possui_prox_pag is True:
                    if(url_proxima_pagina!=''):
                        print(f'Consultando: {url_proxima_pagina}')
                        response = requests.get(url_proxima_pagina, cookies=cookies)
                        resp_json_nova_pag = response.json()
                        print(f'Quantidade de registros encontrados: {len(resp_json_nova_pag.get(principal,{}))}')
                        possui_prox_pag = resp_json.get('meta',{}).get('has_more',False)
                        if len(resp_json_nova_pag.get(principal,{}))>0:
                            resp_json = unir_jsons(resp_json_nova_pag, resp_json)
                            url_proxima_pagina = resp_json_nova_pag.get('links',{}) .get('next','')
                        if possui_prox_pag is True:
                            contador += 1
                        else:
                            break
                    else:
                        break
                else:
                    print('Não foram encontrados registros')
                    break
        print('Não possui mais proximas páginas')
        resultado['dados'] =  resp_json
        resultado['status'] = True
        resultado['descricao'] = 'Sucesso ao extrair dados'
    except Exception as erro:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        resultado['status'] = False
        resultado['dados'] = {}
        resultado['descricao'] = 'Erro ao gerar dados.'
        resultado['stack'] = str(erro) + ' na linha ' + str(exc_tb.tb_lineno)
    finally:
        return resultado


def unir_jsons(json1, json2):
    json3= {}
    for i in json1:
        if type(json1[i]) is list:
            json3[i] = json1[i] + json2[i]
        if type(json1[i]) is dict:
            json3[i] = {**json1[i], **json2[i]}
    return json3