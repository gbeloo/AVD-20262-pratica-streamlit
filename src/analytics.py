"""Funções auxiliares: EDA de Pokémon e operações usadas pelos dashboards.

[IA] ChatGPT — apoio na estrutura e sintaxe de funções, a revisar pelo autor.
"""
import pandas as pd
import numpy as np

BASE_STATS = ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]
VARS_QUANT = ["total", *BASE_STATS]
COLS_REQUIRED = ["number", "name", "type1", "type2", "total", *BASE_STATS, "generation", "legendary"]

def tratar_pokemon(df: pd.DataFrame) -> pd.DataFrame:
    """Repete as decisões documentadas no notebook original (sem excluir formas)."""
    missing = set(COLS_REQUIRED).difference(df.columns)
    if missing:
        raise ValueError(f"Colunas ausentes do CSV: {', '.join(sorted(missing))}")
    result = df.copy()
    result["type2"] = result["type2"].replace("", np.nan)
    result["type1"] = result["type1"].replace({"Graass": "Grass"})
    mascara = result["type1"].eq("Blastoise")
    result.loc[mascara, "type1"] = "Water"
    result.loc[mascara, "type2"] = np.nan
    result["name"] = result["name"].replace({"Gigantamax Blasoise": "Gigantamax Blastoise"})
    result["type2"] = result["type2"].fillna("Sem segundo tipo")
    result["legendary"] = result["legendary"].astype(str).str.strip().str.lower().map(
        {"true": True, "false": False, "1": True, "0": False}
    )
    if result["legendary"].isna().any():
        raise ValueError("Valores inesperados na coluna legendary.")
    result["legendary_label"] = result["legendary"].map({True: "Lendário", False: "Não lendário"})
    for col in VARS_QUANT + ["generation"]:
        result[col] = pd.to_numeric(result[col], errors="coerce")
    if result[VARS_QUANT].isna().any().any():
        raise ValueError("Encontrados valores numéricos ausentes/inválidos nas colunas de status.")
    return result

def aplicar_filtros(df, variavel_intervalo, intervalo, geracoes, tipos, classe):
    filtro = df.copy()
    if geracoes:
        filtro = filtro[filtro["generation"].isin(geracoes)]
    if tipos:
        filtro = filtro[filtro["type1"].isin(tipos)]
    if classe != "Todos":
        filtro = filtro[filtro["legendary_label"].eq(classe)]
    if variavel_intervalo in VARS_QUANT and intervalo is not None:
        filtro = filtro[filtro[variavel_intervalo].between(*intervalo)]
    return filtro

def correlacao_spearman(df, variaveis):
    if len(variaveis) < 2 or len(df) < 2:
        return pd.DataFrame()
    return df[variaveis].corr(method="spearman")

def calcular_kpi(df, variavel, operacao):
    """Cálculos genéricos; seleção e justificativa das métricas são do aluno."""
    if df.empty or variavel not in VARS_QUANT:
        return None
    serie = df[variavel]
    funcoes = {
        "Média": serie.mean,
        "Mediana": serie.median,
        "Máximo": serie.max,
        "Mínimo": serie.min,
        "Desvio padrão": serie.std,
        "Contagem": serie.count,
    }
    if operacao not in funcoes:
        return None
    val = funcoes[operacao]()
    return None if pd.isna(val) else float(val)
