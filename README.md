# promoavatar

Repo de **domínio** do fluxo `/promoavatar` do inemaccbot: reels de divulgação
para 12 públicos, com portão humano no meio.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/promoavatar/guia/**

O bot escreve os roteiros e PARA. Você grava os avatares no HeyGen; quando
terminar, libera e ele baixa, monta os reels e entrega em cada canal.

Aqui não há código — só a **definição** do pipeline. Um fluxo novo é uma entrada
no registry do bot mais um repo como este, sem uma linha de TypeScript.

## O que tem aqui

| arquivo | o que é |
|---|---|
| `flow.json` | as fases, os 12 públicos, o canal e o gatilho de cada um |
| `prompts/fase1-texto.md` | o que o agente recebe para escrever os roteiros |
| `HELP.md` | a ajuda que aparece no chat em `/promoavatar help` |
| `textos/A<N>/` | os roteiros gerados, um arquivo por público |
| `docs/pipeline.md` | **a tabela de tudo**: etapas, LLM/IA/worker, custo e tempo |
| `docs/canais-e-destinos.md` | para quem e onde fica cada reel |
| `docs/` | as demais decisões e o que ainda está aberto |

## Para quem, e onde fica

É a pergunta que mais gera dúvida, então em resumo — o detalhe está em
[`docs/canais-e-destinos.md`](docs/canais-e-destinos.md):

| pergunta | quem responde | onde ajustar |
|---|---|---|
| **para quem** é o reel | este repo | `flow.json`, campo `canal` do público |
| **onde fica** o canal no disco | o bot | derivado: `~/projetos/yt-pub-<canal>/imports/videos` |

Exemplo: `mulheres` tem `"canal": "lives24"`, então o reel dela é entregue em
`~/projetos/yt-pub-lives24/imports/videos`.

O caminho **não está escrito em lugar nenhum** — é sempre
`~/projetos/yt-pub-<canal>/imports/videos`. Por isso:

- **trocar o canal de um público** = editar o `flow.json` (vale no próximo fluxo);
- **criar um canal novo** = `mkdir -p ~/projetos/yt-pub-lives33/imports/videos`,
  sem tocar no bot.

## O ciclo, em uma tela

```
/promoavatar <assunto> [--alvo=mulheres]
        │
        ▼
  1. texto     UM roteiro por público, gravado em textos/A<N>/<publico>.md
        │
        ⏸️  PARA — o chat te manda cada roteiro com o TÍTULO do vídeo
        │      você grava no HeyGen com esse nome exato
        │      /aprovar A#<N>
        ▼
  2. baixar    acha o vídeo pelo título e baixa (janela de 90 min)
        │
        ▼
  3. reel      monta o reel 9:16 e ENTREGA no canal do público
        │
        ▼
  ✅ link do vídeo final no chat
```

## O título é o contrato

No estúdio, o vídeo precisa se chamar **exatamente**:

```
A<N>-<publico>-v1        ex.: A8-mulheres-v1
```

O download casa por igualdade exata de string. Nome diferente = vídeo nunca
encontrado, e a fase expira em 90 minutos. O chat te manda o título pronto junto
de cada roteiro, justamente para não ser digitado de memória.

## Opções na criação

| opção | padrão | o que faz |
|---|---|---|
| `--alvo=jovens` (repetível) ou `\| alvos=a,b` | todos os 12 | só esses públicos |
| `\| legenda` ou `\| legenda=sim` | **SEM legenda** | legenda palavra-a-palavra no reel, com a caixa encostada na borda INFERIOR |
| `\| versao=N` | 1 | muda o `-vN` do título do estúdio |
| `\| de=<fase>` | — | começa no meio (você já fez texto e/ou avatar) |
| `\| sombra` | — | mostra o plano, não enfileira nada |

```
/promoavatar <assunto> --alvo=jovens --legenda
```

Legenda é decisão de quem publica, por isso o padrão é não ter. Ligar é
explícito, na criação — e vale para o fluxo inteiro.

### Legenda: o que vem da HeyGen e o que é nosso

Essa opção controla **só a legenda que o nosso editor desenha**. Ela não vê o
MP4 que veio do HeyGen: se o avatar chegar com legenda **queimada nos pixels**,
ela sobrevive ao reel inteiro, mesmo com a opção desligada — não existe etapa de
remoção, máscara ou inpaint no pipeline.

O que a API do HeyGen oferece (`video_status.get`):

| campo | o que é | usamos? |
|---|---|---|
| `video_url` | MP4 **sem** legenda queimada | **sim, sempre** |
| `video_url_caption` | MP4 **com** legenda queimada | não |
| `caption_url` | legenda solta (arquivo), quando existe | não |

O download do bot lê **só `video_url`**
(`inemaccbot/src/fila/tarefas/heygen.ts`).

**Não dá para escolher nada na hora de baixar.** O download é um `GET` numa URL
pronta — não há `?estilo=`, `?formato=`, `?idioma=`. Seis endpoints de legenda
foram sondados (`v1/video.caption`, `v2/video/caption`, `v1/video.subtitle`,
`v1/caption.list`, `v2/caption_styles`, `v2/video/<id>`) e deram **404 nos
seis**. Estilo, fonte e posição da legenda queimada se decidem **no estúdio,
antes de renderizar**; depois disso estão nos pixels, e só regravando.

**O que foi medido (2026-08-01, chave real da conta):** os 25 vídeos completos
mais recentes — `video_url_caption` nulo e `caption_url` vazio em **todos**.
Nenhum vídeo da conta tem legenda hoje.

**O que NÃO foi medido:** o comportamento com a legenda **ligada** no estúdio.
Os nomes dos campos sugerem que `video_url` continuaria limpo e o
`video_url_caption` passaria a vir preenchido — mas não há observação que prove
isso, e a hipótese contrária (a legenda entrar no render principal) não está
descartada. **Até alguém testar, a garantia é uma só: gravar SEM legenda no
estúdio.** O teste custa um vídeo: renderize um com legenda ligada e olhe os
dois campos.

Consequências práticas de deixar passar uma legenda queimada:

- ela vem posicionada para o enquadramento 16:9, não para a faixa do meio do
  9:16 — pode ser cortada ou colidir com a base;
- com a opção `legenda` ligada, saem **duas** legendas.

## Onde mudar o quê

A regra: **o que é decisão de público ou de campanha mora neste repo; o que é
identidade visual da marca mora na skill.** A skill é global — mexer nela muda
TODO reel, inclusive os disparados direto no chat.

| quero mudar… | arquivo | camada |
|---|---|---|
| o canal de um público | `flow.json` → `alvos.<publico>.canal` | domínio |
| o gancho de um público | `flow.json` → `alvos.<publico>.gatilho` | domínio |
| **como os roteiros são escritos** | `prompts/fase1-texto.md` | domínio |
| **o que este fluxo pede ao reel** | `flow.json` → fase `reel`, campo `entrega` | domínio |
| **o clipe de CTA do fim** | `cta/cta-9x16.mp4` — troque o arquivo | domínio |
| a ajuda do chat | `HELP.md` | domínio |
| **como o reel é MONTADO** (cores, fontes, posições, SFX, modos) | `~/.claude/skills/reel-edita-inema/SKILL.md` | skill (global) |
| o que o agente recebe antes de chamar a skill | `inemaccbot/prompts/reel.md` | bot |
| filas, timeouts, modelo e esforço | `inemaccbot/config/skills.json` | bot |

### O prompt do texto (`prompts/fase1-texto.md`)

É onde vivem, nesta ordem:

1. **CONTEXTO FIXO** — o que o agente já sabe (Nei e Tiza são os gestores da
   comunidade), para não citar nome sem função nem inventar quem são.
2. **NÃO MEXA NA MÁQUINA** — proibição de instalar qualquer coisa. Um render
   instalou um binário errado seguindo dica de log e derrubou o render seguinte.
3. **PASSO ZERO** — tese central, elemento demonstrável e a escolha explícita de
   um formato entre 11. Sem escolher, o agente cai sempre em dor→solução→CTA,
   que é molde de anúncio, e anúncio não é compartilhado.
4. **OFICINA DE GANCHO** — cinco primeiras frases por público, quatro
   descartadas POR ESCRITO. O critério é o teste da lacuna: depois da frase, a
   pessoa precisa da próxima para fechar o sentido? Se a frase se basta, é
   afirmação, não gancho. Teto de 9 palavras.
5. **REGRAS DE ESCRITA** — as 16 regras: gancho nos 2 primeiros segundos, dor
   antes da solução, nomear a profissão, benefício antes da mecânica, frases
   curtas, promessa do tamanho certo, CTA imperativo, nada de placeholder, nada
   de urgência inventada, as SOBREPOSIÇÕES como roteiro VISUAL com os quatro
   gatilhos (atenção · retenção · engajamento · CTA), a lacuna vivendo na FALA,
   valor completo antes da marca, a última frase decidindo o compartilhamento, e
   escrever para UMA pessoa concreta.
6. **O contrato de saída** — `{{pasta}}`, `RESULT:`/`ERRO:`.

Variáveis que o bot injeta: `{{input}}` (o assunto), `{{publicos}}` (os alvos
REAIS do fluxo), `{{pasta}}` (onde gravar, absoluto), `{{ref}}`, `{{saida}}`.

#### Assunto que é DEBATE: o prompt crava uma posição

Assunto que chega como pergunta em aberto ("isso é bom ou ruim?", "o que você
acha?") tinha um resultado previsível: o agente explicava os dois lados e
fechava em "o importante é se preparar". Correto e morno — ninguém comenta com
equilibrista, e o vídeo é visto e esquecido.

A causa não era falta de talento: são as regras 9 e 10 (não invente dado, não
invente urgência) fazendo o agente recuar até o meio-termo, que é o único lugar
onde ele tem certeza de não estar afirmando nada.

Então o prompt agora manda **tomar um lado** nesse caso, e **escrever no resumo
qual posição cravou e por quê**. Isso não afrouxa as regras 9 e 10: opinião é
permitida, fato inventado não.

**A posição que você mandar vence a dele.** Se você escreve a sua no assunto, ele
usa a sua; o bloco só existe para quando você não escreveu. Escrever a sua
continua sendo o melhor caminho — junto com um fato concreto (para a linha PROVA
não ficar vazia) e a pergunta que você quer nos comentários.

Como o resumo diz a posição escolhida, você discorda dela **no portão**, antes de
gerar avatar nenhum — `/refazer` custa um texto, não um render.

### O estilo do reel — duas camadas

O `entrega` da fase `reel` no `flow.json` é o que ESTE pipeline pede: os quatro
gatilhos, a headline a partir do `{gatilho}` do público, e os dois marcadores
que a criação resolve — `{legenda}` e `{cta}`.

A skill `reel-edita-inema` é quem sabe montar: composição empilhada 9:16, cores,
fontes, corte de silêncio, legenda palavra-a-palavra, SFX. Mudar ali muda a
marca inteira.

**Melhorar o reel, na ordem do mais barato:** trocar o clipe de `cta/`; ajustar
o `entrega` do `flow.json`; e só então mexer na skill.

## Atenção: tudo aqui é congelado na criação

O `flow.json`, os prompts e as opções (`legenda`, `cta`) são **congelados quando
o fluxo nasce**. Editar vale para os PRÓXIMOS — um fluxo em andamento não muda
de regra no meio do caminho, e por isso nem `/refazer` pega a mudança.
