"""Exporta o CSV tratado seguindo a EDA — executar antes da publicação."""
from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.analytics import tratar_pokemon

URL = "https://raw.githubusercontent.com/STATS-UOA/databunker/master/data/pokemon.csv"
RAW = ROOT / "data" / "raw" / "Pokemon.csv"
OUT = ROOT / "data" / "clean" / "dataset.csv"

def main():
    fonte = RAW if RAW.exists() else URL
    df = tratar_pokemon(pd.read_csv(fonte))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"Preparado: {len(df)} registros em {OUT}")
    print("Dados públicos; formas alternativas mantidas; sem credenciais pessoais.")

if __name__ == "__main__":
    main()
