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

## Endpoints da API

### Obter todas as tarefas

-   **GET /tasks**
-   **Resposta de sucesso:**
    ```json
    {
      "tasks": [
        {
          "id": 1,
          "title": "Buy groceries",
          "description": "Milk, Cheese, Pizza, Fruit, Tylenol",
          "done": false
        }
      ]
    }
    ```

### Obter uma tarefa

-   **GET /tasks/<task_id>**
-   **Resposta de sucesso:**
    ```json
    {
      "task": {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, Cheese, Pizza, Fruit, Tylenol",
        "done": false
      }
    }
    ```
-   **Resposta de erro (404 Not Found):** Se a tarefa não existir.

### Criar uma tarefa

-   **POST /tasks**
-   **Corpo da solicitação:**
    ```json
    {
      "title": "New Task Title",
      "description": "New Task Description"
    }
    ```
-   **Resposta de sucesso (201 Created):**
    ```json
    {
      "task": {
        "id": 3,
        "title": "New Task Title",
        "description": "New Task Description",
        "done": false
      }
    }
    ```
-   **Resposta de erro (400 Bad Request):** Se o título estiver ausente.

### Atualizar uma tarefa

-   **PUT /tasks/<task_id>**
-   **Corpo da solicitação:**
    ```json
    {
      "title": "Updated Title",
      "description": "Updated Description",
      "done": true
    }
    ```
-   **Resposta de sucesso:**
    ```json
    {
      "task": {
        "id": 1,
        "title": "Updated Title",
        "description": "Updated Description",
        "done": true
      }
    }
    ```
-   **Resposta de erro (404 Not Found):** Se a tarefa não existir.

### Excluir uma tarefa

-   **DELETE /tasks/<task_id>**
-   **Resposta de sucesso:**
    ```json
    {
      "result": true
    }
    ```
-   **Resposta de erro (404 Not Found):** Se a tarefa não existir.
