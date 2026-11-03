# Pokémon | Laboratório EDA — AVD 2026.2

**Aluno:** Gabriel Nascimento Belo Osório

Aplicação Streamlit com dois dashboards, baseada na EDA entregue na disciplina de Análise e Visualização de Dados. Dataset público [Pokémon Stats (Kaggle)](https://www.kaggle.com/datasets/ulrikthygepedersen/pokemon-stats).

## O que já está programado

- Dashboard 1: seletor de variáveis, slider, filtros por geração/tipo/classe, heatmap de Spearman e histogramas quantitativos.
- Dashboard 2: público-alvo definido como **jogadores iniciantes**; três KPIs escolhidos (**quantidade de registros, ataque médio e defesa média**) e três gráficos Altair configurados por padrão. Os valores respondem aos filtros.
- Tratamento do dataset coerente com o notebook, inclusive formas alternativas, correção `Blastoise`/`Graass` e ausência de `type2`.
- Testes de lógica local e testes de interface via GitHub Actions, documentação de IA e layouts rascunhados.

## Rodar

Python 3.11+ (recomendado 3.12):

```bash
python -m pip install -r requirements.txt
python scripts/prepare_data.py
python -m pip install "pytest>=8,<10"
python -m pytest -q
streamlit run app.py
```

O CSV público apresenta 1.072 linhas; duas delas (`Farfetch'd` e `Galarian Corsola`) possuem discrepâncias entre `total` e a soma dos seis status. Foram preservadas, conforme a regra do EDA de não alterar automaticamente valores extremos/inconsistências sem análise. O aplicativo não usa `total` para inferir causalidade.

O app usa `data/clean/dataset.csv` quando presente. Se faltar, utiliza como fallback o [CSV público equivalente](https://github.com/STATS-UOA/databunker/blob/master/data/pokemon.csv); entretanto a entrega deve versionar o arquivo limpo. O workflow **Preparar dataset público** em GitHub Actions tenta gerar e commitar automaticamente o CSV limpo, com permissão de escrita, na primeira publicação. Se não ocorrer, execute-o manualmente na aba Actions ou carregue `data/clean/dataset.csv`.

## Como publicar sem notebook (pelo celular)

1. Faça um *fork* do [repositório-modelo da professora](https://github.com/mfal-school/AVD-20262-pratica-streamlit/fork) para sua conta GitHub (`gbeloo`).
2. Copie os arquivos deste pacote para os mesmos caminhos no fork, preservando `notebooks/arquivo-eda-original.ipynb` e `notebooks/eda-com-downloads.ipynb` do modelo.
3. No fork, abra **Actions** e execute **Preparar dataset público**, caso o workflow não tenha gerado automaticamente o CSV.
4. No [Streamlit Community Cloud](https://share.streamlit.io), conecte ao GitHub, selecione seu fork, branch `main`, caminho `app.py` e Python 3.12.
5. Teste em aba anônima, confira os indicadores definidos no Dashboard 2, revise `entregas/justificativa-metricas.md`, preencha e assine a declaração oficial de IA e atualize a URL abaixo.

**Link do app:** PENDENTE DE PUBLICAÇÃO — substituir por `https://<nome>.streamlit.app`

## Entrega

- `notebooks/eda.ipynb`: cópia do notebook original de Pokémon.
- `app.py`: os dois painéis.
- `src/`: leitura e funções de análise.
- `data/clean/dataset.csv`: gerar via GitHub Actions e versionar.
- `entregas/`: rascunhos de layout + justificativa das métricas confirmadas pelo aluno, com redação revisada por IA (conferir antes da entrega).
- `prompts/`: registro do uso real da IA e declaração para assinatura.
- `tests/`: testes automatizados e checklist manual.

### Importante sobre a IA
Este projeto foi montado com apoio substancial do ChatGPT. Os trechos assistidos estão marcados `# [IA]` e o registro foi iniciado em `prompts/declaracao-uso-ia.md`. **Não declarar que houve somente auxílio pontual se trechos de código foram efetivamente gerados.** O PDF oficial da declaração deve ser preenchido e assinado pelo aluno.
