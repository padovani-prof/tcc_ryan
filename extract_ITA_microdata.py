import pandas as pd

# df2019 = pd.read_csv("MICRODADOS_ENEM_2019.csv", encoding="cp1252", delimiter=";")
def MA0():
    df = pd.read_csv("../MICRODADOS_ENEM_2019.csv", encoding="cp1252", delimiter=";")
    print("QTD: 2019[GERAL]:", len(df))
    itac2019 = df[df["CO_MUNICIPIO_ESC"]==1301902]
    itac2019.to_excel("MICRODADOS_ITA_2019.xlsx")

    df = pd.read_csv("../MICRODADOS_ENEM_2023.csv", encoding="cp1252", delimiter=";")
    print("QTD: 2023[GERAL]:", len(df))
    itac2023 = df[df["CO_MUNICIPIO_ESC"]==1301902]
    itac2023.to_excel("MICRODADOS_ITA_2023.xlsx")

def MA1():
    participantes_2019 = pd.read_excel("MICRODADOS_ITA_2019.xlsx")
    participantes_2023 = pd.read_excel("MICRODADOS_ITA_2023.xlsx")
    print("Qtd. 2019 (ITA):", len(participantes_2019))
    print("Qtd. 2023 (ITA):", len(participantes_2023))
    return participantes_2019, participantes_2023

def MA2():
    itac2019, itac2023 = MA1()
    presenca_prova_CN = itac2019[["NU_INSCRICAO", "TP_PRESENCA_CN"]].groupby("TP_PRESENCA_CN").count()
    presenca_prova_CH = itac2019[["NU_INSCRICAO", "TP_PRESENCA_CH"]].groupby("TP_PRESENCA_CH").count()
    presenca_prova_LC = itac2019[["NU_INSCRICAO", "TP_PRESENCA_LC"]].groupby("TP_PRESENCA_LC").count()
    presenca_prova_MT = itac2019[["NU_INSCRICAO", "TP_PRESENCA_MT"]].groupby("TP_PRESENCA_MT").count()
    presenca_redacao = len(itac2019) - len(itac2019[itac2019['TP_STATUS_REDACAO'].isna()])
    print("=-=-=-=-=-=-= PRESENÇA CN, CH, LC, MT e REDAÇÃO 2019 =-=-=-=-=-=-=")
    print(presenca_prova_CN)
    print(presenca_prova_CH)
    print(presenca_prova_LC)
    print(presenca_prova_MT)
    print(presenca_redacao)
    presenca_prova_CN = itac2023[["NU_INSCRICAO", "TP_PRESENCA_CN"]].groupby("TP_PRESENCA_CN").count()
    presenca_prova_CH = itac2023[["NU_INSCRICAO", "TP_PRESENCA_CH"]].groupby("TP_PRESENCA_CH").count()
    presenca_prova_LC = itac2023[["NU_INSCRICAO", "TP_PRESENCA_LC"]].groupby("TP_PRESENCA_LC").count()
    presenca_prova_MT = itac2023[["NU_INSCRICAO", "TP_PRESENCA_MT"]].groupby("TP_PRESENCA_MT").count()
    presenca_redacao = len(itac2023) - len(itac2023[itac2023['TP_STATUS_REDACAO'].isna()])

    print("=-=-=-=-=-=-= PRESENÇA CN, CH, LC, MT e REDAÇÃO 2023 =-=-=-=-=-=-=")
    print(presenca_prova_CN)
    print(presenca_prova_CH)
    print(presenca_prova_LC)
    print(presenca_prova_MT)
    print(presenca_redacao)

def MA3():
    itac2019, itac2023 = MA1()  # carrega os arquivos já filtrados para Itacoatiara

    alvo_2019 = itac2019[["NU_INSCRICAO", "TP_FAIXA_ETARIA"]]
    faixa_2019 = alvo_2019.groupby("TP_FAIXA_ETARIA").count()

    alvo_2023 = itac2023[["NU_INSCRICAO", "TP_FAIXA_ETARIA"]]
    faixa_2023 = alvo_2023.groupby("TP_FAIXA_ETARIA").count()

    print("=-=-=-=-=-= FAIXA ETÁRIA =-=-=-=-=-=")
    print("2019:")
    print(faixa_2019)
    print("\n2023:")
    print(faixa_2023)

