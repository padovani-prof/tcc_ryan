import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np



# ========================
# Função para padronizar colunas e valores
# ========================
def padronizar_colunas(df):
    colunas_map = {
        "TP_SEXO": "Sexo",
        "TP_ESTADO_CIVIL": "Estado Civil",
        "TP_COR_RACA": "Cor/Raça",
        "TP_DEPENDENCIA_ADM_ESC": "Dependência Administrativa",
        # Caso já estejam com os nomes finais, não há problema
        "Sexo": "Sexo",
        "Estado Civil": "Estado Civil",
        "Cor/Raça": "Cor/Raça",
        "Dependência Administrativa": "Dependência Administrativa",
    }

    df = df.rename(columns=colunas_map)

    # ----------------------------
    # Padronizar valores da coluna Sexo
    # ----------------------------
    if "Sexo" in df.columns:
        df["Sexo"] = df["Sexo"].replace({
            "M": "Masculino",
            "F": "Feminino"
        })

    # ----------------------------
    # Padronizar valores da coluna Estado Civil
    # ----------------------------
    if "Estado Civil" in df.columns:
        df["Estado Civil"] = df["Estado Civil"].replace({
            0: "Não informado",
            1: "Solteiro(a)",
            2: "Casado(a)/Mora com companheiro(a)",
            3: "Divorciado(a)/Separado(a)",
            4: "Viúvo(a)"
        })

    # ----------------------------
    # Padronizar valores da coluna Cor/Raça
    # ----------------------------
    if "Cor/Raça" in df.columns:
        df["Cor/Raça"] = df["Cor/Raça"].replace({
            0: "Não declarado",
            1: "Branca",
            2: "Preta",
            3: "Parda",
            4: "Amarela",
            5: "Indígena"
        })

    # ----------------------------
    # Padronizar valores da Dependência Administrativa
    # ----------------------------
    if "Dependência Administrativa" in df.columns:
        df["Dependência Administrativa"] = df["Dependência Administrativa"].replace({
            1: "Federal",
            2: "Estadual",
            3: "Municipal",
            4: "Privada"
        })

    return df


# ========================
# Carregar dados (só uma vez)
# ========================
if "df" not in st.session_state:
    # Carregar os dados de 2019
    df_2019 = pd.read_csv("MD_ITA_2019.csv", sep=";", encoding='latin1')
    df_2019["Ano"] = 2019
    df_2019 = padronizar_colunas(df_2019)

    # Carregar os dados de 2023
    try:
        df_2023 = pd.read_csv("MD_ITA_2023.csv", sep=";", encoding='latin1')
    except FileNotFoundError:
        df_2023 = pd.read_excel("MICRODADOS_ITA_2023_FILTRADO.xlsx")

    df_2023["Ano"] = 2023
    df_2023 = padronizar_colunas(df_2023)

    # Concatenar em um único dataframe
    df = pd.concat([df_2019, df_2023], ignore_index=True)

    # Simular alguns alunos sem escola (NaN na dependência administrativa)
    mask = np.random.choice([True, False], size=len(df), p=[0.1, 0.9])
    df.loc[mask, "Dependência Administrativa"] = None

    # Guardar no session_state
    st.session_state["df"] = df
else:
    df = st.session_state["df"]

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

sexo = st.sidebar.multiselect(
    "Sexo:", options=df["Sexo"].dropna().unique(), default=df["Sexo"].dropna().unique()
)

estado_civil = st.sidebar.multiselect(
    "Estado civil:", options=df["Estado Civil"].dropna().unique(), default=df["Estado Civil"].dropna().unique()
)

cor_raca = st.sidebar.multiselect(
    "Cor/Raça:", options=df["Cor/Raça"].dropna().unique(), default=df["Cor/Raça"].dropna().unique()
)

# ========================
# Aplicar filtros
# ========================
df_filtrado = df[df["Ano"].isin(anos)]
df_filtrado = df_filtrado[df_filtrado["Sexo"].isin(sexo)]
df_filtrado = df_filtrado[df_filtrado["Estado Civil"].isin(estado_civil)]
df_filtrado = df_filtrado[df_filtrado["Cor/Raça"].isin(cor_raca)]

