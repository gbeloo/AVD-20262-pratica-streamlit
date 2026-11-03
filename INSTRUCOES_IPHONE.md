# Entrega pelo iPhone usando o fork já criado

Repositório: https://github.com/gbeloo/AVD-20262-pratica-streamlit

## 1. Importar o projeto no Codespaces
1. Baixe o ZIP da conversa para o aplicativo Arquivos do iPhone.
2. No Safari, abra https://github.com/gbeloo/AVD-20262-pratica-streamlit e procure Code → Codespaces → Create codespace on main. Se não aparecer direito, ative “Solicitar site para computador”.
3. No editor do Codespaces (VS Code no navegador), na barra Explorer (ícone de arquivos), use o menu `...` → **Upload...** e selecione o ZIP que você salvou no iPhone.
4. Abra o Terminal pelo menu do editor e execute, **na raiz do seu fork**, os comandos abaixo. Verifique a pasta com `pwd` e `git remote -v`: o remoto deve ser `gbeloo/AVD-20262-pratica-streamlit`.

```bash
unzip -o Pokemon_Gabriel_PARA_FORK_IPHONE.zip
bash publicar_no_fork.sh
```

**Atenção:** `unzip` sobrescreve arquivos de mesmo nome. O pacote não apaga arquivos extras do fork, incluindo o notebook original da professora. Se o arquivo tiver outro nome ao subir para Codespaces, adapte o comando `unzip`.

## 2. Publicar o app
1. Abra https://share.streamlit.io, faça login com sua conta GitHub.
2. Escolha **Create app / Deploy a public app from GitHub**.
3. Repository: `gbeloo/AVD-20262-pratica-streamlit`; branch: `main`; main file path: `app.py`; Python: `3.12`.
4. Aguarde o deploy finalizar e anote a URL real terminada em `.streamlit.app`.
5. No GitHub, edite `README.md` para substituir a linha `**Link do app:** PENDENTE...` pela URL publicada. Faça o commit pelo editor web.

## 3. Testes finais obrigatórios
- [ ] Abre em aba anônima, sem login.
- [ ] Os dois dashboards carregam pelas abas.
- [ ] Alterar seletor e slider modifica gráficos.
- [ ] Os sete histogramas aparecem ao selecionar as sete variáveis.
- [ ] Dados públicos, sem tokens, CPFs ou e-mails expostos.
- [ ] Os indicadores do Dashboard 2 foram escolhidos e justificados por você.
- [ ] Coloque no `prompts/` a **declaração oficial preenchida e assinada** com o nome `DECLARACAO_IA.pdf` e entregue no Classroom também. O PDF modelo do pacote não conta como declaração assinada.

## Observação
O registro de IA deve ser fiel: o ChatGPT gerou partes substantivas de código, documentação e testes. O público-alvo e as justificativas das métricas do Dashboard 2 precisam ser elaborados e validados individualmente.
