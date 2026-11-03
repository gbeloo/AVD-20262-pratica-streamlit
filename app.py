"""EDA de Pokémon — app com dois painéis.

[IA] ChatGPT — apoio no esqueleto Streamlit, filtros, sintaxe de gráficos e
tratamento de estados vazios. O autor deve revisar e compreender todo o código.
Dashboard 2: métricas, justificativas e público-alvo devem ser definidos pelo autor.
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
    st.subheader("Painel para um público definido pelo autor")
    st.warning("Atenção: escolha e justifique pessoalmente as métricas e o público-alvo. A IA foi usada apenas como apoio à implementação.")
    # [IA] ChatGPT — estrutura genérica para o aluno configurar os próprios KPIs, não suas escolhas.
    publico = st.text_input("Público-alvo definido por você", placeholder="Ex.: escreva aqui o público que VOCÊ escolheu")
    if not publico.strip():
        st.caption("Público-alvo ainda não definido. Configure as métricas a seguir e registre suas justificativas em entregas/justificativa-metricas.md.")
    quantidade = st.slider("Número de métricas", min_value=3, max_value=5, value=3)
    st.markdown("**Escolha as 3 a 5 métricas do seu painel**")
    specs=[]
    for i in range(quantidade):
        col_a, col_b = st.columns([1,1])
        var = col_a.selectbox(f"Variável do KPI {i+1}", ["Selecionar..."]+VARS_QUANT, key=f"kpi_var_{i}")
        operacao = col_b.selectbox(f"Cálculo do KPI {i+1}", ["Selecionar...", "Média", "Mediana", "Máximo", "Mínimo", "Desvio padrão", "Contagem"], key=f"kpi_calc_{i}")
        specs.append((var,operacao))
    colunas=st.columns(quantidade)
    for i,((var,op),col) in enumerate(zip(specs,colunas),start=1):
        valor=calcular_kpi(filtrado,var,op)
        col.metric(f"KPI {i}: {op} de {var}" if valor is not None else f"KPI {i}: a definir",
                   f"{valor:,.1f}" if valor is not None else "—")
    st.divider()
    st.markdown("**Três visuais interativos — escolha as variáveis e confirme se fazem sentido para o seu público**")
    if filtrado.empty:
        st.info("Sem registros para exibir no Dashboard 2.")
    else:
        # [IA] ChatGPT — estrutura e sintaxe Altair; o aluno escolhe quais 3 gráficos usar.
        import altair as alt
        tipos_grafico = ["Escolher gráfico...", "Histograma", "Barras por geração", "Boxplot por classe"]
        visuais = st.columns(3)
        for i, area in enumerate(visuais, start=1):
            with area:
                st.markdown(f"**Visual {i}**")
                tipo_grafico = st.selectbox(f"Gráfico {i}", tipos_grafico, key=f"tipo_visual_{i}")
                variavel_grafico = st.selectbox(f"Variável do gráfico {i}",
                                               ["Selecionar..."] + VARS_QUANT, key=f"var_visual_{i}")
                if variavel_grafico not in VARS_QUANT or tipo_grafico == "Escolher gráfico...":
                    st.info("Escolha o tipo de gráfico e a variável que você deseja mostrar.")
                    continue
                if tipo_grafico == "Histograma":
                    chart = alt.Chart(filtrado).mark_bar(color="#6963af").encode(
                        x=alt.X(f"{variavel_grafico}:Q", bin=alt.Bin(maxbins=20)),
                        y=alt.Y("count():Q", title="Registros"),
                        tooltip=[alt.Tooltip("count():Q", title="Registros")]
                    )
                elif tipo_grafico == "Barras por geração":
                    medias = filtrado.groupby("generation", as_index=False)[variavel_grafico].mean()
                    chart = alt.Chart(medias).mark_bar(color="#aa69bd").encode(
                        x=alt.X("generation:O", title="Geração"),
                        y=alt.Y(f"{variavel_grafico}:Q", title=f"Média · {variavel_grafico}"),
                        tooltip=["generation", alt.Tooltip(f"{variavel_grafico}:Q", format=".1f")]
                    )
                else:
                    chart = alt.Chart(filtrado).mark_boxplot(size=35, color="#4c8699").encode(
                        x=alt.X("legendary_label:N", title="Categoria"),
                        y=alt.Y(f"{variavel_grafico}:Q", title=variavel_grafico)
                    )
                st.altair_chart(chart.properties(height=300), use_container_width=True)
    st.caption("KPIs exibidos são cálculos exploratórios. Para a entrega, registre escolhas, justificativas e validação autorais no arquivo exigido.")
