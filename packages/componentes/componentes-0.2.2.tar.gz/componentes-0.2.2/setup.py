# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['componentes']

package_data = \
{'': ['*']}

install_requires = \
['nest_asyncio>=1,<2',
 'numpy>=1.22.2,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pycarol>=2.54.0,<3.0.0',
 'pymongo>=4.1.0,<5.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'componentes',
    'version': '0.2.2',
    'description': 'Componetes de uso de teste',
    'long_description': '# Documentação\n\n___\n\n## Sustentação de componente\n<details>\n  <summary>Criando ou atualizando componente</summary>\n\n### Como criar um pacote de pip install\n\n### 1. Criar conta no https://pypi.org/\n\n### 2. Gerar Token (Account settings)\n\n### 3. Pip install poetry\n\n### 4. Gerar um novo projeto\n    - Abra o terminal dentro do diretorio relacionado\n    - Utilizar comando `poetry new nome_projeto`\n    - Acesse a pasta do projeto criado (usando cd)\n    - registre o token gerado no projeto com o comando `poetry config pypi-token.pypi token_gerado`\n    - Alterando informações no arquivo `pyproject.toml`\n        -- Adicione o nome, descrição, autor(ficara visivel no Pypi) e informações que desejar\n        -- Adicione as dependencias usando no terminal `poetry add nome_pacote` ou adicione dentro de `pyproject.toml` abaixo da linha tool.poetry.dependencies\n        -- Altere a versão caso seja uma atualização\n    - No arquivo _init_.py altere a versão caso seja uma atualização\n    - Na pasta do projeto: Adicione os arquivos necessários\n    - No terminal: digite `poetry build` para compilar e gerar o diretorio dist com os arquivos zipados\n    - No terminal: digite `poetry publish` e o pacote será criado ou atualizado\n  Obs: É importante alterar a versão no `pyproject.toml` sempre que for alterar o projeto\n</details>\n\n___\n',
    'author': 'Bruno S',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
