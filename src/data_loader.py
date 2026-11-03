"""Carregamento do dataset tratado.

[IA] ChatGPT — apoio com cache, paths relativos e fallback do CSV público.
"""
from pathlib import Path
import pandas as pd
import streamlit as st
from src.analytics import tratar_pokemon

ROOT = Path(__file__).resolve().parents[1]
CLEAN_CSV = ROOT / "data" / "clean" / "dataset.csv"
# Espelho público de dados com a estrutura do dataset utilizado no EDA.
SOURCE_URL = "https://raw.githubusercontent.com/STATS-UOA/databunker/master/data/pokemon.csv"

@st.cache_data(ttl=86400, show_spinner="Carregando os Pokémon...")
def load_data():
    if CLEAN_CSV.is_file():
        return tratar_pokemon(pd.read_csv(CLEAN_CSV))
    # Fallback para que o app publicado não quebre antes de gerar o CSV local.
    try:
        return tratar_pokemon(pd.read_csv(SOURCE_URL))
    except Exception as exc:
        raise RuntimeError(
            "Não foi possível ler data/clean/dataset.csv nem baixar o arquivo público. "
            "Execute scripts/prepare_data.py ou adicione o CSV tratado ao repositório."
        ) from exc
