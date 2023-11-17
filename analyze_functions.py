import streamlit as st


def clean_powerbi(powerbi_table):
    df_placa_preju = powerbi_table.rename(
        columns={"Placa": "placa", "Valor Reclamado (BRL)": "prejuizo"}
    )[["placa", "prejuizo"]]

    return df_placa_preju


def clean_embarques(embarque_table):
    # fmt: off
    df_embarque = (embarque_table
                   .rename(columns={
                       "Placa Simples Veículo": "placa",
                       "Data Transporte": "data",
                       "Nome Transportadora": "transportadora",
                       "Valor total incl.imp.": "valor",
                       })
                    )[["placa", "data", "transportadora", "valor"]]

    df_placa_trans = (df_embarque
                      .groupby("placa", as_index=False)["transportadora"]
                      .unique()
                      )

    df_trans_valor = (df_embarque
                      .groupby("transportadora", as_index=False)["valor"]
                      .sum()
                      .rename(columns={"valor": "valor_total_transportadora"})
                      )
    # fmt: on

    return df_placa_trans, df_trans_valor


def compare(df_placa_preju, df_placa_trans, df_trans_valor):
    df_placa_preju_trans = df_placa_preju.merge(df_placa_trans)

    df_placa_preju_trans.transportadora = [
        name[0] for name in df_placa_preju_trans.transportadora
    ]

    df_final = df_placa_preju_trans.merge(df_trans_valor)[
        ["transportadora", "valor_total_transportadora", "prejuizo"]
    ].rename(
        columns={
            "transportadora": "Transportadora",
            "valor_total_transportadora": "Total Transportado (R$)",
            "prejuizo": "Sinistros (R$)",
        }
    )
    df_final["Porcentagem"] = round(
        (df_final["Sinistros (R$)"] / df_final["Total Transportado (R$)"]) * 100, 2
    )

    return df_final.sort_values("Porcentagem", ascending=False)


def analyze(powerbi_table, embarque_table):
    df_placa_preju = clean_powerbi(powerbi_table)
    df_placa_trans, df_trans_valor = clean_embarques(embarque_table)
    df_results = compare(df_placa_preju, df_placa_trans, df_trans_valor)

    return df_results
