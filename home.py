import streamlit as st
import pandas as pd
import plotly.express as px


# Função para carregar dados
def carregar_dados():
    df_2019 = pd.read_csv("MD_ITA_2019.csv", sep=";", encoding="latin1")
    df_2023 = pd.read_csv("MD_ITA_2023.csv", sep=";", encoding="latin1")
    return df_2019, df_2023

df_2019, df_2023 = carregar_dados()

# Adiciona coluna de ano e combina os dados dos dois anos para análise
df_2019["ANO"] = 2019
df_2023["ANO"] = 2023
df_final = pd.concat([df_2019, df_2023], ignore_index=True)

# -=-=-=-=-=-=-=-=-=-
# Criação da Barra Lateral
# -=-=-=-=-=-=-=-=-=-
st.sidebar.header("Filtros")

#Seleção dos filtros dos anos de 2019 e 2023
anos = st.sidebar.multiselect(
    "Selecione o(s) ano(s):",
    options=[2019, 2023],
    default=[2019, 2023]
)
# Filtra os dados de acordo com os anos selecionados
df_filtrado = df_final[df_final["ANO"].isin(anos)]

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Checkbox na barra lateral
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=
incluir_sem_escola = st.sidebar.checkbox(
    "Incluir alunos sem escola",
    value=True,
    help="Se desmarcado, alunos sem informação de escola não serão considerados."
)

if not incluir_sem_escola and "CO_MUNICIPIO_ESC" in df_filtrado.columns:
    # Remove os alunos sem escola
    df_filtrado = df_filtrado[df_filtrado["CO_MUNICIPIO_ESC"].notna()]

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Título e cabeçalho
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=
st.title("Análise Social")
st.header("Microdados do Exame Nacional do Ensino Médio")

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Criação das abas Dados Gerais, pessoais, escolares de renda, moradia, transporte e aparelhos e tecnologias em casa
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=
tabs = st.tabs([
    "Dados Gerais",
    "Dados Pessoais",
    "Depêndencia Administrativa",
    "Dados de Renda",
    "Dados de Moradia",
    "Dados de Transporte",
    "Aparelhos e Tecnologias Digitais"
])

#-=-=-=-=-=-=-=-=-=-
# Dados gerais
# --=-=-=-=-=-=-=-=-
with tabs[0]:
    df_inscritos = df_filtrado  # todos os inscritos, sem filtro
    if not df_inscritos.empty:
        contagem = (
            # AGRUPA DADOS PELAS COLUNAS / Conta o número de linhas em cada grupo / Transforma o resultado em um novo DF com duas colunas de ano e quantidade
            df_inscritos.groupby("ANO").size().reset_index(name="Quantidade")
        )
        fig = px.bar(
            contagem,
            x="ANO",
            y="Quantidade",
            text="Quantidade",
            title="Quantidade de inscritos no ENEM por ano"
        )
        st.plotly_chart(fig)
    else:
        st.warning("Não há dados para os anos selecionados.")

#-=-=-=-=
# Dados pessoais
# -=-=-=-=-=-=-=-
with tabs[1]:
    # pegando somente a coluna sexo
    dados = df_filtrado["TP_SEXO"].dropna().unique()
    # Opções de sexo disponíveis
    sexos_selecionados = st.sidebar.multiselect(
        "Sexo:",
        options=dados,
        default=dados
    )

    # filtrando os dados com o sexo escolhido masculino ou feminino
    filtrado = df_filtrado[df_filtrado["TP_SEXO"].isin(sexos_selecionados)]
    #substitui M e F por Masculino e feminino
    if "TP_SEXO" in filtrado:
        #troca os valores de TP_SEXO
        filtrado["TP_SEXO"] = filtrado["TP_SEXO"].replace({
            "M": "Masculino",
            "F": "Feminino"
        })
    #criando o gráfico de pizza com os dados filtrados
    graf_pizza = px.pie(
        filtrado,
        names="TP_SEXO",
        hole=0.3,
        title="Paticipantes por sexo"
    )
    st.plotly_chart(graf_pizza)

#-=-=-=-=-=-=-=-=-=-=-=-==-=
# TIPO DE ESCOLA
#-=-=-=-=-=-=-=-=-=-=-=-=-=-
with tabs[2]:
    # opções de tipo de escola
    dados = df_filtrado["TP_DEPENDENCIA_ADM_ESC"].dropna().unique()
    escola_selecionada = st.sidebar.multiselect(
        "Tipo de Escola:",
        options=dados,
        default=dados
    )
    # filtra os dados
    filtrado_escola = df_filtrado[df_filtrado["TP_DEPENDENCIA_ADM_ESC"].isin(escola_selecionada)]
    # conta os tipos de escola e padroniza os valores de 1,2,3 e 4 para o tipo de escola
    if "TP_DEPENDENCIA_ADM_ESC" in filtrado_escola.columns:
        filtrado_escola["TP_DEPENDENCIA_ADM_ESC"] = filtrado_escola["TP_DEPENDENCIA_ADM_ESC"].replace({
            1: "Federal",
            2: "Estadual",
            3: "Municipal",
            4: "Privada"
        })
    # muda na parte inferior do gráfico o nome TP_ESCOLA para dependência administrativa
    contagem = (
        filtrado_escola["TP_DEPENDENCIA_ADM_ESC"].value_counts().reset_index()
    )
    contagem.columns = ["Dependência administrativa", "Quantidade"]
    #Grafico de barras
    grafico = px.bar(
        contagem,
        x="Dependência administrativa",
        y="Quantidade",
        text="Quantidade",
        title="Quantidade de inscritos por tipo de escola"
    )
    st.plotly_chart(grafico)

