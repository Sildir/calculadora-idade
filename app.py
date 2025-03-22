import streamlit as st
import datetime

def calcular_idade(data_nascimento_str):
    try:
        data_nascimento = datetime.datetime.strptime(data_nascimento_str, "%d/%m/%Y").date()
        hoje = datetime.date.today()
        idade = hoje.year - data_nascimento.year
        if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
            idade -= 1
        return idade
    except ValueError:
        st.error("Formato de data inválido. Por favor, use DD/MM/YYYY.")
        return None

st.title("Calculadora de Idade")

nome = st.text_input("Digite seu nome:")
data_nascimento_str = st.text_input("Digite sua data de nascimento (DD/MM/YYYY):")

if nome and data_nascimento_str:
    idade = calcular_idade(data_nascimento_str)
    if idade is not None:
        st.success(f"{nome}, sua idade é {idade} anos.")
