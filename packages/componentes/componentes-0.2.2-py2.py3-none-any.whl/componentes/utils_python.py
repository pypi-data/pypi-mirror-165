"""
Componente de uso de diversas funcionalidades do python.
Como por exemplo: instalar pacotes, gerar e instalar
arquivo requiriments.txt
"""

import subprocess

def install(**argumentos):
    """Função destinada a instalar pacotes

    params:
        - pacote: (string) Informe o pacote para instalar
            exemplo: install(pacote='pandas')

        - pacotes: (list) Informe a lista de pacotes para instalar
            exemplo: install(pacotes=['pandas','numpy'])
    return:
        Não possui retorno
    """
    pacote = argumentos.get('pacote',False)
    pacotes = argumentos.get('pacotes',False)
    if pacote:
        subprocess.call(f'pip install {pacote}')
    if pacotes:
        for pacote in pacotes:
            subprocess.call(f'pip install {pacote}')

def gerar_requiriments():
    r"""Função olhando para todos os arquivos da pasta atual,
    destinada gerar automaticamente o arquivo requirements.txt

    params:
        Não possui parametros

    return:
        Não possui retorno
    """
    install(pacote='pipreqs')
    subprocess.call('pipreqs --debug --use-local --force')
