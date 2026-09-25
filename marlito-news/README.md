# Marlito News

Portal de notícias internacionais em português, estilo moderno/clean, com as
editorias **Mundo & Geopolítica**, **Tecnologia**, **Ciência** e **Cultura &
Entretenimento**. Publicado de graça no GitHub Pages, atualizado sozinho
todo dia via GitHub Actions. Nenhum custo, nenhuma chave de API.

## Como colocar no ar (uma vez só)

1. **Crie uma conta no GitHub**, se ainda não tiver: https://github.com/signup (grátis)

2. **Crie um repositório novo:**
   - Clique em "New repository"
   - Dê um nome, ex.: `marlito-news`
   - Marque como **Public** (necessário para o GitHub Pages gratuito e para o
     Actions rodar sem limite de minutos)
   - Não marque nenhuma opção de inicializar com README — vamos subir os arquivos prontos

3. **Suba estes arquivos para o repositório** (arraste e solte na tela do GitHub,
   ou use `git push` se preferir linha de comando), mantendo a estrutura de pastas:
   ```
   marlito-news/
   ├── index.html
   ├── template.html
   ├── generate.py
   ├── requirements.txt
   └── .github/
       └── workflows/
           └── atualizar.yml
   ```

4. **Ative o GitHub Pages:**
   - No repositório, vá em **Settings → Pages**
   - Em "Source", escolha **Deploy from a branch**
   - Branch: **main**, pasta: **/ (root)**
   - Salve. Em alguns minutos o site estará no ar em:
     `https://SEU-USUARIO.github.io/marlito-news/`

5. **Rode a primeira atualização automática manualmente** (para não esperar até o
   próximo dia):
   - Vá na aba **Actions** do repositório
   - Clique no workflow "Atualizar Marlito News"
   - Clique em **Run workflow**
   - Em cerca de um minuto, ele busca as notícias reais e substitui a edição
     de exemplo que já vem no `index.html`

Pronto. A partir daí, o workflow roda sozinho todo dia às 09h UTC (~06h em
Brasília) e atualiza as quatro editorias automaticamente — sem você precisar
fazer nada.

## Como funciona por baixo dos panos

- `generate.py` busca as notícias mais recentes em feeds RSS públicos e
  gratuitos, já em português:
  - **Mundo**: BBC News Brasil, DW Brasil
  - **Tecnologia**: TecMundo, Olhar Digital
  - **Ciência**: Super Interessante
  - **Cultura**: Omelete
- Ele preenche o `template.html` com a manchete e as matérias de cada
  editoria e salva o resultado como `index.html`
- O `.github/workflows/atualizar.yml` roda esse script todo dia, e se algo
  mudou, o próprio GitHub Actions commita e publica a atualização — usando
  uma permissão temporária que o GitHub já fornece de graça, sem senha nem
  chave de API

## Personalizar

- **Trocar as fontes de notícia:** edite o dicionário `FEEDS` no início do
  `generate.py` — qualquer site com feed RSS funciona, em qualquer categoria
- **Mudar o horário da atualização:** edite a linha `cron` no arquivo
  `.github/workflows/atualizar.yml` (formato cron, horário em UTC)
- **Mudar o visual:** o CSS inteiro está dentro do `template.html`

## Domínio próprio (opcional, não obrigatório)

O endereço `SEU-USUARIO.github.io/marlito-news` já funciona como site
público de verdade e não custa nada. Se um dia quiser um domínio próprio
(tipo `marlito.news`), basta registrá-lo em qualquer provedor e apontar para
o GitHub Pages nas configurações do repositório — isso sim tem um custo
anual, mas é totalmente opcional.
