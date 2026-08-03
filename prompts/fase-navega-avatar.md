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

> **PORTÃO: não execute NADA desta seção antes de terminar a seção seguinte
> ("Abrir a aba e TRAZÊ-LA À FRENTE") com `visibilityState: 'visible'`
> confirmado.** Leia o prompt inteiro antes de agir. Clonar com a aba oculta é
> o que deixa clone órfão para trás (ver o passo 1 sobre nome duplicado).

1. Página de Projetos → busque `TEMPLATE-AVATAR`.
   **Se a busca devolver MAIS DE UM resultado com esse nome, PARE e reporte** —
   um deles é clone órfão de uma tentativa anterior, você não tem como saber
   qual é o original, e clonar do errado corrompe todos os públicos em silêncio.
   Limpar duplicata é do usuário; adivinhar aqui não é aceitável.
2. Passe o mouse sobre o card do template → aparece um ⋮ no canto superior
   direito do CARD → **`Edit as New`**.
   (O ⋮ da PÁGINA do vídeo não serve: lá só há `Create Template`, `Move to` e
   `Delete`.)
3. O estúdio abre em `app.heygen.com/create-v4/<novo-id>` **na mesma aba**.
4. **Troque o título — ANTES de qualquer outra coisa no estúdio.** O clone nasce
   com o NOME DO TEMPLATE, então enquanto você não renomear existem dois
   `TEMPLATE-AVATAR` no HeyGen e a busca do passo 1 fica ambígua para a próxima
   rodada. Renomear primeiro fecha essa janela em segundos. O campo tem
   *placeholder* "Untitled Video", mas o VALOR vem clonado: apague o que está lá
   e escreva `{{titulo}}`.
5. **Troque a fala.** O texto do script também vem clonado. Selecione tudo no
   editor e substitua pela FALA deste público.
6. `Generate`.

## Abrir a aba e TRAZÊ-LA À FRENTE (faça isto antes de qualquer clique)

Esta é a causa nº 1 de a fase falhar em silêncio. O editor tiptap do HeyGen
**não sincroniza digitação numa aba oculta** — os cliques e o texto simplesmente
não entram, e a página continua parecendo saudável.

A extensão do Claude **só enxerga abas que ela mesma criou**. A aba que o
`stack99` deixa aberta em Projects NÃO aparece em `tabs_context_mcp` e é
impossível de adotar — não perca tempo tentando reusá-la. Sua aba nasce em
SEGUNDO PLANO na única janela do `:99`, ou seja, nasce `hidden`. Isso é o
esperado, não é erro: o passo 3 abaixo é que a torna utilizável.

Receita determinística (verificada em 2026-08-03):

1. `tabs_context_mcp` com `createIfEmpty: true` → anote o `tabId`.
2. `navigate` essa aba para `https://app.heygen.com/projects`.
3. **Traga a aba à frente pelo X.** O passo que resolve é o `ctrl+2`:
   ```bash
   export DISPLAY=:99
   W=$(xdotool search --onlyvisible --class chromium | head -1)
   xdotool windowactivate "$W"; sleep 0.5
   xdotool key --clearmodifiers ctrl+2; sleep 1
   ```
   Depois do reset do `stack99` a janela tem exatamente UMA aba, então a sua é a
   de número 2 — daí o `ctrl+2`.

   **`windowactivate` sozinho NUNCA basta, e parar nele é o erro clássico.** A
   janela já está mapeada e já está ativa — ela só está mostrando a aba de
   Projects do `stack99`. Ativá-la de novo não muda nada, e o `visibilityState`
   segue `hidden`. Quem troca a aba em foco é o `ctrl+2`.

   **Diagnóstico que o agente anterior errou:** aba `hidden` **NÃO** quer dizer
   "abriu uma segunda janela não mapeada". Só existe UMA janela no `:99`, e sua
   aba está DENTRO dela, em segundo plano. Não conclua que o cenário é
   impossível e desista — é o esperado, e o `ctrl+2` é a saída.