if not incluir_sem_escola:
    df_filtrado = df_filtrado[df_filtrado["CO_MUNICIPIO_ESC"]== 1301902]

# ========================
# Título e cabeçalho
# ========================
st.title("Análise social")
st.header("Microdados do Exame Nacional do Ensino Médio")

# ========================
# Layout com abas
# ========================
tabs = st.tabs([
    "Dados gerais",
    "Dados pessoais",
    "Dados escolares",
    "Dados de renda",
    "Dados de moradia",
    "Dados de transporte",
    "Dados de aparelhos e tecnologias digitais"
])

# ------------------------
# Aba 1 - Dados gerais
# ------------------------
with tabs[0]:
    st.subheader("Dados gerais")
    total = len(df_filtrado)
    st.metric("Total de inscritos", total)

    fig = px.bar(
        df_filtrado.groupby("Ano").size().reset_index(name="Quantidade"),
        x="Ano", y="Quantidade", text="Quantidade",
        title="Quantidade de inscritos por ano"
    )
    fig.update_traces(textposition="outside")

    #ajuste para não cortar os valores
    fig.update_layout(
        yaxis=dict(automargin=True),
        margin=dict(l=50, r=50, b=50, t=80, pad=0),
    )
    st.plotly_chart(fig, use_container_width=True)

