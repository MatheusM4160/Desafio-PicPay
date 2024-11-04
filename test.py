import streamlit as st

# Inicializa a sessão
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Função para trocar de página
def change_page(page):
    st.session_state.page = page

# Página de login
def login_page():
    st.title("Login")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    
    if st.button("Login"):
        # Aqui você colocaria a lógica de autenticação
        # Por exemplo, verificar no banco de dados se o usuário existe e a senha está correta
        st.session_state.logged_in = True
        change_page('main')
        
    st.markdown("Não tem uma conta? [Registre-se](#)", unsafe_allow_html=True)
    if st.button("Registrar-se"):
        change_page('register')

# Página de registro
def register_page():
    st.title("Registro")
    nome = st.text_input("Nome")
    cpf = st.text_input("CPF")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    
    if st.button("Registrar"):
        # Aqui você adicionaria a lógica de registro
        # Como salvar os dados no banco de dados
        st.success("Conta criada com sucesso!")
        change_page('login')
    
    st.markdown("Já tem uma conta? [Faça login](#)", unsafe_allow_html=True)
    if st.button("Fazer Login"):
        change_page('login')

# Página principal (após login)
def main_page():
    st.title("Página Principal")
    st.write("Bem-vindo ao sistema!")

# Controle de navegação entre páginas
if st.session_state.page == 'login':
    login_page()
elif st.session_state.page == 'register':
    register_page()
elif st.session_state.page == 'main' and st.session_state.logged_in:
    main_page()
