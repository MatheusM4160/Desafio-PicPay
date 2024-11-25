# Desafio do PicPay

---

## 📋 Funcionalidades
- Login e registro de usuários.
- Realização de transações financeiras.
- Histórico de transações detalhado.

---

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3
- **Framework Frontend:** Streamlit
- **Banco de Dados:** SQLite
- **Bibliotecas Adicionais:** 
  - `streamlit`
  - `sqlite3`
  - `pandas`

---

## 🚀 Como Rodar o Projeto

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git

2. Entre no diretório do projeto:
    ```bash
    cd nome-do-projeto

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt

4. Inicie o projeto:
    ```bash
    streamlit run app.py

---

## 📝 Estrutura do Banco de Dados

# Tabela `client`
- `id`: Identificador único.
- `name`: Nome do usuário.
- `cpf`: CPF do usuário.
- `email`: E-mail do usuário.
- `password`: Senha do usuário
- `account_type`: Tipo de conta.

# Tabela `account`

- `account_id`: ID único da conta.
- `client_id`: Referência ao cliente.
- `account_type`: Tipo de conta.
- `balance`: Saldo.
- `password`: Senha para transações.
