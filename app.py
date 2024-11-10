import streamlit as st
import sqlite3
import random

# Inicializa o estado de autenticação
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = 'login'  # Começa na página de login

# Função para exibir a página de login
def login_page():
    def Login(Email, Password):
        with sqlite3.connect('register.db') as connect:
            cursor = connect.cursor()
            
            try:
                cursor.execute("""select * from client where email = ? and password = ?""", (Email, Password))
                result = cursor.fetchone()
                if result:
                    st.success('Login com sucesso')
                    st.session_state.logged_in = True
                    st.session_state.page = 'home'
                else:
                    st.error('Incorret Email or Password')
            except Exception as e:
                print('Erro:', e)

    st.title('Login')
    FieldEmail = st.text_input(label='Email')
    FieldPassword = st.text_input(label='Password', type='password')

    ButtonLogin = st.button(label='Login', on_click=lambda:Login(Email=FieldEmail, Password=FieldPassword)
                            if FieldEmail and FieldPassword != ''
                            else st.error('Fill in all fields'))
    
    if st.button('Registrar'):
        st.session_state.logged_in = True
        st.session_state.page = 'register'
        st.rerun()

# Função para exibir a página de registro
def register_page():
    def Register(Name, CPF, Email, Password, AccountType):
        with sqlite3.connect('register.db') as connect:
            cursor = connect.cursor()

            CPF = CPF.replace('.', '').replace('-', '')

            try:
                TestCPF = str(CPF)
                print(TestCPF)
            except:
                return st.error('Error. CPF invalid!')
                
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

                st.success('Cadastrado com Sucesso!')
                st.session_state.logged_in = True
                st.session_state.page = 'home'
            except Exception as e:
                print('Error:', e)


    Title = st.title('Register')
    FieldName = st.text_input(label='Name')
    FieldCPF = st.text_input(label='CPF', placeholder='000.000.000-00')
    FieldEmail = st.text_input(label='E-mail')
    FieldPassword = st.text_input(label='Password', type='password')
    FieldPasswordConfirm = st.text_input(label='Confirm Password', type='password')
    FieldAccountType = st.selectbox(label='Tipo de usuário', options=['Usuário', 'Logista'])

    ButtonRegister = st.button(label='Register', on_click=lambda: Register(Name=FieldName, CPF=FieldCPF, Email=FieldEmail, Password=FieldPassword, AccountType=FieldAccountType)
                            if FieldPassword == FieldPasswordConfirm
                            else st.error('Error. Password difference!'))
    if st.button('Login'):
        st.session_state.logged_in = False
        st.session_state.page = 'login'
        st.rerun()

# Função para exibir a página inicial (Home)
def home_page():
    st.title("Saldo em conta:")
    # Continuar escrevendo a logica
    if st.session_state.page == 'home':
        st.sidebar.button("Home", on_click=lambda: st.session_state.update(page='home'))
        st.sidebar.button("Ir para Registro", on_click=lambda: st.session_state.update(page='T'))
    

# Controle de navegação entre páginas
if st.session_state.page == 'login' and not st.session_state.logged_in:
    login_page()
elif st.session_state.page == 'register':
    register_page()
elif st.session_state.page == 'home' and st.session_state.logged_in:
    home_page()
else:
    login_page()