# ------------------------
# Aba 2 - Dados pessoais
# ------------------------
with tabs[1]:
    st.subheader("Dados pessoais")

    # ------------------------
    # Análise por sexo
    # ------------------------
    with st.expander("Análise por sexo"):
        col1, col2 = st.columns(2)

        # Gráfico de pizza - geral
        with col1:
            fig_pizza = px.pie(
                df_filtrado, names="Sexo", hole=0.3,
                title="Distribuição geral por sexo"
            )
            fig_pizza.update_traces(
                textinfo="percent+label",
                texttemplate="%{label}<br>%{percent:.2%}",
                hovertemplate="%{label}<br>%{percent:.2%}<br>N = %{value}",
                insidetextorientation='radial'
            )
            fig_pizza.update_layout(
                margin=dict(t=80, b=50, l=50, r=50)
            )
            st.plotly_chart(fig_pizza, use_container_width=True)

        # Gráfico de barras - por ano
        with col2:
            df_percent = (
                df_filtrado.groupby(["Ano", "Sexo"]).size().reset_index(name="Quantidade")
            )
            df_percent["Percentual"] = df_percent.groupby("Ano")["Quantidade"].transform(lambda x: 100 * x / x.sum())

            fig_bar = go.Figure()
            for sexo in df_percent["Sexo"].unique():
                df_sexo = df_percent[df_percent["Sexo"] == sexo]
                fig_bar.add_trace(go.Bar(
                    x=df_sexo["Ano"],
                    y=df_sexo["Percentual"],
                    name=sexo,
                    text=[f"{v:.2f}%" for v in df_sexo["Percentual"]],
                    textposition="outside"
                ))

            fig_bar.update_layout(
                barmode='group',
                title="Percentual de inscritos por sexo e ano",
                yaxis=dict(automargin=True, range=[0, df_percent["Percentual"].max() * 1.15]),
                margin=dict(t=80, b=50, l=50, r=50)
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    # ------------------------
    # Análise por estado civil
    # ------------------------
    with st.expander("Análise por estado civil"):
        col1, col2 = st.columns(2)

        # Gráfico de pizza - geral
        with col1:
            fig_pizza_ec = px.pie(
                df_filtrado, names="Estado Civil", hole=0.3,
                title="Distribuição geral por estado civil"
            )
            fig_pizza_ec.update_traces(
                textinfo="percent+label",
                texttemplate="%{label}<br>%{percent:.2%}",
                hovertemplate="%{label}<br>%{percent:.2%}<br>N = %{value}",
                insidetextorientation='radial'
            )
            fig_pizza_ec.update_layout(
                margin=dict(t=80, b=50, l=50, r=50)
            )
            st.plotly_chart(fig_pizza_ec, use_container_width=True)

        # Gráfico de barras - por ano
        with col2:
            df_percent_ec = (
                df_filtrado.groupby(["Ano", "Estado Civil"]).size().reset_index(name="Quantidade")
            )
            df_percent_ec["Percentual"] = df_percent_ec.groupby("Ano")["Quantidade"].transform(lambda x: 100 * x / x.sum())

            fig_bar_ec = go.Figure()
            for ec in df_percent_ec["Estado Civil"].unique():
                df_ec = df_percent_ec[df_percent_ec["Estado Civil"] == ec]
                fig_bar_ec.add_trace(go.Bar(
                    x=df_ec["Ano"],
                    y=df_ec["Percentual"],
                    name=ec,
                    text=[f"{v:.2f}%" for v in df_ec["Percentual"]],
                    textposition="outside"
                ))

            fig_bar_ec.update_layout(
                barmode='group',
                title="Percentual de inscritos por estado civil e ano",
                yaxis=dict(automargin=True, range=[0, df_percent_ec["Percentual"].max() * 1.15]),
                margin=dict(t=80, b=50, l=50, r=50)
            )
            st.plotly_chart(fig_bar_ec, use_container_width=True)

    # ------------------------
    # Análise por cor/raça
    # ------------------------
    with st.expander("Análise por cor/raça"):
        col1, col2 = st.columns(2)

        # Gráfico de pizza - geral
        with col1:
            fig_pizza_cr = px.pie(
                df_filtrado, names="Cor/Raça", hole=0.3,
                title="Distribuição geral por cor/raça"
            )
            fig_pizza_cr.update_traces(
                textinfo="percent+label",
                texttemplate="%{label}<br>%{percent:.2%}",
                hovertemplate="%{label}<br>%{percent:.2%}<br>N = %{value}",
                insidetextorientation='radial'
            )
            fig_pizza_cr.update_layout(margin=dict(t=80, b=50, l=50, r=50))
            st.plotly_chart(fig_pizza_cr, use_container_width=True)

        # Gráfico de barras - por ano
        with col2:
            df_percent_cr = (
                df_filtrado.groupby(["Ano", "Cor/Raça"]).size().reset_index(name="Quantidade")
            )
            df_percent_cr["Percentual"] = df_percent_cr.groupby("Ano")["Quantidade"].transform(lambda x: 100 * x / x.sum())

            fig_bar_cr = go.Figure()
            for cr in df_percent_cr["Cor/Raça"].unique():
                df_cr = df_percent_cr[df_percent_cr["Cor/Raça"] == cr]
                fig_bar_cr.add_trace(go.Bar(
                    x=df_cr["Ano"],
                    y=df_cr["Percentual"],
                    name=cr,
                    text=[f"{v:.2f}%" for v in df_cr["Percentual"]],
                    textposition="outside"
                ))

            fig_bar_cr.update_layout(
                barmode='group',
                title="Percentual de inscritos por cor/raça e ano",
                yaxis=dict(automargin=True, range=[0, df_percent_cr["Percentual"].max() * 1.15]),
                margin=dict(t=80, b=50, l=50, r=50)
            )
            st.plotly_chart(fig_bar_cr, use_container_width=True)

# ------------------------
# Aba 3 - Dados escolares
# ------------------------
with tabs[2]:
    st.subheader("Dados escolares")

    # ------------------------
    # Dependência Administrativa
    # ------------------------
    with st.expander("Análise por dependência administrativa", expanded=False):
        col1, col2 = st.columns(2)

        # Definir cores fixas
        dep_colors = {
            "Federal": "#636EFA",       # Azul
            "Estadual": "#ff0000",      # Vermelho
            "Municipal": "#00CC96",     # Verde
            "Privada": "#AB63FA",       # Roxo
            "Não informado": "#0000ff"  # Cinza
        }

        # Geral
        with col1:
            df_dep_total = df_filtrado.assign(
                **{"Dependência Administrativa": df_filtrado["Dependência Administrativa"].fillna("Não informado")}
            )
            fig_dep = px.pie(
                df_dep_total,
                names="Dependência Administrativa", hole=0.3,
                title="Distribuição geral por dependência administrativa",
                color="Dependência Administrativa",
                color_discrete_map=dep_colors
            )
            fig_dep.update_traces(
                textinfo="percent+label",
                hovertemplate="%{label}<br>%{percent}<br>N = %{value}"
            )
            st.plotly_chart(fig_dep, use_container_width=True)

        # Por ano
        with col2:
            df_dep = (
                df_filtrado.assign(
                    **{"Dependência Administrativa": df_filtrado["Dependência Administrativa"].fillna("Não informado")}
                )
                .groupby(["Ano", "Dependência Administrativa"]).size().reset_index(name="Quantidade")
            )
            df_dep["Percentual"] = df_dep.groupby("Ano")["Quantidade"].transform(lambda x: 100 * x / x.sum())

            fig_dep_ano = px.bar(
                df_dep, x="Ano", y="Percentual", color="Dependência Administrativa",
                barmode="group", text="Percentual",
                title="Dependência administrativa por ano",
                color_discrete_map=dep_colors
            )
            fig_dep_ano.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            st.plotly_chart(fig_dep_ano, use_container_width=True)

    # ------------------------
    # Localização da Escola
    # ------------------------
    with st.expander("Análise por localização da escola", expanded=False):
        df_loc = df_filtrado.copy()
        df_loc = df_loc.rename(columns={"TP_LOCALIZACAO_ESC": "Localização"})

        # Mapear os valores
        localizacao_map = {1: "Urbana", 2: "Rural"}
        df_loc["Localização"] = df_loc["Localização"].map(localizacao_map)
        df_loc["Localização"] = df_loc["Localização"].fillna("Não informado")

        col1, col2 = st.columns(2)

        with col1:
            fig_loc = px.pie(
                df_loc,
                names="Localização",
                hole=0.3,
                title="Distribuição geral por localização"
            )
            fig_loc.update_traces(
                textinfo="percent+label",
                hovertemplate="%{label}<br>%{percent}<br>N = %{value}"
            )
            st.plotly_chart(fig_loc, use_container_width=True)

        with col2:
            df_loc_ano = (
                df_loc.groupby(["Ano", "Localização"])
                .size()
                .reset_index(name="Quantidade")
            )
            df_loc_ano["Percentual"] = df_loc_ano.groupby("Ano")["Quantidade"].transform(
                lambda x: 100 * x / x.sum()
            )

            fig_loc_ano = px.bar(
                df_loc_ano,
                x="Ano",
                y="Percentual",
                color="Localização",
                barmode="group",
                text="Percentual",
                title="Localização da escola por ano"
            )
            fig_loc_ano.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside"
            )
            st.plotly_chart(fig_loc_ano, use_container_width=True)

    # ------------------------
    # Tipo de Ensino
    # ------------------------
    with st.expander("Análise por tipo de ensino", expanded=False):
        df_tipo = df_filtrado.copy()
        df_tipo = df_tipo.rename(columns={"TP_ESCOLA": "Tipo de Ensino"})

        # Mapear os valores conforme a imagem
        tipo_map = {
            1: "Ensino Regular",
            2: "Educação Especial - Modalidade Substitutiva",
            3: "Educação de Jovens e Adultos"
        }
        df_tipo["Tipo de Ensino"] = df_tipo["Tipo de Ensino"].map(tipo_map)
        df_tipo["Tipo de Ensino"] = df_tipo["Tipo de Ensino"].fillna("Não informado")

        col1, col2 = st.columns(2)

        with col1:
            fig_tipo = px.pie(
                df_tipo,
                names="Tipo de Ensino",
                hole=0.3,
                title="Distribuição geral por tipo de ensino",
                width=600,  # Aumentando largura
                height=500  # Aumentando altura
            )
            fig_tipo.update_traces(
                textinfo="percent+label",
                hovertemplate="%{label}<br>%{percent:.2%}<br>N = %{value}"  # Apenas 2 casas decimais
            )
            st.plotly_chart(fig_tipo, use_container_width=True)

        with col2:
            df_tipo_ano = (
                df_tipo.groupby(["Ano", "Tipo de Ensino"])
                .size()
                .reset_index(name="Quantidade")
            )
            df_tipo_ano["Percentual"] = df_tipo_ano.groupby("Ano")["Quantidade"].transform(
                lambda x: 100 * x / x.sum()
            )

            fig_tipo_ano = px.bar(
                df_tipo_ano,
                x="Ano",
                y="Percentual",
                color="Tipo de Ensino",
                barmode="group",
                text="Percentual",
                title="Tipo de ensino por ano",
                width=700,  # Aumentando largura
                height=500  # Aumentando altura
            )
            fig_tipo_ano.update_traces(
                texttemplate="%{text:.2f}%",  # Apenas duas casas decimais
                textposition="outside"
            )
            st.plotly_chart(fig_tipo_ano, use_container_width=True)


