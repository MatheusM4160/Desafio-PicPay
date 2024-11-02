import sqlite3
import streamlit as st

def Register(Name, CPF, Email, Password):
    with sqlite3.connect('register.db') as connect:
        cursor = connect.cursor()


    CPF = CPF.replace('.', '').replace('-', '')

    try:
        TestCPF = str(CPF)
        print(TestCPF)
    except:
        return st.error('Error. CPF invalid!')
    

    try:
        cursor.execute("""insert into client (name, cpf, email, password)
                       values (?, ?, ?, ?)
                       """, (Name, CPF, Email, Password))
        
        connect.commit()
        st.success('Cadastrado com Sucesso!')
    except sqlite3.IntegrityError as e:
        print('Error:', e)
    except Exception as e:
        print('Error:', e)

Title = st.title('Register')
FieldName = st.text_input(label='Name')
FieldCPF = st.text_input(label='CPF', placeholder='000.000.000-00')
FieldEmail = st.text_input(label='E-mail')
FieldPassword = st.text_input(label='Password', type='password')
FieldPasswordConfirm = st.text_input(label='Confirm Password', type='password')

ButtonRegister = st.button(label='Register', on_click=lambda: Register(Name=FieldName, CPF=FieldCPF, Email=FieldEmail, Password=FieldPassword)
                           if FieldPassword == FieldPasswordConfirm
                           else st.error('Error. Password difference!'))