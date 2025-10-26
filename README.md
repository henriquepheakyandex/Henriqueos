# Henriqueos

Este é um projeto de API de gerenciamento de tarefas simples construído com Flask.

## Instalação

Para instalar as dependências, execute o seguinte comando:

```bash
pip install -r requirements.txt
```

## Executando o aplicativo

Para executar o aplicativo, execute o seguinte comando:

```bash
python src/app.py
```

## Executando os testes

Para executar os testes, execute o seguinte comando:

```bash
python -m unittest discover tests
```

## Gerador de Código

Este projeto inclui um gerador de código para criar rapidamente novos recursos de API RESTful.

### Uso

Para gerar um novo recurso, execute o seguinte comando a partir do diretório raiz do projeto:

```bash
python scripts/generate_resource.py <nome_do_recurso>
```

Substitua `<nome_do_recurso>` pelo nome do seu recurso (por exemplo, `user`, `item`).

O script irá automaticamente:
1. Criar um novo arquivo de rota em `src/routes/`.
2. Criar um novo arquivo de teste em `tests/`.
3. Registrar o novo Blueprint em `src/app.py`.

## Endpoints da API

### Tarefas

- **GET /tasks**: Obtém todas as tarefas.
- **GET /tasks/<id>**: Obtém uma única tarefa.
- **POST /tasks**: Cria uma nova tarefa.
- **PUT /tasks/<id>**: Atualiza uma tarefa.
- **DELETE /tasks/<id>**: Exclui uma tarefa.

### Produtos

- **GET /products**: Obtém todos os produtos.
- **GET /products/<id>**: Obtém um único produto.
- **POST /products**: Cria um novo produto.
- **PUT /products/<id>**: Atualiza um produto.
- **DELETE /products/<id>**: Exclui um produto.