# ------------------------
# Aba 4 - Dados de RENDA
# ------------------------
    with tabs[3]:
        renda_map = {
            "Q006": {
                "A": "Até 1 salário mínimo",
                "B": "1 a 2 salários mínimos",
                "C": "2 a 3 salários mínimos",
                "D": "3 a 5 salários mínimos",
                "E": "5 a 10 salários mínimos",
                "F": "Acima de 10 salários mínimos",
                "Z": "Não informado"
            }
        }


        # Função para converter código em texto
        def mapear_renda(row):
            return renda_map["Q006"].get(row.get("Q006"), "Não informado")


        # Aplicar ao dataframe
        if "Q006" in df_filtrado.columns:
            df_filtrado["Faixa de Renda"] = df_filtrado.apply(mapear_renda, axis=1)

        # Mapeamento numérico aproximado para cálculo de renda
        salario_minimo = 1500  # ajuste conforme o valor atual
        faixa_valor = {
            "A": 1 * salario_minimo,
            "B": 1.5 * salario_minimo,
            "C": 2.5 * salario_minimo,
            "D": 4 * salario_minimo,
            "E": 7.5 * salario_minimo,
            "F": 12.5 * salario_minimo,
            "Z": np.nan
        }

        # Calcular renda total e per capita
        if "Q005" in df_filtrado.columns and "Q006" in df_filtrado.columns:
            df_filtrado["Renda Total (R$)"] = df_filtrado["Q006"].map(faixa_valor)
            df_filtrado["Renda Per Capita (R$)"] = df_filtrado["Renda Total (R$)"] / df_filtrado["Q005"]
            # Arredondar para duas casas decimais
            df_filtrado["Renda Total (R$)"] = df_filtrado["Renda Total (R$)"].round(2)
            df_filtrado["Renda Per Capita (R$)"] = df_filtrado["Renda Per Capita (R$)"].round(2)

        # Gráfico de pizza da faixa de renda
        fig_renda = px.pie(
            df_filtrado.dropna(subset=["Faixa de Renda"]),
            names="Faixa de Renda",
            hole=0.3,
            title="Distribuição por faixa de renda",
            hover_data=["Faixa de Renda", "Renda Total (R$)", "Renda Per Capita (R$)"]
        )
        fig_renda.update_traces(
            textinfo="percent+label",
            hovertemplate="%{label}<br>%{percent}<br>N = %{value}<br>Renda Total: %{customdata[1]:.2f} R$<br>Per Capita: %{customdata[2]:.2f} R$"
        )
        st.plotly_chart(fig_renda, use_container_width=True)

        # ------------------------
        # Gráfico de barras da Renda Per Capita média
        # ------------------------
        df_media = df_filtrado.dropna(subset=["Renda Per Capita (R$)"]).groupby("Faixa de Renda")[
            "Renda Per Capita (R$)"].mean().reset_index()
        df_media["Renda Per Capita (R$)"] = df_media["Renda Per Capita (R$)"].round(2)
        df_media = df_media.sort_values("Renda Per Capita (R$)", ascending=False)

        fig_bar = px.bar(
            df_media,
            x="Faixa de Renda",
            y="Renda Per Capita (R$)",
            text="Renda Per Capita (R$)",
            title="Renda Per Capita Média por Faixa de Renda",
            labels={"Renda Per Capita (R$)": "R$"},
            color="Renda Per Capita (R$)",
            color_continuous_scale="Blues"
        )
        fig_bar.update_traces(texttemplate="R$ %{text:.2f}", textposition="outside")
        fig_bar.update_layout(yaxis_title="Renda Per Capita (R$)", xaxis_title="Faixa de Renda")
        st.plotly_chart(fig_bar, use_container_width=True)

