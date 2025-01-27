import streamlit as st
import sqlite3
import random
import requests
import time
import pandas as pd

# Pegar dados de data para utilizar na hora das transições
day = time.localtime().tm_mday
mon = time.localtime().tm_mon
year = time.localtime().tm_year
date = f'{day}/{mon}/{year}'


# Função para verifiacr o Mock
def send_notification(to, message):
    url = "https://util.devi.tools/api/v1/notify"
    payload = {"to": to, "message": message}

    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao enviar notificação: {e}")
        return None


# Criação das sessões mais importantes, a de login e a de page para navegar entre as páginas
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = 'login'


# Função para página de login
def login_page():
    # Função para verificar o login com o banco de dados
    def Login(Email, Password):
        with sqlite3.connect('register.db') as connect:
            cursor = connect.cursor()
            try:
                cursor.execute("""SELECT * FROM client WHERE email = ? AND password = ?""", (Email, Password))
                result = cursor.fetchone()
                if result:
                    st.success('Login com sucesso')
                    st.session_state.account_id = result[0]
                    st.session_state.logged_in = True
                    st.session_state.update(page='home')
                else:
                    st.error('E-mail ou senha incorretos')
            except Exception as e:
                print('Erro:', e)

    st.title('Login')
    FieldEmail = st.text_input(label='E-mail')
    FieldPassword = st.text_input(label='Senha', type='password')

    ButtonLogin = st.button(label='Login', on_click=lambda:Login(Email=FieldEmail, Password=FieldPassword)
                            if FieldEmail and FieldPassword != ''
                            else st.error('Preencha todos os campos'))

    if st.button('Registrar'):
        st.session_state.logged_in = True
        st.session_state.page = 'register'
        st.rerun()

# Função para página de registro
def register_page():
    #Função para colocar os dados do registro no banco de dados
    def Register(Name, CPF, Email, Password, AccountType):
        with sqlite3.connect('register.db') as connect:
            cursor = connect.cursor()
            CPF = CPF.replace('.', '').replace('-', '')

            try:
                TestCPF = str(CPF)
                print(TestCPF)
            except:
                return st.error('Erro. CPF inválido!')  
            try:
                cursor.execute("""INSERT INTO client (name, cpf, email, password, account_type)
                            VALUES (?, ?, ?, ?, ?)
                            """, (Name, CPF, Email, Password, AccountType))  
                connect.commit()
                
                client_id = cursor.lastrowid
                balance = random.randrange(500, 5000)

                cursor.execute("""INSERT INTO account (client_id, account_type, balance)
                               VALUES (?, ?, ?)""", (client_id, AccountType, balance))
                connect.commit()

                st.session_state.account_id = client_id

                st.success('Cadastrado com Sucesso!')
                st.session_state.logged_in = True
                st.session_state.update(page='home')
            except Exception as e:
                print('Erro:', e)

    Title = st.title('Registro')
    FieldName = st.text_input(label='Nome')
    FieldCPF = st.text_input(label='CPF', placeholder='000.000.000-00')
    FieldEmail = st.text_input(label='E-mail')
    FieldPassword = st.text_input(label='Senha', type='password')
    FieldPasswordConfirm = st.text_input(label='Confirmar Senha', type='password')
    FieldAccountType = st.selectbox(label='Tipo de usuário', options=['Usuário', 'Logista'])
    
    ButtonRegister = st.button(label='Register', on_click=lambda: Register(Name=FieldName, CPF=FieldCPF, Email=FieldEmail, Password=FieldPassword, AccountType=FieldAccountType)
                            if FieldPassword == FieldPasswordConfirm
                            else st.error('Erro. Senha diferente!'))
    if st.button('Login'):
        st.session_state.logged_in = False
        st.session_state.page = 'login'
        st.rerun()


# Função para página principal
def home_page():
    st.title("Saldo em conta:")
    with sqlite3.connect('register.db') as connect:
        # Pega o saldo da conta
        cursor = connect.cursor()
        account_id = st.session_state.account_id
        cursor.execute('SELECT * FROM account WHERE account_id == ?', (account_id,))
        result = cursor.fetchone()
        if result:
            st.subheader(result[3])
        else:
            st.error('Não estamos conseguindo acessar o valor da sua conta! Tente reiniciar o app.')

        if result[2] == 'Usuário':
            st.button(label='Transação', on_click=lambda: st.session_state.update(page='transaction_1'))
        else:
            pass

    #Cria o menu lateral da página
    if st.session_state.page == 'home':
        st.sidebar.button(label='Menu', on_click=lambda: st.session_state.update(page='home'))
        st.sidebar.button(label='Histórico de Transações', on_click=lambda: st.session_state.update(page='transaction history'))

# Função para página de primeira sessão da transação
def transaction_page1():
    st.title('Transação')
    FieldCPF = st.text_input(label='CPF', placeholder='000.000.000-00').replace('.', '').replace('-', '').strip()
    st.button(label='Voltar', on_click=lambda: st.session_state.update(page='home'))
    
    if st.button(label='Continuar'):
        with sqlite3.connect('register.db') as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM client WHERE cpf == ?', (FieldCPF,))
            result = cursor.fetchone()
            if result:
                st.session_state.Id_Client = result[0]
                st.session_state.update(page='transaction_2')
                st.rerun()  
            else:
                st.error('CPF Inválido')

