"""Testes do processamento, sem necessidade do servidor Streamlit."""
import pandas as pd
from src.analytics import BASE_STATS, VARS_QUANT, tratar_pokemon, aplicar_filtros, correlacao_spearman, calcular_kpi

def exemplo():
    return pd.DataFrame([
        [9,"Gigantamax Blasoise","Blastoise","Water",530,79,83,100,85,105,78,1,False],
        [1,"Bulbasaur","Grass","Poison",318,45,49,49,65,65,45,1,False],
        [25,"Pikachu","Electric",None,320,35,55,40,50,50,90,1,False],
        [150,"Mewtwo","Psychic",None,680,106,110,90,154,90,130,1,True],
        [3,"Mega Venusaur","Grass","Poison",625,80,100,123,122,120,80,1,False],
    ],columns=["number","name","type1","type2","total",*BASE_STATS,"generation","legendary"])

def test_preserva_formas_alternativas():
    assert len(tratar_pokemon(exemplo())) == 5

def test_corrige_tipo_e_nome_e_ausencia():
    df = tratar_pokemon(exemplo())
    assert df.iloc[0]["name"] == "Gigantamax Blastoise"
    assert df.iloc[0]["type1"] == "Water"
    assert df.iloc[0]["type2"] == "Sem segundo tipo"
    assert df.iloc[2]["type2"] == "Sem segundo tipo"

def test_filtra_por_intervalo_e_classe():
    df=tratar_pokemon(exemplo())
    filtro=aplicar_filtros(df,"total",(500,700),[1],["Psychic"],"Lendário")
    assert filtro["name"].tolist() == ["Mewtwo"]

def test_calculos_parametrizados():
    df=tratar_pokemon(exemplo())
    assert calcular_kpi(df,"hp","Contagem") == 5.0
    assert calcular_kpi(df,"hp","Média") == float(df["hp"].mean())
    assert calcular_kpi(df,"hp","Nao existe") is None

def test_matriz_spearman():
    df=tratar_pokemon(exemplo())
    corr=correlacao_spearman(df,BASE_STATS)
    assert corr.shape==(6,6)
    assert corr.index.tolist()==BASE_STATS
    assert correlacao_spearman(df,["total"]).empty

def test_sem_dados_apos_filtro():
    df=tratar_pokemon(exemplo())
    vazio=aplicar_filtros(df,"total",(999,1000),[1],list(df["type1"]),"Todos")
    assert vazio.empty
    assert calcular_kpi(vazio,"hp","Média") is None
