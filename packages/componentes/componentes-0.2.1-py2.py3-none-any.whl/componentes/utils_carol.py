"""
- Arquivo destinado a armazenar funções de uso padrão para:

 > Chamadas na carol
 > Consulta de dados
 > Envio de resultado de logs
 > Alteração de dados

"""
from pymongo import MongoClient
from pycarol import ApiKeyAuth, Carol, Staging
from pycarol.bigquery import BQ
import pandas as pd
import sys
import os
import nest_asyncio

nest_asyncio.apply()
def enviar_para_carol(**argumentos):
    r"""
    Função destinada a enviar dados para a carol
    """
    resultado = {'status':False,'descricao':''}
    try:
      print('Enviando dados para a Carol')
      dados = argumentos.get('dados',{})
      argumentos['dados'] = {}
      argumentos = {**argumentos, **dados}
      print(argumentos)
      tenant_name = argumentos.get('tenant_name','')
      app_name=argumentos.get('app_name','')
      auth_key=argumentos.get('auth_key','')
      connector=argumentos.get('connector','')
      organization=argumentos.get('organization','')
      stagin_table = argumentos.get('stagin_table','')
      df_dados = argumentos.get('df',False)
      step_size = argumentos.get('step_size',1000)
      async_send = argumentos.get('async_send',True)
      max_workers = argumentos.get('max_workers',8)
      print(argumentos)

      carol = Carol(domain=tenant_name,
                  app_name=app_name,
                  auth=ApiKeyAuth(api_key=auth_key),
                  connector_id=connector, organization=organization)
      staging = Staging(carol)
      print(f'Enviando para a Carol')
      staging.send_data(
        staging_name=stagin_table,
        data = df_dados,
        step_size = step_size,
        connector_id=connector,
        async_send=async_send,
        max_workers=max_workers)
      resultado['status'] = True
      resultado['descricao'] = 'Dados enviados para a Carol com Sucesso'
    except Exception as erro:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        resultado['status'] = False
        resultado['descricao'] = 'Erro ao enviar para a Carol.' + str(erro) + ' na linha ' + str(exc_tb.tb_lineno) + ' da função: ' + __name__
    finally:
      return resultado


def consultar_query_carol_bq(**argumentos):
  resultado = {'status':False,'descricao':'Erro ao consultar na Carol','dados':{},'stack':''}
  try:
    carol = Carol(domain=argumentos.get('TENANT_NAME',''),
      app_name=argumentos.get('APP_NAME',''),
      auth=ApiKeyAuth(api_key=argumentos.get('X_AUTH_KEY','')),
      connector_id=argumentos.get('CONNECTOR',''),
      organization=argumentos.get('ORGANIZATION','')
      )
    bq = BQ(carol)
    df = bq.query(argumentos.get('query',''), return_dataframe=True)
    resultado['status'] = True
    resultado['descricao'] = 'Sucesso ao consultar dados'
    resultado['dados'] = df
  except Exception as erro:
          exc_type, exc_obj, exc_tb = sys.exc_info()
          resultado['status'] = False
          resultado['descricao'] = 'Erro ao enviar para a Carol.'
          resultado['stack'] = 'Erro:' + str(erro) + ' na linha ' + str(exc_tb.tb_lineno) + ' da função: ' + __name__
  finally:
        return resultado
