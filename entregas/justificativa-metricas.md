# Justificativa das métricas — Dashboard 2

**Público-alvo escolhido:** jogadores iniciantes de Pokémon.

**Objetivo:** apresentar informações fáceis de visualizar sobre os Pokémon, sem exigir que um iniciante interprete muitos números ou estatísticas de uma vez. Eu escolhi a contagem de registros, o ataque médio e a defesa média porque são indicadores simples de entender.

## Indicador 1 — Registros analisados
- **Variável e cálculo:** `total` — contagem de registros não nulos.
- **O que mede:** a quantidade de registros de Pokémon que restam após os filtros. Formas alternativas também são contadas, então não representa o número de espécies únicas.
- **Por que escolhi:** o número é direto e fácil de visualizar. Mostra de maneira rápida quantos registros estão entrando na análise e muda quando aplico os filtros.
- **O que comunica:** o tamanho da amostra usada para os outros indicadores.

## Indicador 2 — Ataque médio
- **Variável e cálculo:** `attack` — média aritmética.
- **O que mede:** o valor médio de ataque dos registros filtrados.
- **Por que escolhi:** ataque é um atributo básico que os iniciantes reconhecem. A média reúne vários valores em um número só e facilita entender o nível geral de ataque, sem olhar Pokémon por Pokémon.
- **O que comunica:** uma referência geral do atributo de ataque dentro da seleção.

## Indicador 3 — Defesa média
- **Variável e cálculo:** `defense` — média aritmética.
- **O que mede:** o valor médio de defesa dos registros filtrados.
- **Por que escolhi:** defesa também é um atributo básico e fácil de visualizar. Junto do ataque médio, dá para observar dois atributos importantes lado a lado de forma simples.
- **O que comunica:** uma referência geral da defesa dos Pokémon incluídos nos filtros.

## Visuais do painel
- **Histograma de ataque:** mostra a distribuição dos valores de ataque.
- **Gráfico de barras por geração:** mostra a média de defesa em cada geração.
- **Boxplot de HP por categoria:** permite observar a distribuição de HP entre Pokémon lendários e não lendários.

## Conferência e observações
- Os três indicadores respondem aos filtros de geração, tipo, categoria e intervalo de atributo.
- A contagem inclui formas alternativas que aparecem como registros separados no dataset.
- Uma média serve como resumo dos valores e não informa, sozinha, o desempenho de cada Pokémon.
- **Conferência pessoal pendente:** executar o painel, testar mudanças nos filtros e conferir os números antes da entrega.

**Transparência:** o aluno definiu público, indicadores e o motivo de serem fáceis de visualizar; a redação foi revisada com apoio do ChatGPT e deve constar na declaração de IA, conforme as regras da atividade.