# ------------------------
# Aba 4 - Dados de moradia
# ------------------------
with tabs[4]:
    st.subheader("Dados de moradia")

    # Mapas de código para texto
    moradia_map = {
        "Q020": {  # Tipo de moradia
            "A": "Casa",
            "B": "Apartamento",
            "C": "Condomínio",
            "D": "Barraco",
            "E": "Outros"
        },
        "Q021": {  # Situação da moradia
            "A": "Própria",
            "B": "Alugada",
            "C": "Cedido",
            "D": "Financiada",
            "E": "Outros"
        }
    }

    # Função para combinar tipo e situação da moradia
    def combinar_moradia(row):
        tipo = moradia_map["Q020"].get(row.get("Q020"), "")
        situacao = moradia_map["Q021"].get(row.get("Q021"), "")

        if tipo and situacao:
            return f"{tipo} ({situacao})"
        elif tipo:
            return tipo
        elif situacao:
            return situacao
        else:
            return "Não informado"

    # Criar coluna Moradia no df_filtrado
    if "Q020" in df_filtrado.columns or "Q021" in df_filtrado.columns:
        df_filtrado["Moradia"] = df_filtrado.apply(combinar_moradia, axis=1)

        # Contar frequências
        moradia_counts = df_filtrado["Moradia"].value_counts()

        # Agrupar categorias pequenas (<2% do total) em "Outros"
        limite = 0.02 * moradia_counts.sum()
        moradia_counts_ajustado = moradia_counts.copy()
        moradia_counts_ajustado[moradia_counts < limite] = "Outros"

        df_moradia_ajustado = moradia_counts_ajustado.reset_index()
        df_moradia_ajustado.columns = ["Moradia", "Quantidade"]
        df_moradia_ajustado = df_moradia_ajustado.groupby("Moradia", as_index=False).sum()

        # Gráfico de pizza
        fig_moradia = px.pie(
            df_moradia_ajustado,
            names="Moradia",
            values="Quantidade",
            hole=0.3,
            title="Distribuição do tipo e situação da moradia",
        )
        fig_moradia.update_traces(textinfo="percent+label", hovertemplate="%{label}<br>%{percent}<br>N = %{value}")
        st.plotly_chart(fig_moradia, use_container_width=True)
    else:
        st.warning("⚠️ Colunas de moradia (Q020 e Q021) não encontradas nos dados.")

    # ------------------------
    # Aba 5 - Dados de MORADIA
    # ------------------------
    with tabs[4]:

        # Mapear os códigos para texto completo do ENEM
        banheiro_map = {
            "A": "Nenhum banheiro",
            "B": "1 banheiro",
            "C": "2 banheiros",
            "D": "3 ou mais banheiros",
            "Z": "Não informado"
        }

        quartos_map = {
            "A": "1 quarto",
            "B": "2 quartos",
            "C": "3 quartos",
            "D": "4 ou mais quartos",
            "Z": "Não informado"
        }


        # Q005 é numérico → converter para categorias
        def categorizar_moradores(x):
            if pd.isna(x):
                return "Não informado"
            elif x == 1:
                return "1 morador"
            elif x == 2:
                return "2 moradores"
            elif x == 3:
                return "3 moradores"
            elif x == 4:
                return "4 moradores"
            elif x >= 5:
                return "5 ou mais moradores"
            else:
                return "Não informado"


        # Função para processar cada ano
        def processar_dados(df, ano):
            dados = df.copy()
            if "Q008" in dados.columns:
                dados["Banheiros em Casa"] = dados["Q008"].map(banheiro_map)
            if "Q007" in dados.columns:
                dados["Quartos em Casa"] = dados["Q007"].map(quartos_map)
            if "Q005" in dados.columns:
                dados["Moradores em Casa"] = dados["Q005"].apply(categorizar_moradores)
            dados["Ano"] = ano
            return dados


        # Assumindo que você já tem df_2019 e df_2023
        df_2019_proc = processar_dados(df_2019, 2019)
        df_2023_proc = processar_dados(df_2023, 2023)

        # Juntar os dois anos
        df_moradia = pd.concat([df_2019_proc, df_2023_proc])


        # ------------------------
        # Função auxiliar para calcular % e plotar
        # ------------------------
        def plot_percentual(df, coluna, ordem, titulo):
            df_plot = (
                df.groupby(["Ano", coluna])
                .size().reset_index(name="Quantidade")
            )

            # Converter em %
            df_plot["Percentual"] = df_plot.groupby("Ano")["Quantidade"].transform(
                lambda x: (x / x.sum()) * 100
            )

            fig = px.bar(
                df_plot,
                x=coluna,
                y="Percentual",
                color="Ano",
                barmode="group",
                category_orders={coluna: ordem},
                title=titulo,
                labels={"Percentual": "% de Inscritos"}
            )
            fig.update_traces(texttemplate="%{y:.2f}%", textposition="inside")
            return fig


        # ------------------------
        # Gráfico de Banheiros
        # ------------------------
        ordem_banheiros = ["Nenhum banheiro", "1 banheiro", "2 banheiros", "3 ou mais banheiros", "Não informado"]
        fig_banheiros = plot_percentual(df_moradia, "Banheiros em Casa", ordem_banheiros,
                                        "Banheiros nas Casas")
        st.plotly_chart(fig_banheiros, use_container_width=True)

        # ------------------------
        # Gráfico de Quartos
        # ------------------------
        ordem_quartos = ["1 quarto", "2 quartos", "3 quartos", "4 ou mais quartos", "Não informado"]
        fig_quartos = plot_percentual(df_moradia, "Quartos em Casa", ordem_quartos, "Quartos nas Casas ")
        st.plotly_chart(fig_quartos, use_container_width=True)

        # ------------------------
        # Gráfico de Moradores
        # ------------------------
        ordem_moradores = ["1 morador", "2 moradores", "3 moradores", "4 moradores", "5 ou mais moradores",
                           "Não informado"]
        fig_moradores = plot_percentual(df_moradia, "Moradores em Casa", ordem_moradores,
                                        "Moradores por Casa ")
        st.plotly_chart(fig_moradores, use_container_width=True)