def MA4():
    itac2019, itac2023 = MA1()
    tp_sexo_2019 = itac2019[["NU_INSCRICAO", "TP_SEXO"]].groupby("TP_SEXO").count()
    tp_sexo_2023 = itac2023[["NU_INSCRICAO", "TP_SEXO"]].groupby("TP_SEXO").count()
    print("=-=-=-=-=-=-= SEXO DOS PARTICIPANTES 2019 X 2023 =-=-=-=-=-=-=")
    print(tp_sexo_2019)
    print(tp_sexo_2023)


def MA5():
    itac2019, itac2023 = MA1()
    estado_civil_2019 = itac2019[["NU_INSCRICAO", "TP_ESTADO_CIVIL"]].groupby("TP_ESTADO_CIVIL").count()
    estado_civil_2023 = itac2023[["NU_INSCRICAO", "TP_ESTADO_CIVIL"]].groupby("TP_ESTADO_CIVIL").count()
    print("=-=-=-=-=-= ESTADO CIVIL 2019 X 2023 =-=-=-=-=-=")
    print(estado_civil_2019)
    print(estado_civil_2023)

def MA6():
    itac2019, itac2023 = MA1()
    tp_cor_raca_2019 = itac2019[["NU_INSCRICAO", "TP_COR_RACA"]].groupby("TP_COR_RACA").count()
    tp_cor_raca_2023 = itac2023[["NU_INSCRICAO", "TP_COR_RACA"]].groupby("TP_COR_RACA").count()
    print("=-=-=-=-=-= TP_COR/RAÇA 2019 X TP_COR/RAÇA 2023 ")
    print(tp_cor_raca_2019)
    print(tp_cor_raca_2023)

def contar_por_coluna(df, coluna):
    return df[coluna].value_counts().sort_index()

def contar_renda(df):
    return contar_por_coluna(df, "Q006")

def MA7():
    import numpy as np
    df2019 = pd.read_excel('MICRODADOS_ITA_2019.xlsx')

    df2023 = pd.read_excel('MICRODADOS_ITA_2023.xlsx')

    faixas_renda = {
        'A': (0.00, 0.00),
        'B': (0.01, 998.00),
        'C': (998.01, 1497.00),
        'D': (1497.01, 1996.00),
        'E': (1996.01, 2495.00),
        'F': (2495.01, 2994.00),
        'G': (2994.01, 3992.00),
        'H': (3992.01, 4990.00),
        'I': (4990.01, 5988.00),
        'J': (5988.01, 6986.00),
        'K': (6986.01, 7984.00),
        'L': (7984.01, 8982.00),
        'M': (8982.01, 9980.00),
        'N': (9980.01, 11976.00),
        'O': (11976.01, 14970.00),
        'P': (14970.01, 19960.00),
        'Q': (19960.00, np.inf)  # Faixa aberta superiormente
    }
    # Exemplo de DataFrame
    df = df2023

    # Converter Q005 para inteiro
    df['Q005'] = pd.to_numeric(df['Q005'], errors='coerce')

    # Funções para calcular renda per capita mínima e máxima
    def renda_per_capita_min(row):
        faixa = faixas_renda.get(row['Q006'], (np.nan, np.nan))
        return faixa[0] / row['Q005'] if row['Q005'] else np.nan

    def renda_per_capita_max(row):
        faixa = faixas_renda.get(row['Q006'], (np.nan, np.nan))
        return faixa[1] / row['Q005'] if row['Q005'] else np.nan

    # Aplicar as funções ao DataFrame
    df['renda_per_capita_min'] = df.apply(renda_per_capita_min, axis=1)
    df['renda_per_capita_max'] = df.apply(renda_per_capita_max, axis=1)

    df['renda_per_capita_media'] = df[['renda_per_capita_min', 'renda_per_capita_max']].mean(axis=1)

    # Função para enquadrar a média em uma faixa
    def enquadrar_faixa(media):
        for letra, (min_val, max_val) in faixas_renda.items():
            if min_val <= media <= max_val:
                return letra
        return np.nan

    # Aplicar a função
    df['faixa_per_capita'] = df['renda_per_capita_media'].apply(enquadrar_faixa)
    df['faixa_per_capita'] = df['faixa_per_capita'].fillna('Q')

    print(df)

    df = df[['NU_INSCRICAO', 'faixa_per_capita']].groupby('faixa_per_capita').count()
    print(df)

