def extrair_dados_de_itacoatiara():
    # PASSO 1: Gerar o novo conjunto de dados de Itacoatiara
    # - Antes estávamos considerando apenas CO_MUNICIPIO_ESC = ITA
    # - Agora vamos considerar também CO_MUNICIPIO_PROVA quando CO_MUNICIPIO_ESC for vazio
    import pandas as pd

    # Código de Itacoatiara
    ITA_CODE = '1301902'
    for ano in [2019, 2023]:
        df = pd.read_csv(f"MICRODADOS_ENEM_{ano}.csv", encoding="cp1252", delimiter=";", dtype=str)
        print(f"QTD: {ano}[GERAL]:", len(df))
        itac = df[(df["CO_MUNICIPIO_ESC"] == ITA_CODE) |
        ((df["CO_MUNICIPIO_ESC"].isna()) & (df["CO_MUNICIPIO_PROVA"] == ITA_CODE))]
        itac.to_csv(f"MD_ITA_{ano}.csv", index=False, encoding="cp1252", sep=';')

# extrair_dados_de_itacoatiara()
import pandas as pd
import streamlit as st

df_2019 = pd.read_csv(f"MD_ITA_2019.csv", encoding="cp1252", delimiter=";", dtype=str)
df_2023 = pd.read_csv(f"MD_ITA_2023.csv", encoding="cp1252", delimiter=";", dtype=str)
df = pd.concat([df_2019, df_2023], ignore_index=True)

# ========================
# Barra lateral - filtros
# ========================
st.sidebar.header("Filtros")

anos = st.sidebar.multiselect(
    "Selecione o(s) ano(s):", options=[2019, 2023], default=[2019, 2023]
)

incluir_sem_escola = st.sidebar.checkbox(
    "Incluir estudantes sem escola", value=True,
    help="Se desmarcado, alunos sem informação de escola não serão considerados."
)
if not incluir_sem_escola:
    df = df[df["CO_MUNICIPIO_ESC"] == '1301902']

sexo = st.sidebar.multiselect(
    "Sexo:", options=df["TP_SEXO"].dropna().unique(), default=df["TP_SEXO"].dropna().unique()
)

estado_civil = st.sidebar.multiselect(
    "Estado civil:", options=df["TP_ESTADO_CIVIL"].dropna().unique(), default=df["TP_ESTADO_CIVIL"].dropna().unique()
)

cor_raca = st.sidebar.multiselect(
    "Cor/Raça:", options=df["TP_COR_RACA"].dropna().unique(), default=df["TP_COR_RACA"].dropna().unique()
)

st.write(df)
st.write(len(df))