# Função para página de segunda sessão da transação
def transaction_page2():
    Id_Client = st.session_state.Id_Client
    account_id = st.session_state.account_id
    FielValue = st.text_input(label='Valor', placeholder='19,90').strip().replace(',', '.')

    st.button(label='Voltar', on_click=lambda: st.session_state.update(page='transaction_1'))
    
    if st.button(label='Continuar'):
        try:
            FielValue = int(FielValue)
        except:
            st.error('Digite um valor válido')
        else:
            with sqlite3.connect('register.db') as connect:
                cursor = connect.cursor()
                cursor.execute('SELECT * FROM account WHERE client_id == ?', (account_id,))
                result = cursor.fetchone()[3]
                if result >= FielValue:
                    cursor.execute('SELECT * FROM account WHERE client_id == ?', (Id_Client,))
                    result = cursor.fetchone()[3]
                    if result:
                        st.session_state.Value = FielValue
                        st.session_state.update(page='transaction_3')
                        st.rerun()
                    else:
                        st.error('Conta não encontrada. Tente novamente mais tarde.')
                else:
                    st.error('Saldo Insuficiente!')


# Função para página de terceira sessão da transação
def transaction_page3():
    Id_Client = st.session_state.Id_Client
    account_id = st.session_state.account_id
    Value = st.session_state.Value
    with sqlite3.connect('register.db') as connect:
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM account WHERE account_id == ?', (account_id,))
        result = cursor.fetchone()[4]
        # Caso não tenha criado a senha de autenticação deve criar
        if result == None:
            st.title('Crie uma senha de até seis digitos')
            FieldPassword = st.text_input(label='', placeholder='EX: 123456').strip()
            if st.button('Continuar'):
                try:
                    FieldPassword = int(FieldPassword)
                except:
                    st.error('Senha Inválida')
                else:
                    if len(str(FieldPassword)) <= 6:
                        cursor.execute('UPDATE account SET password = ? WHERE account_id == ?', (FieldPassword, account_id))
                        st.rerun()
                    else:
                        st.error('Senha com mais de 6 digitos')
        else:
            st.title('Digite sua senha')
            FieldPassword = st.text_input(label='')
            cursor.execute('SELECT * FROM account WHERE account_id == ?', (account_id,))
            result = cursor.fetchone()[4]
            if st.button('Continuar'):
                resposta = requests.get('https://util.devi.tools/api/v2/authorize')
                resposta = resposta.json()
                try:
                    FieldPassword = int(FieldPassword)
                except:
                    st.error('Senha Inválida')
                else:
                    if result == FieldPassword and resposta['data']['authorization'] == True:
                        cursor.execute('SELECT * FROM account WHERE client_id == ?', (Id_Client,))
                        result = cursor.fetchone()[3]
                        result = result + Value
                        cursor.execute('UPDATE account SET balance = ? WHERE client_id == ?', (result, Id_Client))
                        connect.commit()
                        cursor.execute("""INSERT INTO transaction_history (id_client, get, date)
                                       VALUES(?, ?, ?)""", (Id_Client, Value, date))
                        connect.commit()


                        cursor.execute('SELECT * FROM account WHERE account_id == ?', (account_id,))
                        result = cursor.fetchone()[3]
                        result = result - Value
                        cursor.execute('UPDATE account SET balance = ? WHERE account_id == ?', (result, account_id))
                        connect.commit()
                        Value = Value*-1
                        cursor.execute("""INSERT INTO transaction_history (id_client, give, date)
                                       VALUES(?, ?, ?)""", (account_id, Value, date))
                        connect.commit()
                        st.success('Transação feita com sucesso!')
                        time.sleep(2)

                        cursor.execute("""SELECT * FROM client WHERE id = ?""", (Id_Client,))
                        result = cursor.fetchone()[3]
                        send_notification(result, f'Você recebeu um pagamento de R${float(Value):.2f}!')

                        st.session_state.update(page='home')
                        st.rerun()

                    elif resposta['data']['authorization'] == False:
                        st.error('Transação negada! Tente novamente mais tarde!')
                        time.sleep(2)
                        st.session_state.update(page='home')
                        print('FOI NEGADO!')
                        st.rerun()
                    else:
                        st.error('Senha Incorreta!')


# Função da página ver o histórico de transações
def transaction_history_page():
    account_id = st.session_state.account_id
    st.title('Hitórico')
    with sqlite3.connect('register.db') as connect:
        cursor = connect.cursor()
        cursor.execute('''SELECT give, get, date
                       FROM transaction_history
                       WHERE id_client = ?
                       ''', (account_id,))
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=['Saiu', 'Entrou', 'Data'])
        df.fillna('', inplace=True)

        st.dataframe(df)

    #Cria o menu lateral da página
    if st.session_state.page == 'transaction history':
        st.sidebar.button(label='Menu', on_click=lambda: st.session_state.update(page='home'))
        st.sidebar.button(label='Histórico de Transações', on_click=lambda: st.session_state.update(page='transaction history'))



# Lógica de mudança de páginas
if st.session_state.page == 'login' and not st.session_state.logged_in:
    login_page()
elif st.session_state.page == 'transaction_1':
    transaction_page1()
elif st.session_state.page == 'transaction_2':
    transaction_page2()
elif st.session_state.page == 'transaction_3':
    transaction_page3()
elif st.session_state.page == 'transaction history':
    transaction_history_page()
elif st.session_state.page == 'register':
    register_page()
elif st.session_state.page == 'home' and st.session_state.logged_in == True:
    home_page()
else:
    login_page()