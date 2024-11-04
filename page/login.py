import sqlite3
import streamlit as st


def Login(Email, Password):
    with sqlite3.connect('register.db') as connect:
           cursor = connect.cursor()
           
           try:
               cursor.execute("""select * from client where email = ? and password = ?""", (Email, Password))
               result = cursor.fetchone()
               if result:
                   print('login com sucesso')
               else:
                   st.error('Incorret Email or Password')
           except Exception as e:
               print('Erro:', e)

st.title('Login')
FieldEmail = st.text_input(label='Email')
FieldPassword = st.text_input(label='Password', type='password')

st.button(label='Login', on_click=lambda:Login(Email=FieldEmail, Password=FieldPassword)
        if FieldEmail and FieldPassword != ''
        else st.error('Fill in all fields'))

if st.button('Register'):
    st.session_state.page = 'register'