#=-=-=-=-=-=-=-=-=-=-=-=-=
# Dados de Renda
#=-=-=-=-=-=-=-=-=-=-=-=-=
with tabs[3]:
    # criando uma paleta de cores para renda
    paleta_renda = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2",
        "#7f7f7f", "#bcbd22", "#17becf", "#393b79", "#637939", "#8c6d31", "#843c39",
        "#7b4173", "#5254a3", "#9c9ede"
    ]
    # Mapeamento dos valores de Q006 para mudar as letras para o nome de A a Q
    mapa_renda = {
        "A": "Nenhuma renda",
        "B": "Até R$ 1.320,00",
        "C": "De R$ 1.320,01 até R$ 1.980,00",
        "D": "De R$ 1.980,01 até R$ 2.640,00",
        "E": "De R$ 2.640,01 até R$ 3.300,00",
        "F": "De R$ 3.300,01 até R$ 3.960,00",
        "G": "De R$ 3.960,01 até R$ 5.280,00.",
        "H": "De R$ 5.280,01 até R$ 6.600,00.",
        "I": "De R$ 6.600,01 até R$ 7.920,00",
        "J": "De R$ 7.920,01 até R$ 9240,00",
        "K": "De R$ 9.240,01 até R$ 10.560,00",
        "L": "De R$ 10.560,01 até R$ 11.880,00",
        "M": "De R$ 11.880,01 até R$ 13.200,00",
        "N": "De R$ 13.200,01 até R$ 15.840,00",
        "O": "De R$ 15.840,01 até R$19.800,00",
        "P": "De R$ 19.800,01 até R$ 26.400,00",
        "Q": "Acima de R$ 26.400,00"

    }
    # Substitui diretamente na coluna renomeando as letras pelas faixas de renda pelo meio do mapa_renda
    df_filtrado["Q006"] = df_filtrado["Q006"].replace(mapa_renda)
    # Para o multiselect, pega valores únicos já traduzidos
    dados_renda = df_filtrado["Q006"].dropna().unique()
    renda_selecionado = st.sidebar.multiselect(
        "Renda",
        options=dados_renda,
        default=dados_renda
    )
    # Contagem dos dados filtrados
    renda = df_filtrado["Q006"].value_counts().reset_index()
    renda.columns = ["Dados de Renda", "Quantidade"]
    # Gráfico de renda
    grafico_renda = px.bar(
        renda,
        x="Dados de Renda",
        y="Quantidade",
        text="Quantidade",
        color="Dados de Renda", # para que cada cor vá para uma faixa de renda diferente
        color_discrete_map={r: c for r, c in zip(renda["Dados de Renda"], paleta_renda)}
    )
    st.plotly_chart(grafico_renda)

#-=-=-=-=-=-=-=-=-=-=-=-=-=
# Aba 4 - Dados de moradia
#-=-=-=-=-=-=-=-=-=-=-=-=-=
with tabs[4]:
    moradia_dados = df_filtrado["Q005"].dropna().unique()
    # Contagem dos dados filtrados
    moradia = df_filtrado["Q005"].value_counts().reset_index()
    grafico = px.pie(
        moradia,
        names="Q005",
        values="Q005",
        hole=0.3
    )
    st.plotly_chart(grafico)

with tabs[5]:
    st.subheader("Dados de Transporte - Carros")
    veiculos_map = {
        "A": "Não",
        "B": "Sim, um",
        "C": "Sim, dois",
        "D": "Sim, três",
        "E": "Sim, quatro ou mais"
    }
    # Mapear os códigos carro
    df_filtrado["Q010"] = df_filtrado["Q010"].map(veiculos_map)

    #mapear códigos moto
    df_filtrado["Q011"] = df_filtrado["Q011"].map(veiculos_map)
    #contar quantos  em cada categoria de carros
    contagem_carro = df_filtrado["Q010"].value_counts().reset_index()
    contagem_carro.columns = ["Dados de Transporte", "Quantidade"]

    # contar quantos em cada categoria de motos
    contagem_moto = df_filtrado["Q011"].value_counts().reset_index()
    contagem_moto.columns = ["Dados de Transporte", "Quantidade"]

    #gráfico de carros
    grafico_veiculos = px.bar(
        contagem_carro,
        x="Dados de Transporte",
        y="Quantidade",
        text="Quantidade"
    )
    # Gráfico Carros
    st.plotly_chart(grafico_veiculos)

    #gráfico de motos
    st.subheader("Dados de Transporte - Moto")
    grafico_motos = px.bar(
        contagem_moto,
        x="Dados de Transporte",
        y="Quantidade",
        text="Quantidade"
    )
    # Gráfico Carros
    st.plotly_chart(grafico_motos)
