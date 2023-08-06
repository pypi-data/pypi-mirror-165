import requests
import base64
import sys

def gerar_token_de_acesso(**argumentos):
    resultado = {'status':False,'descricao':'', 'dados':{},'stack':''}
    try:
        url = argumentos.get('url',"https://apimprod.totvs.com.br/api/token")
        usuario = argumentos.get('usuario',False)
        senha = argumentos.get('senha',False)
        data_bytes = f'{usuario}:{senha}'.encode("utf-8")
        autorizacao = base64.b64encode(data_bytes)
        autorizacao = autorizacao.decode("utf-8")
        payload = "grant_type=client_credentials"
        headers = {
            'authorization': f"Basic {autorizacao}",
            'content-type': "application/x-www-form-urlencoded"
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        response_json = response.json()
        if 'error'  in response_json:
            resultado['descricao'] = 'Erro ao gerar dados'
            resultado['stack'] = f"{response_json.get('error','')}. {response_json.get('error_description','')}"
            return resultado
        print(response_json)
        access_token = response_json.get('access_token','')
        expires_in = response_json.get('expires_in',0)
        print(access_token)

        resultado['status'] = True
        resultado['descricao'] = 'Sucesso ao gerar dados'
        resultado['dados'] = response_json

    except Exception as erro:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        resultado['status'] = False
        resultado['descricao'] = 'Erro ao gerar dados.'
        resultado['stack'] = str(erro) + ' na linha ' + str(exc_tb.tb_lineno)
    finally:
      return resultado

def consultar_dados_api_zendesk(**argumentos):
    resultado = {'status':False,'descricao':'', 'dados':{},'stack':''}
    try:
        id_token_zendesk = argumentos.get('id_token_zendesk','')
        access_token = argumentos.get('access_token',False)
        url = argumentos.get('url',"https://apimprod.totvs.com.br/api/zendesk-unificada/v1.0/search")
        if access_token is False:
            resultado_token = gerar_token_de_acesso(
                usuario=argumentos.get('usuario',''),
                senha=argumentos.get('senha','')
            )
            if resultado_token['status'] is False:
                return resultado_token
            else:
                access_token = resultado_token['dados']['access_token']
        querystring = {"query":argumentos.get('query',"")}
        print(querystring)
        headers = {
            'authorization': f"Bearer {access_token}",
            'id-token-zendesk': id_token_zendesk
            }

        response_zendesk = requests.request("GET", url, headers=headers, params=querystring)
        response_zendesk_json = response_zendesk.json()
        print(response_zendesk_json)
        if 'error' in response_zendesk_json:
            resultado['descricao'] = 'Erro ao gerar dados'
            resultado['stack'] = f"Erro: {response_zendesk_json['error']}"
        else:
            resultado['status'] = True
            resultado['descricao'] = 'Sucesso ao gerar dados'
            resultado['dados'] = response_zendesk_json
    except Exception as erro:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        resultado['status'] = False
        resultado['descricao'] = 'Erro ao gerar dados.'
        resultado['stack'] = str(erro) + ' na linha ' + str(exc_tb.tb_lineno)
    finally:
      return resultado

    resultado = {'status':False, 'descricao':'', 'dados':{}, 'stack':''}
    try:
        resultado['status'] = True
        resultado['descricao'] = 'Sucesso'
    except Exception as erro:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        resultado['status'] = False
        resultado['descricao'] = 'Erro ao gerar dados.'
        resultado['stack'] = str(erro) + ' na linha ' + str(exc_tb.tb_lineno)
    finally:
        return resultado
