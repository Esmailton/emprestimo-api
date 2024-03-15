# API REST PARA GERENCIAR EMPRESTIMO

## Visão Geral
A API é construída utilizando Django, Django REST Framework, PostgresSQL e Docker gerenciado por docker compose.

## Como Iniciar
Para configurar e iniciar o projeto, siga estes passos:
Clone o repositório:
   ```bash
    https://github.com/Esmailton/emprestimo-api.git
    cd emprestimo-api
```
Criando o ambiente e startando o projeto:
Após clonar o projeto e acessa a pasta com `cd emprestimo-api`
execute o comando `make run`  para iniciar a criação do ambiente e da start no projeto.

Obtendo um Token:

Para obter um token e ter acessar aos endpoints protegidos, você precisa acessar o endpoint de geração de token:

```bash
    Método: GET
    URL: /api/generate-token/
```
Após obter o token, você pode incluí-lo no cabeçalho Authorization de suas solicitações. Aqui está um exemplo de como obter o token usando cURL:

```bash
    curl -X GET http://localhost:8000/api/generate-token/
```
Isso retornará um token. Para usá-lo em solicitações subsequentes, adicione-o ao cabeçalho Authorization 

assim:
```bash
    Authorization: Token cbf0fca38630b210f82c1c4cf054ecfc447d2bd6
```

você pode obter toda a documentação da API no Swagger após startar o projeto:

## Documentação
```bash
http://localhost:8000/swagger`

```