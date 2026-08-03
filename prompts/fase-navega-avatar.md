Gere O VÍDEO DE AVATAR deste público CLONANDO um template no estúdio do HeyGen,
pelo navegador. NÃO monte cena do zero e NÃO escolha avatar, voz, cenário nem
proporção: tudo isso vem pronto do template.

<publico>{{alvo}}</publico>
<assunto>{{input}}</assunto>

Título EXATO do vídeo no estúdio (não invente outro — é por ele que o download
encontra o vídeo depois): {{titulo}}

Fonte da fala: a seção FALA do arquivo `{{pasta}}/{{alvo}}.md`, gerado na fase 1.

## O template

Projeto de origem no HeyGen: **`TEMPLATE-AVATAR`**. Ache-o pela BUSCA da página
de Projetos (campo "Search videos and folders"), nunca pegando "o mais recente"
da lista — a lista anda a cada vídeo gerado, e clonar do vídeo errado erra todos
os públicos em silêncio.

O template já está com avatar, voz, cenário, motor Avatar III e proporção 16:9
corretos. NÃO confira nem mexa em nenhum deles: no estúdio não dá para ler com
segurança qual botão de proporção está selecionado, e "conferir" ali acaba
virando um clique que MUDA o que estava certo. Se o template estiver errado, o
conserto é no template, não aqui.

## O caminho (verificado em 2026-08-03)

1. Página de Projetos → busque `TEMPLATE-AVATAR`.
2. Passe o mouse sobre o card do template → aparece um ⋮ no canto superior
   direito do CARD → **`Edit as New`**.
   (O ⋮ da PÁGINA do vídeo não serve: lá só há `Create Template`, `Move to` e
   `Delete`.)
3. O estúdio abre em `app.heygen.com/create-v4/<novo-id>` **na mesma aba**.
4. **Troque o título.** O campo do título tem *placeholder* "Untitled Video",
   mas o VALOR vem clonado do template — ou seja, ele chega preenchido com o
   nome do template, não vazio. Apague o que está lá e escreva `{{titulo}}`.
5. **Troque a fala.** O texto do script também vem clonado. Selecione tudo no
   editor e substitua pela FALA deste público.
6. `Generate`.

## Antes de digitar: a aba TEM que estar visível

Esta é a causa nº 1 de a fase falhar em silêncio. O editor tiptap do HeyGen
**não sincroniza digitação numa aba oculta** — os cliques e o texto simplesmente
não entram, e a página continua parecendo saudável.

- **REUSE a aba do HeyGen já aberta. NUNCA abra aba nova nem janela nova.** No
  display virtual `:99` só existe UMA janela mapeada; qualquer aba/janela nova
  nasce `hidden` para sempre e nada que você digitar terá efeito.
- Antes de digitar qualquer coisa, confirme com JavaScript na aba:
  `document.visibilityState` tem que ser `'visible'`. Se vier `'hidden'`, tente
  `xdotool windowactivate` na janela do Chromium do `:99`; se ainda assim ficar
  `hidden`, PARE e reporte — não digite, não clique em `Generate`.
- Depois de escrever o título e a fala, **releia os valores pelo DOM** e confirme
  que mudaram de verdade antes de gerar. `read_page` mostra o *placeholder* do
  título, não o valor: leia o `.value` do campo por JavaScript.

## Navegador

Você está HEADLESS e ninguém responde pergunta. Se houver mais de um navegador
conectado, NÃO pergunte qual usar — selecione automaticamente o navegador LOCAL
desta máquina (o que tem uma aba em `app.heygen.com`) via
`list_connected_browsers` + `select_browser`, e siga. Perguntar aqui é falhar.

## Honestidade

Só afirme que o vídeo foi gerado se você de fato usou as tools de navegador,
clicou em `Generate` e VIU o vídeo aparecer em Meus Projetos do HeyGen. Se não
tiver acesso a tools de navegador nesta execução, NÃO diga que gerou nada:
reporte exatamente isso e pare. Se algo travar (HeyGen deslogado, aba presa,
template não encontrado), pare e reporte o que travou — não insista em loop.

Se você trocou o título e falhou ANTES de gerar, sobra um rascunho com o título
de produção. Na tentativa seguinte, procure primeiro um RASCUNHO chamado
`{{titulo}}` e continue dele, em vez de clonar o template de novo — senão a
retentativa deixa um segundo rascunho homônimo para trás. Você NUNCA apaga nada
no HeyGen; limpeza de rascunho é do usuário.

Ao terminar, escreva o título gerado em {{saida}} e sua ÚLTIMA linha deve ser:
`RESULT: {{saida}}`

Se falhar, sua ÚLTIMA linha deve ser:
`ERRO: <motivo curto>`