# ------------------------
# Aba 5 - Dados de transporte
# ------------------------
with tabs[5]:
    st.subheader("Dados de transporte")

    # Mapas de código para texto
    transporte_map = {
        "Q010": {"A": "Não", "B": "1 carro", "C": "2 carros", "D": "3 carros", "E": "4 ou mais"},
        "Q011": {"A": "Não", "B": "1 moto", "C": "2 motos", "D": "3 ou mais"},
        "Q012": {"A": "Não", "B": "1 veículo", "C": "2 ou mais"}
    }

    def mapear_transporte(coluna, mapa):
        if coluna in df_filtrado.columns:
            return df_filtrado[coluna].map(mapa.get(coluna, {})).fillna("Não informado")
        else:
            return pd.Series(["Não informado"]*len(df_filtrado))

    df_filtrado["Carro"] = mapear_transporte("Q010", transporte_map)
    df_filtrado["Moto"] = mapear_transporte("Q011", transporte_map)
    df_filtrado["Automóvel"] = mapear_transporte("Q012", transporte_map)

    # Contagem de frequências
    carro_counts = df_filtrado["Carro"].value_counts().sort_index().reset_index()
    carro_counts.columns = ["Categoria", "Quantidade"]

    moto_counts = df_filtrado["Moto"].value_counts().sort_index().reset_index()
    moto_counts.columns = ["Categoria", "Quantidade"]

    automovel_counts = df_filtrado["Automóvel"].value_counts().sort_index().reset_index()
    automovel_counts.columns = ["Categoria", "Quantidade"]

    # Gráfico lado a lado
    fig_transporte = go.Figure()

    # Pizza - Carro
    fig_transporte.add_trace(go.Pie(
        labels=carro_counts["Categoria"],
        values=carro_counts["Quantidade"],
        hole=0.3,
        name="Carro",
        title="Carros",
        domain={'x': [0.0, 0.34]},  # aumenta espaço
        textinfo='percent+label',
        texttemplate='%{label}<br>%{percent:.2%}',  # 2 casas decimais
        hovertemplate="%{label}<br>%{percent:.2%}<br>N = %{value}",
        insidetextorientation='radial'  # evita cortes
    ))

    # Pizza - Moto
    fig_transporte.add_trace(go.Pie(
        labels=moto_counts["Categoria"],
        values=moto_counts["Quantidade"],
        hole=0.3,
        name="Moto",
        title="Motos",
        domain={'x': [0.35, 0.66]},
        textinfo='percent+label',
        texttemplate='%{label}<br>%{percent:.2%}',
        hovertemplate="%{label}<br>%{percent:.2%}<br>N = %{value}",
        insidetextorientation='radial'
    ))

    # Pizza - Automóvel
    fig_transporte.add_trace(go.Pie(
        labels=automovel_counts["Categoria"],
        values=automovel_counts["Quantidade"],
        hole=0.3,
        name="Automóvel",
        title="Automóveis",
        domain={'x': [0.67, 1.0]},
        textinfo='percent+label',
        texttemplate='%{label}<br>%{percent:.2%}',
        hovertemplate="%{label}<br>%{percent:.2%}<br>N = %{value}",
        insidetextorientation='radial'
    ))

    # Layout final
    fig_transporte.update_layout(
        legend=dict(orientation="v", y=0.5, x=1.05),
        margin=dict(t=50, b=0, l=50, r=150),  # margens ajustadas
        showlegend=True
    )

    st.plotly_chart(fig_transporte, use_container_width=True)

