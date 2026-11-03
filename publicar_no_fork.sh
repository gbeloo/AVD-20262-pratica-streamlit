#!/usr/bin/env bash
set -euo pipefail

# [IA] ChatGPT - automacao dos comandos de ambiente, testes e commit no fork autorizado.
echo '=== Verificando repositório GitHub ==='
remote="$(git remote get-url origin)"
if [[ "$remote" != *"gbeloo/AVD-20262-pratica-streamlit"* ]]; then
  echo 'ERRO: abra o Codespace do fork gbeloo/AVD-20262-pratica-streamlit, nao o modelo da professora.'
  echo "Remoto encontrado: $remote"
  exit 1
fi
if [[ "$(git branch --show-current)" != "main" ]]; then
  echo 'ERRO: selecione a branch main antes de executar.'
  exit 1
fi

echo '=== Instalando dependências ==='
python -m pip install -r requirements.txt
python -m pip install 'pytest>=8,<10'

echo '=== Preparando dataset público completo ==='
python scripts/prepare_data.py
if [[ ! -s data/clean/dataset.csv ]]; then
  echo 'ERRO: o dataset completo nao foi exportado. Nenhum commit foi feito.'
  exit 1
fi

echo '=== Testando ==='
python -m pytest -q tests/test_analytics.py
python -m compileall -q app.py src scripts

echo '=== Preparando commit ==='
git add app.py README.md requirements.txt .gitignore .streamlit .github src scripts tests data/clean notebooks/eda.ipynb notebooks/eda-com-downloads.ipynb entregas prompts INSTRUCOES_IPHONE.md publicar_no_fork.sh
if git diff --cached --quiet; then
  echo 'Nenhuma alteracao a commitar.'
else
  git commit -m 'feat: app Streamlit de Pokemon com dois dashboards e testes'
fi

echo '=== Enviando para main ==='
git push origin main

echo '=== SUCESSO: projeto enviado ao fork ==='
echo 'PROXIMO PASSO: publicar em https://share.streamlit.io e atualizar o README com o link real.'