def MA8():
    itac2019, itac2023 = MA1()
    dados_ita_2019 = itac2019[["NU_INSCRICAO", "TP_DEPENDENCIA_ADM_ESC"]].groupby("TP_DEPENDENCIA_ADM_ESC").count()
    dados_ita_2023 = itac2023[["NU_INSCRICAO", "TP_DEPENDENCIA_ADM_ESC"]].groupby("TP_DEPENDENCIA_ADM_ESC").count()
    print("=-=-=-=-=-=-= DEPENDÊNCIA DA ESCOLA =-=-=-=-=-=")
    print(dados_ita_2019, dados_ita_2023)

def MA9():
    itac2019, itac2023 = MA1()
    dados_ita_2019 = itac2019[["NU_INSCRICAO", "TP_ENSINO"]].groupby("TP_ENSINO").count()
    dados_ita_2023 = itac2023[["NU_INSCRICAO", "TP_ENSINO"]].groupby("TP_ENSINO").count()
    print("=-=-=-=-=-=-= TIPO DE ENSINO =-=-=-=-=-=")
    print(dados_ita_2019, dados_ita_2023)

def MA10():
    itac2019, itac2023 = MA1()
    tipo_escola_2019 = itac2019[["NU_INSCRICAO", "TP_ESCOLA"]].groupby("TP_ESCOLA").count()
    tipo_escola_2023 = itac2023[["NU_INSCRICAO", "TP_ESCOLA"]].groupby("TP_ESCOLA").count()
    print("=-=-=-=-=-=-= TIPO DE ESCOLA =-=-=-=-=-=")
    print(tipo_escola_2019, tipo_escola_2023)

def MA11():
    itac2019, itac2023 = MA1()
    empregado_domestico2019 = itac2019[["NU_INSCRICAO", "Q007"]].groupby("Q007").count()
    empregado_domestico2023 = itac2023[["NU_INSCRICAO", "Q007"]].groupby("Q007").count()
    print("=-=-=-=-=-=-= EMPREGADO DOMÉSTICO =-=-=-=-=-=")
    print(empregado_domestico2019)
    print(empregado_domestico2023)

def MA12():
    itac2019, itac2023 = MA1()
    banheiro2019 = itac2019[["NU_INSCRICAO", "Q008"]].groupby("Q008").count()
    banheiro2023 = itac2023[["NU_INSCRICAO", "Q008"]].groupby("Q008").count()
    print("=-=-=-=-=-=-= BANHEIRO EM CASA =-=-=-=-=-=-=")
    print(banheiro2019)
    print(banheiro2023)

def MA13():
    itac2019, itac2023 = MA1()
    quartos2019 = itac2019[["NU_INSCRICAO", "Q009"]].groupby("Q009").count()
    quartos2023 = itac2023[["NU_INSCRICAO", "Q009"]].groupby("Q009").count()
    print("=-=-=-=-=-=-= QUARTOS EM CASA =-=-=-=-=-=-=")
    print(quartos2019)
    print(quartos2023)

