import pandas as pd

def load_clingen_validity(path="Clingen-Gene-Disease-Summary-2025-07-01.csv"):
    try:
        df_raw = pd.read_csv(path, header=None)
        df = df_raw.iloc[5:]  # Data starts from 6th row
        df.columns = df_raw.iloc[4]  # Get actual headers from 5th row
        df = df[["GENE SYMBOL", "DISEASE LABEL", "CLASSIFICATION"]].dropna()
        return df
    except Exception as e:
        print("ClinGen file could not be read:", e)
        return pd.DataFrame()

def get_clingen_classification(gene_symbol, df_clingen):
    gene_row = df_clingen[df_clingen["GENE SYMBOL"] == gene_symbol]
    if not gene_row.empty:
        return gene_row.iloc[0]["CLASSIFICATION"]
    return "None"