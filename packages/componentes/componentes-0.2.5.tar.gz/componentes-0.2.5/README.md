# Documentação

___

## Sustentação de componente
<details>
  <summary>Criando ou atualizando componente</summary>

### Como criar um pacote de pip install

### 1. Criar conta no https://pypi.org/

### 2. Gerar Token (Account settings)

### 3. Pip install poetry

### 4. Gerar um novo projeto
    - Abra o terminal dentro do diretorio relacionado
    - Utilizar comando `poetry new nome_projeto`
    - Acesse a pasta do projeto criado (usando cd)
    - registre o token gerado no projeto com o comando `poetry config pypi-token.pypi token_gerado`
    - Alterando informações no arquivo `pyproject.toml`
        -- Adicione o nome, descrição, autor(ficara visivel no Pypi) e informações que desejar
        -- Adicione as dependencias usando no terminal `poetry add nome_pacote` ou adicione dentro de `pyproject.toml` abaixo da linha tool.poetry.dependencies
        -- Altere a versão caso seja uma atualização
    - No arquivo _init_.py altere a versão caso seja uma atualização
    - Na pasta do projeto: Adicione os arquivos necessários
    - No terminal: digite `poetry build` para compilar e gerar o diretorio dist com os arquivos zipados
    - No terminal: digite `poetry publish` e o pacote será criado ou atualizado
  Obs: É importante alterar a versão no `pyproject.toml` sempre que for alterar o projeto
</details>

___
