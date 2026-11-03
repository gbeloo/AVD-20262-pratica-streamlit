"""EDA de Pokémon — app com dois painéis.

[IA] ChatGPT — apoio no esqueleto Streamlit, filtros, sintaxe de gráficos e
tratamento de estados vazios. O autor deve revisar e compreender todo o código.
Dashboard 2: público e métricas escolhidos pelo aluno; código desenvolvido com apoio da IA.
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from src.analytics import BASE_STATS, VARS_QUANT, aplicar_filtros, correlacao_spearman, calcular_kpi
from src.data_loader import load_data

st.set_page_config(page_title="Pokémon | Laboratório EDA", page_icon="🧬", layout="wide")
st.title("🧬 Pokémon | Laboratório EDA")
st.caption("Gabriel Nascimento Belo Osório · AVD 2026.2 · Base: Pokémon Stats (Kaggle)")
try:
    df = load_data()
except Exception as exc:
    st.error(f"Falha ao carregar os dados: {exc}")
    st.stop()

# [IA] ChatGPT — apoio na construção de widgets Streamlit e seu tratamento de limites.
with st.sidebar:
    st.header("Filtros gerais")
    variaveis = st.multiselect("Variáveis para análise", VARS_QUANT, default=BASE_STATS,
                              help="Escolha os atributos do laboratório de correlação e distribuição.")
    variavel_intervalo = st.selectbox("Atributo do filtro de intervalo", VARS_QUANT)
    minimo = float(df[variavel_intervalo].min())
    maximo = float(df[variavel_intervalo].max())
    intervalo = st.slider(f"Intervalo de {variavel_intervalo}", min_value=minimo,
                         max_value=maximo, value=(minimo, maximo), step=1.0)
    geracoes = st.multiselect("Gerações", sorted(df["generation"].dropna().unique().tolist()),
                              default=sorted(df["generation"].dropna().unique().tolist()))
    tipos = st.multiselect("Tipo primário", sorted(df["type1"].dropna().unique().tolist()),
                           default=sorted(df["type1"].dropna().unique().tolist()))
    classe = st.selectbox("Categoria", ["Todos", "Lendário", "Não lendário"])

filtrado = aplicar_filtros(df, variavel_intervalo, intervalo, geracoes, tipos, classe)
st.caption(f"Registros exibidos: **{len(filtrado)} de {len(df)}**. As formas alternativas fazem parte da base.")
aba1, aba2 = st.tabs(["📊 Dashboard 1 · Distribuição e correlação",
                       "🎯 Dashboard 2 · KPIs por público-alvo"])

with aba1:
    st.subheader("Laboratório de distribuição e correlação")
    st.write("Explore o formato das distribuições e as associações entre atributos, com os mesmos critérios da EDA original.")
    if filtrado.empty:
        st.warning("Nenhum Pokémon corresponde aos filtros. Amplie os intervalos ou categorias.")
    else:
        a,b = st.columns([1.1, 1.3])
        with a:
            st.markdown("**Correlação de Spearman**")
            if len(variaveis) < 2:
                st.info("Selecione pelo menos duas variáveis para o mapa de calor.")
            else:
                cor = correlacao_spearman(filtrado, variaveis)
                if cor.empty or cor.isna().all().all():
                    st.info("Não há variação suficiente para calcular correlações.")
                else:
                    graf = go.Figure(data=go.Heatmap(z=cor.values, x=cor.columns, y=cor.index,
                        zmin=-1, zmax=1, colorscale="RdBu", reversescale=True,
                        text=cor.round(2).fillna(0).values, texttemplate="%{text:.2f}",
                        colorbar=dict(title="ρ"), hovertemplate="%{y} × %{x}: %{z:.2f}<extra></extra>"))
                    graf.update_layout(margin=dict(l=0,r=0,b=30,t=20), height=420)
                    st.plotly_chart(graf, use_container_width=True)
                    st.caption("`total` é a soma dos seis atributos; sua correlação não é evidência independente.")
        with b:
            st.markdown("**Histogramas**")
            if not variaveis:
                st.info("Selecione uma ou mais variáveis na barra lateral.")
            else:
                for ix in range(0, len(variaveis), 2):
                    cols = st.columns(2)
                    for bloco, var in zip(cols, variaveis[ix:ix+2]):
                        fig = px.histogram(filtrado, x=var, nbins=25, marginal="box",
                                title=var.replace('_',' ').title(), color_discrete_sequence=["#6963af"])
                        fig.update_layout(showlegend=False, height=285, margin=dict(l=0,r=0,t=45,b=0))
                        bloco.plotly_chart(fig, use_container_width=True, key=f"hist_{var}")


with aba2:
    st.subheader("Pokémon em números — visão para iniciantes")
    st.caption(
        "Público-alvo: jogadores iniciantes. O painel apresenta indicadores simples "
        "para conhecer os atributos dos Pokémon e explorar a base com filtros."
    )

    # [IA] ChatGPT — implementação da interface; escolhas de público e métricas confirmadas pelo aluno.
    publico = st.text_input(
        "Público-alvo",
        value="Jogadores iniciantes de Pokémon",
        help="Público escolhido: jogadores iniciantes de Pokémon.",
    )

    st.markdown("### Indicadores")
    st.caption("Indicadores escolhidos: quantidade de registros analisados, ataque médio e defesa média. Os filtros atualizam os valores.")
    quantidade = st.slider("Quantidade de indicadores", min_value=3, max_value=5, value=3)

    atributos = ["Selecionar..."] + VARS_QUANT
    operacoes = ["Selecionar...", "Média", "Mediana", "Máximo", "Mínimo", "Desvio padrão", "Contagem"]
    exemplos = [
        ("total", "Contagem"),
        ("attack", "Média"),
        ("defense", "Média"),
    ]
    rotulos = {
        ("total", "Contagem"): "Registros analisados",
        ("attack", "Média"): "Ataque médio",
        ("defense", "Média"): "Defesa média",
    }
    descricoes = {
        ("total", "Contagem"): "Número de registros na amostra filtrada, incluindo formas alternativas.",
        ("attack", "Média"): "Média aritmética do atributo de ataque na amostra filtrada.",
        ("defense", "Média"): "Média aritmética do atributo de defesa na amostra filtrada.",
    }

    indicadores = []
    for i in range(quantidade):
        atributo_padrao, operacao_padrao = exemplos[i] if i < len(exemplos) else ("Selecionar...", "Selecionar...")
        a, b = st.columns(2)
        var = a.selectbox(
            f"Atributo do indicador {i + 1}", atributos,
            index=atributos.index(atributo_padrao), key=f"kpi_var_{i}"
        )
        op = b.selectbox(
            f"Cálculo do indicador {i + 1}", operacoes,
            index=operacoes.index(operacao_padrao), key=f"kpi_calc_{i}"
        )
        indicadores.append((var, op))

    colunas = st.columns(quantidade)
    for numero, ((var, op), col) in enumerate(zip(indicadores, colunas), start=1):
        valor = calcular_kpi(filtrado, var, op)
        nome = rotulos.get((var, op), f"{op} de {var}" if valor is not None else f"Indicador {numero}")
        col.metric(nome, "—" if valor is None else f"{valor:,.0f}" if op == "Contagem" else f"{valor:,.1f}")
        if (var, op) in descricoes:
            col.caption(descricoes[(var, op)])

    st.divider()
    st.markdown("### Três gráficos interativos")
    st.caption("Use os gráficos para enxergar a distribuição dos atributos e comparar grupos.")

    if filtrado.empty:
        st.warning("Os filtros atuais não retornaram Pokémon. Ajuste o painel lateral.")
    else:
        # [IA] ChatGPT — sintaxe Altair para três visuais-modelo e seus controles.
        import altair as alt
        tipos_grafico = ["Escolher gráfico...", "Histograma", "Barras por geração", "Boxplot por classe"]
        graficos_padrao = [
            ("Histograma", "attack"),
            ("Barras por geração", "defense"),
            ("Boxplot por classe", "hp"),
        ]
        visuais = st.columns(3)
        for i, area in enumerate(visuais):
            tipo_inicial, atributo_inicial = graficos_padrao[i]
            with area:
                st.markdown(f"**Gráfico {i + 1}**")
                tipo_grafico = st.selectbox(
                    f"Tipo do gráfico {i + 1}", tipos_grafico,
                    index=tipos_grafico.index(tipo_inicial), key=f"tipo_visual_{i}"
                )
                variavel_grafico = st.selectbox(
                    f"Atributo do gráfico {i + 1}", atributos,
                    index=atributos.index(atributo_inicial), key=f"var_visual_{i}"
                )
                if variavel_grafico not in VARS_QUANT or tipo_grafico == "Escolher gráfico...":
                    st.info("Escolha um gráfico e uma variável.")
                    continue

                if tipo_grafico == "Histograma":
                    chart = alt.Chart(filtrado).mark_bar(color="#6963af").encode(
                        x=alt.X(f"{variavel_grafico}:Q", bin=alt.Bin(maxbins=20), title=variavel_grafico),
                        y=alt.Y("count():Q", title="Quantidade de registros"),
                        tooltip=[alt.Tooltip("count():Q", title="Registros")]
                    )
                elif tipo_grafico == "Barras por geração":
                    medias = filtrado.groupby("generation", as_index=False)[variavel_grafico].mean()
                    chart = alt.Chart(medias).mark_bar(color="#aa69bd").encode(
                        x=alt.X("generation:O", title="Geração"),
                        y=alt.Y(f"{variavel_grafico}:Q", title=f"Média de {variavel_grafico}"),
                        tooltip=["generation:O", alt.Tooltip(f"{variavel_grafico}:Q", format=".1f")]
                    )
                else:
                    chart = alt.Chart(filtrado).mark_boxplot(size=35, color="#4c8699").encode(
                        x=alt.X("legendary_label:N", title="Categoria"),
                        y=alt.Y(f"{variavel_grafico}:Q", title=variavel_grafico)
                    )
                st.altair_chart(chart.properties(height=300), use_container_width=True)

    st.info(
        "Indicadores e público selecionados pelo aluno. A redação do arquivo de justificativas foi revisada com IA; "
        "registre esse apoio e a conferência dos cálculos na declaração obrigatória."
    )