# ------------------------
# Aba 6 - Aparelhos e tecnologias digitais (apenas barras)
# ------------------------
with tabs[6]:
    st.subheader("Aparelhos e tecnologias digitais")

    # Mapas de código para texto das questões ENEM
    tecnologia_map = {
        "Q024": {"A": "Sim", "B": "Não"},   # Possui computador
        "Q025": {"A": "Sim", "B": "Não"},   # Acesso à internet
        "Q022": {"A": "Sim", "B": "Não"}    # Possui smartphone
    }

    def mapear_tecnologia(coluna, mapa):
        if coluna in df_filtrado.columns:
            return df_filtrado[coluna].map(mapa.get(coluna, {})).fillna("Não informado")
        else:
            return pd.Series(["Não informado"]*len(df_filtrado))

    # Criar colunas mapeadas
    df_filtrado["Computador"] = mapear_tecnologia("Q024", tecnologia_map)
    df_filtrado["Internet"] = mapear_tecnologia("Q025", tecnologia_map)
    df_filtrado["Smartphone"] = mapear_tecnologia("Q022", tecnologia_map)

    # Preparar dados para gráfico de barras
    colunas_graficos = ["Computador", "Internet", "Smartphone"]
    df_barras = pd.DataFrame()

    for coluna in colunas_graficos:
        contagem = df_filtrado[coluna].value_counts(normalize=True).reset_index()
        contagem.columns = ["Categoria", "Percentual"]
        contagem["Percentual"] = contagem["Percentual"] * 100
        contagem["Dispositivo"] = coluna
        df_barras = pd.concat([df_barras, contagem], ignore_index=True)

    # Definir cores fixas para categorias
    cores = {"Sim": "#1f77b4", "Não": "#ff7f0e", "Não informado": "#d62728"}

    # Gráfico de barras horizontais
    fig_bar = px.bar(
        df_barras,
        x="Percentual",
        y="Dispositivo",
        color="Categoria",
        color_discrete_map=cores,
        orientation="h",
        barmode="stack",
        title="Distribuição de aparelhos e tecnologias digitais entre alunos"
    )

    # Ajustar rótulos para duas casas decimais corretas
    fig_bar.update_traces(
        textposition="outside",
        texttemplate="%{x:.2f}%"  # usa %{x} para referir-se ao valor do eixo X
    )

    # Layout
    fig_bar.update_layout(
        yaxis=dict(autorange="reversed"),
        margin=dict(t=100, b=50, l=100, r=50)
    )

    st.plotly_chart(fig_bar, use_container_width=True)