def MA14():
    itac2019, itac2023 = MA1()
    carros2019 = itac2019[["NU_INSCRICAO", "Q010"]].groupby("Q010").count()
    carros2023 = itac2023[["NU_INSCRICAO", "Q010"]].groupby("Q010").count()
    print("=-=-=-=-=-=-= CARROS EM CASA =-=-=-=-=-=-=")
    print("2019", carros2019)
    print("2023", carros2023)

    motos2019 = itac2019[["NU_INSCRICAO", "Q011"]].groupby("Q011").count()
    motos2023 = itac2023[["NU_INSCRICAO", "Q011"]].groupby("Q011").count()
    print("=-=-=-=-=-=-= MOTOS EM CASA =-=-=-=-=-=-=")
    print("2019", motos2019)
    print("2023",motos2023)

def MA15():
    itac2019, itac2023 = MA1()
    maq_lavar_2019 = itac2019[["NU_INSCRICAO", "Q014"]].groupby("Q014").count()
    maq_lavar_2023 = itac2023[["NU_INSCRICAO", "Q014"]].groupby("Q014").count()
    print("=-=-=-=-=-=-= BANHEIRO EM CASA =-=-=-=-=-=-=")
    print("2019", maq_lavar_2019)
    print("2023", maq_lavar_2023)

def MA16():
    itac2019, itac2023 = MA1()
    micro_2019 = itac2019[["NU_INSCRICAO", "Q016"]].groupby("Q016").count()
    micro_2023 = itac2023[["NU_INSCRICAO", "Q016"]].groupby("Q016").count()
    print("=-=-=-=-=-=-= MIICRO-ONDAS EM CASA =-=-=-=-=-=-=")
    print("2019", micro_2019)
    print("2023", micro_2023)

def MA17():
    itac2019, itac2023 = MA1()
    tv_2019 = itac2019[["NU_INSCRICAO", "Q019"]].groupby("Q019").count()
    tv_2023 = itac2023[["NU_INSCRICAO", "Q019"]].groupby("Q019").count()
    print("=-=-=-=-=-=-= TELEVISÃO EM CASA =-=-=-=-=-=-=")
    print("2019", tv_2019)
    print("2023", tv_2023)

def MA18():
    itac2019, itac2023 = MA1()
    cllr_2019 = itac2019[["NU_INSCRICAO", "Q022"]].groupby("Q022").count()
    cllr_2023 = itac2023[["NU_INSCRICAO", "Q022"]].groupby("Q022").count()
    print("=-=-=-=-=-=-= CELULAR EM CASA =-=-=-=-=-=-=")
    print("2019", cllr_2019)
    print("2023", cllr_2023)

def MA19():
    itac2019, itac2023 = MA1()
    computador_2019 = itac2019[["NU_INSCRICAO", "Q024"]].groupby("Q024").count()
    computador_2023 = itac2023[["NU_INSCRICAO", "Q024"]].groupby("Q024").count()
    print("=-=-=-=-=-=-= COMPUTADOR EM CASA =-=-=-=-=-=-=")
    print("2019", computador_2019)
    print("2023", computador_2023)

def MA20():
    itac2019, itac2023 = MA1()
    internet_2019 = itac2019[["NU_INSCRICAO", "Q025"]].groupby("Q025").count()
    internet_2023 = itac2023[["NU_INSCRICAO", "Q025"]].groupby("Q025").count()
    print("=-=-=-=-=-=-= INTERNET EM CASA =-=-=-=-=-=-=")
    print("2019", internet_2019)
    print("2023", internet_2023)

def inscritos_nacional():
    carregar_dados_2019, carregar_dados_2023 = MA0()
    itac2019 = carregar_dados_2019("MICRODADOS_ENEM_2019.csv")
    itac2023 = carregar_dados_2023("MICRODADOS_ENEM_2023.csv")
    q2019 = len(itac2019)
    q2023 = len(itac2023)

    print(2019, "=", q2019)
    print(2023, "=", q2023)

    df2019 = pd.read_excel('MICRODADOS_ITA_2019.xlsx')
    df2023 = pd.read_excel('MICRODADOS_ITA_2023.xlsx')
    print(df2019['Q009'].max())
    print(df2023['Q009'].max())


MA7()