import pandas as pd

# Código de Itacoatiara
ITA_CODE = 1301902

df = pd.read_csv("MICRODADOS_ENEM_2023.csv", encoding="cp1252", delimiter=";")
print("QTD: 2023[GERAL]:", len(df))

# Extrair somente os registros de Itacoatiara (escolas)
itac2023 = df[df["CO_MUNICIPIO_ESC"] == ITA_CODE]
itac2023.to_excel("MICRODADOS_ITA_2023.xlsx")

def gerar_csv(ano=2023, arquivo_excel="MICRODADOS_ITA_2023.xlsx"):
    # Carregar o arquivo do ano especificado
    df = pd.read_excel(arquivo_excel)

    # Substituir valores vazios por NaN
    df = df.replace("", pd.NA)

    # Filtro: escola em Itacoatiara OU escola vazia mas prova em Itacoatiara
    df_filtrado = df[
        (df["CO_MUNICIPIO_ESC"] == ITA_CODE) |
        ((df["CO_MUNICIPIO_ESC"].isna()) & (df["CO_MUNICIPIO_PROVA"] == ITA_CODE))
    ]

    # Salvar CSV filtrado
    nome_arquivo = f"MICRODADOS_ITA_{ano}_FILTRADO.csv"
    df_filtrado.to_csv(nome_arquivo, index=False, encoding="utf-8-sig")

    print(f"{ano}: CSV criado com {len(df_filtrado)} linhas → {nome_arquivo}")


# Chamadas diretas
gerar_csv(2023, "MICRODADOS_ITA_2023.xlsx")
