Os requerimentos para baixar estão no requirements.txt

# API de Helpdesk

API REST para o controle de chamados de suporte, feita com Flask, SQLAlchemy e SQLite.
O projeto foi organizado em camadas (controller / service / repository / model), de forma
que cada camada tenha uma responsabilidade só.

## Estrutura

```
helpdesk/
├── controllers/                 recebem a requisição e devolvem a resposta HTTP
│   ├── usuario_controller.py
│   └── chamado_controller.py
├── services/                    regras de negócio e validações
│   ├── usuario_service.py
│   └── chamado_service.py
├── repositories/                consultas no banco com SQLAlchemy
│   ├── usuario_repository.py
│   └── chamado_repository.py
├── models/                      entidades do banco
│   ├── usuario.py
│   └── chamado.py
├── database.py                  conexão e criação das tabelas
└── app.py                       cria a aplicação e registra as rotas
```

A ideia da separação é: o controller não sabe nada de regra de negócio, o service não
conhece Flask nem código HTTP, e o repository só faz consulta (nenhuma validação).
Quando um service precisa recusar uma operação ele levanta uma exceção (definida em
`services/__init__.py`), e cada controller captura essa exceção e devolve o código
HTTP certo.

## Como executar

Requisitos: Python 3.10 ou superior.

```bash
# 1. criar e ativar o ambiente virtual (opcional, mas recomendado)
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / macOS

# 2. instalar as dependências
pip install -r requirements.txt

# 3. rodar a aplicação (a partir da pasta raiz do projeto)
python -m helpdesk.app
```

A API sobe em `http://127.0.0.1:5000`.

O banco `helpdesk.db` é criado automaticamente na raiz do projeto na primeira execução.
Ele já vem junto com a entrega com alguns registros de exemplo — se quiser começar do
zero, é só apagar o arquivo e rodar de novo.

## Entidades

**Usuário:** `id`, `nome`, `email`, `setor`

**Chamado:** `id`, `titulo`, `descricao`, `prioridade`, `status`, `tecnico`,
`data_abertura`, `usuario_id`

Um usuário pode ter vários chamados; cada chamado pertence a um único usuário.

## Endpoints

### Usuários

| Método | Rota | Descrição |
|---|---|---|
| GET | `/usuarios` | Lista todos os usuários |
| GET | `/usuarios/<id>` | Busca um usuário |
| POST | `/usuarios` | Cadastra um usuário |
| PUT | `/usuarios/<id>` | Atualiza um usuário |
| DELETE | `/usuarios/<id>` | Remove um usuário |
| GET | `/usuarios/<id>/chamados` | Lista os chamados de um usuário |

### Chamados

| Método | Rota | Descrição |
|---|---|---|
| GET | `/chamados` | Lista todos os chamados |
| GET | `/chamados/<id>` | Busca um chamado |
| POST | `/chamados` | Abre um chamado |
| PUT | `/chamados/<id>` | Atualiza um chamado |
| DELETE | `/chamados/<id>` | Remove um chamado |
| PATCH | `/chamados/<id>/iniciar` | Muda o status para "Em atendimento" |
| PATCH | `/chamados/<id>/encerrar` | Muda o status para "Encerrado" |
| GET | `/chamados/abertos` | Lista só os chamados abertos |
| GET | `/chamados/prioridade/alta` | Lista os chamados de prioridade alta |

## Regras de negócio

**Usuários**

- Nome e e-mail são obrigatórios.
- Não pode haver dois usuários com o mesmo e-mail.
- Um usuário que possui chamados cadastrados não pode ser excluído.

**Chamados**

- Título obrigatório e com no mínimo 5 caracteres.
- Descrição com no mínimo 10 caracteres.
- O chamado precisa estar vinculado a um usuário que exista.
- A prioridade só pode ser `Baixa`, `Média` ou `Alta` (aceita sem acento e em minúsculo,
  mas é gravada no formato correto).
- O status inicial é sempre `Aberto`.
- Um usuário não pode ter mais de 5 chamados de prioridade `Alta` que ainda não estejam
  encerrados. Essa mesma checagem vale quando um chamado é alterado para `Alta`.

**Transições de status**

Só são aceitos estes dois caminhos:

```
Aberto → Em atendimento → Encerrado
```

Qualquer outra tentativa (`Aberto → Encerrado`, `Encerrado → Aberto`,
`Encerrado → Em atendimento`) é recusada com `409`. O status também não pode ser
alterado pelo `PUT`, justamente para que essas transições não sejam burladas — ele muda
só pelos endpoints `iniciar` e `encerrar`.

## Códigos HTTP utilizados

| Código | Quando |
|---|---|
| 200 | Consulta ou atualização feita com sucesso |
| 201 | Registro criado |
| 204 | Registro excluído (sem corpo na resposta) |
| 400 | Dados inválidos ou faltando |
| 404 | Registro ou rota inexistente |
| 405 | Método não permitido na rota |
| 409 | Conflito de regra (e-mail repetido, transição inválida, limite de chamados) |

## Exemplos

Cadastrar um usuário:

```bash
curl -X POST http://127.0.0.1:5000/usuarios \
  -H "Content-Type: application/json" \
  -d "{\"nome\": \"Ana Souza\", \"email\": \"ana@empresa.com\", \"setor\": \"Financeiro\"}"
```

Abrir um chamado:

```bash
curl -X POST http://127.0.0.1:5000/chamados \
  -H "Content-Type: application/json" \
  -d "{\"titulo\": \"Impressora travando\", \"descricao\": \"A impressora do setor nao imprime.\", \"prioridade\": \"Alta\", \"usuario_id\": 1}"
```

Colocar em atendimento e depois encerrar:

```bash
curl -X PATCH http://127.0.0.1:5000/chamados/1/iniciar
curl -X PATCH http://127.0.0.1:5000/chamados/1/encerrar
```

Quando alguma regra é violada, a resposta vem no formato:

```json
{
  "erro": "O título deve ter pelo menos 5 caracteres."
}
```
