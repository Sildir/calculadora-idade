import streamlit as st
import datetime
import pandas as pd
import os

ARQUIVO = 'dados.csv'

st.title("Calculadora de Idade")

# Entradas
nome = st.text_input("Digite seu nome:")
data_nascimento_str = st.text_input("Digite sua data de nascimento (DD/MM/YYYY):")

# Função para calcular idade
def calcular_idade(data_nascimento_str):
    try:
        data_nascimento = datetime.datetime.strptime(data_nascimento_str, "%d/%m/%Y").date()
        hoje = datetime.date.today()
        idade = hoje.year - data_nascimento.year
        if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
            idade -= 1
        return idade
    except ValueError:
        st.error("Formato de data inválido. Use DD/MM/YYYY.")
        return None

# Processamento e exibição
if nome and data_nascimento_str:
    idade = calcular_idade(data_nascimento_str)
    if idade is not None:
        hoje = datetime.date.today()
        st.success(f"{nome}, sua idade é {idade} anos.")

        # Salva os dados no CSV
        novo_dado = pd.DataFrame([{
            "Data da Consulta": hoje.strftime("%Y-%m-%d"),
            "Nome": nome,
            "Data de Nascimento": data_nascimento_str,
            "Idade": idade
        }])

        if os.path.exists(ARQUIVO):
            dados_antigos = pd.read_csv(ARQUIVO)
            dados = pd.concat([dados_antigos, novo_dado], ignore_index=True)
        else:
            dados = novo_dado

        dados.to_csv(ARQUIVO, index=False)

# -------------------
# Visualização dos dados

st.header("📊 Histórico de Consultas")

# Filtros
opcao = st.selectbox("Filtrar por:", ["Todos", "Hoje", "Esta Semana", "Este Mês", "Este Ano"])

# Leitura
if os.path.exists(ARQUIVO):
    df = pd.read_csv(ARQUIVO)
    df['Data da Consulta'] = pd.to_datetime(df['Data da Consulta'])

    hoje = pd.to_datetime(datetime.date.today())

    if opcao == "Hoje":
        df = df[df['Data da Consulta'].dt.date == hoje.date()]
    elif opcao == "Esta Semana":
        semana_atual = hoje.isocalendar()[1]
        df = df[df['Data da Consulta'].dt.isocalendar().week == semana_atual]
    elif opcao == "Este Mês":
        df = df[(df['Data da Consulta'].dt.month == hoje.month) & (df['Data da Consulta'].dt.year == hoje.year)]
    elif opcao == "Este Ano":
        df = df[df['Data da Consulta'].dt.year == hoje.year]

    st.dataframe(df)
else:
    st.info("Nenhuma consulta registrada ainda.")