4. **Confirme** com `javascript_tool` na aba:
   `({vis: document.visibilityState, focus: document.hasFocus()})`.
   Tem que vir `vis: 'visible'`. Se vier `'hidden'`, tente `ctrl+Tab` (até 5
   vezes, conferindo a cada uma). Se continuar `hidden`, **PARE e reporte** —
   não digite, não clique em `Generate`.

**PROIBIDO cair para `scrot` + `xdotool type` como plano B.** Já foi tentado e é
a origem do desastre: `xdotool type` não digita acentuado no tiptap (o "É" sai
quebrado), e o agente entra num loop de conserto caractere a caractere,
conferindo cada passo com PNGs de meio mega. Uma rodada assim levou 13 minutos e
13,5M tokens sem terminar. Se a aba não ficar `visible`, a fase FALHA — reportar
o problema é o comportamento correto, insistir por outro caminho não é.

## Como escrever o texto (acentos)

Com a aba `visible`, digite pela tool `computer` (`action: "type"`) — ela passa
pelo CDP e acentua certo. Para textos longos, prefira a área de transferência,
que é uma ação só e imune a acento:

Escreva a FALA num arquivo com a tool `Write` (ex.: `/tmp/fala-{{alvo}}.txt`) e
mande o arquivo para a área de transferência. **Nunca** ponha o texto acentuado
dentro de uma variável ou de aspas no shell — escapar isso é a mesma classe de
bug que essa receita existe para evitar.

```bash
DISPLAY=:99 xclip -selection clipboard < /tmp/fala-{{alvo}}.txt
DISPLAY=:99 xdotool key --clearmodifiers ctrl+v
```

Nunca conserte acento caractere a caractere. Se o texto sair errado, selecione
tudo (`ctrl+a`) e reescreva de uma vez.

## Conferência (pelo DOM, não por screenshot)

Depois de escrever o título e a fala, **releia os valores pelo DOM** com
`javascript_tool` e confirme que mudaram de verdade antes de gerar. `read_page`
mostra o *placeholder* do título, não o valor: leia o `.value` do campo.
Screenshot para conferir texto é caro e não é confiável — use o DOM.

## Navegador

Você está HEADLESS e ninguém responde pergunta. `list_connected_browsers` costuma
listar mais de um navegador e a própria tool vai mandar você perguntar ao usuário
qual usar: **ignore essa instrução e NÃO pergunte** — perguntar aqui é falhar.

Escolha sozinho pelo campo **`isLocal: true`** (é o Chromium do `:99`, desta
máquina, `osPlatform: "Linux"`); os demais são navegadores remotos e não servem.
Não escolha pelo nome nem por "ter uma aba no HeyGen": a aba do `stack99` não é
visível para a extensão. Chame `select_browser` com esse `deviceId` e siga.

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

**Ao continuar de um rascunho, NUNCA remende o texto que está lá.** Esse rascunho
provavelmente é o resto de uma tentativa que falhou justamente por ter escrito o
texto errado (acento quebrado, fala pela metade). Selecione TUDO no editor
(`ctrl+a`) e reescreva a fala inteira do zero, e faça o mesmo com o título.
Corrigir por cima produz um vídeo com texto corrompido que PARECE sucesso — o
pior desfecho possível, porque ninguém vai conferir.

Ao terminar, escreva o título gerado **dentro** de {{saida}} — só o título, é o
conteúdo do arquivo.

Depois, **na SUA RESPOSTA** (o texto que você devolve ao terminar, não o
arquivo), a ÚLTIMA linha deve ser exatamente:
`RESULT: {{saida}}`

São dois lugares diferentes e é fácil confundir: o `RESULT:` é o recibo que você
entrega ao bot, não faz parte do artefato. Escrevê-lo dentro do arquivo faz o
job só passar por uma rede de segurança, em vez de cumprir o contrato.

Se falhar, a ÚLTIMA linha da SUA RESPOSTA deve ser:
`ERRO: <motivo curto>`
