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
| `templates/*.json` | os 4 layouts do reel 9:16 + o `mapa.json` formato→layout |
| `scripts/*.py` | os motores do reel (`preparar.py`, `montar-reel.py`) |
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

Exemplo: `mulheres` tem `"canal": "lives4"`, então o reel dela é entregue em
`~/projetos/yt-pub-lives4/imports/videos`.

**Essa entrega é a última etapa do pipeline** — ela acontece dentro da fase
`reel`, não numa fase separada de "publicação". Não existe fase `publicar` no
`flow.json`: quem diz o destino é o `canal` de cada público.

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
        │      (é AQUI que se troca a capa: `capa: A#<N> <publico>` + a foto)
        │      /aprovar A#<N>
        ▼
  2.5 baixar   acha o vídeo pelo título e baixa (janela de 90 min)
        │
        ⏸️  PARA — segundo portão: você confere os avatares baixados
        │      antes de gastar fila de render
        ▼
  3. reel      monta o reel 9:16 e ENTREGA no canal do público
        │
        ▼
  ✅ link do vídeo final no chat
```

## As fases e os portões

São **4 fases lógicas e 2 portões**. Os portões são o `"pausa_apos": true` das
fases `texto` e `baixar` no `flow.json` — o pipeline para sozinho ali e só anda
quando você libera.

| nº | fase | `id` no `flow.json` | fila | quem faz | portão depois? |
|---|---|---|---|---|---|
| 1 | texto | `texto` | `texto` | agente (opus) | ✅ `/aprovar A#N` |
| 2 | avatar | *5 rotas, abaixo* | — | **normalmente você** | — |
| 2.5 | baixar | `baixar` | `io` | função `heygen.baixar` | ✅ você confere |
| 3 | reel | `reel` | `render` | função `reel.montar` | fim (entrega no canal) |

A `baixar` é meio-fase de propósito: não cria nada, só traz pro disco o que já
existe no estúdio.

Aprovar antes vale mais que retentar depois — render de avatar e fila de reel
custam caro e não se desfazem. Os dois portões existem para isso: o primeiro
protege o gasto de avatar, o segundo protege o gasto de render.

### A fase 2 tem 5 rotas

Só uma roda por fluxo. As quatro automáticas são fases com a chave `opcional` no
`flow.json`; a quinta é a ausência de todas elas.

| rota | `id` / flag `opcional` | quem gera o avatar |
|---|---|---|
| **manual** *(padrão do promoavatar)* | *nenhuma* | **você**, sem o bot |
| estúdio | `estudio` (`opcional: estudio`) | o bot abre, você conclui |
| API | `gerar` (`opcional: api`) | o bot, via API HeyGen |
| créditos | `gerar-creditos` (`opcional: creditos`) | o bot, consumindo créditos |
| navegador | `navega-avatar` (`opcional: navega`) | agente LLM clonando o `TEMPLATE-AVATAR` |

Duas dessas flags estão documentadas no chat: **`| api`** (ver a seção
"OS AVATARES: SUA MÃO OU A API" do `HELP.md`) e **`| estudio`**. As de
`creditos` e `navega` existem como fase no `flow.json`, mas **não estão no
`HELP.md`** — o nome da flag no chat vem do campo `opcional`, então confirme
antes de usar.

A rota `navega-avatar` é a mais cara: **~17,8k tokens por público**, ou ~214k no
fluxo de 12 (`docs/pipeline.md`).

**O que amarra as 5 rotas é o título.** Em qualquer uma delas o vídeo tem que se
chamar `A<N>-<publico>-v1`. Na rota manual isso é 100% responsabilidade sua — é
o único contrato entre você e o pipeline.

## Trocar a imagem de capa por uma sua

As imagens do reel são decididas na fase de texto (seção `## IMAGENS`, regra
11b) e geradas pelo flux. Para pôr uma arte **sua** no lugar, mande a **foto no
chat com esta legenda** — a legenda da imagem, não uma mensagem separada:

| legenda | efeito |
|---|---|
| `capa: A#25 jovens` | IMAGEM 1 (a capa do feed) desse público |
| `capa: A#25 *` | a mesma imagem em **todos** os públicos do fluxo |
| `capa: A#25 jovens 3` | troca a IMAGEM 3, não a capa |
| `capa: A#25 jovens cover` | preenche **cortando** as laterais |

O bot escreve a linha `arquivo: <caminho>` na imagem certa do
`textos/A<N>/<publico>.md`, e o `preparar.py` passa a usar a sua foto em vez de
gerar uma.

**O padrão é `contain`:** a imagem cabe INTEIRA e o resto da faixa é preenchido
com uma cópia borrada dela mesma. Imagem enviada por você **nunca é cortada sem
você pedir** — a gerada nasce no tamanho exato, então cortar não tira nada; a
sua já vem composta, e se traz texto ou um rosto enquadrado, cortar destrói o
trabalho. `cover` é para imagem de fundo, sem texto.

### Quando mandar: no portão da fase de texto

É a única janela em que trocar a capa é **de graça** — nenhum avatar gerado,
nenhuma imagem paga no flux, nenhum render. Depois que o reel monta, o comando
ainda escreve no roteiro, mas o vídeo só muda com `/refazer` — e o bot avisa
isso na resposta.

Sem foto anexada ele recusa em vez de gravar uma linha vazia. Se você já tem o
arquivo no disco, dá para digitar o caminho:

```
capa: A#25 jovens | arquivo=/caminho/da/imagem.png
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

**A legenda do avatar é decidida no estúdio.** O que a API do HeyGen oferece
(`video_status.get`):

| campo | o que é | usamos? |
|---|---|---|
| `video_url` | MP4 **sem** legenda queimada | sim, quando não há versão legendada |
| `video_url_caption` | MP4 **com** legenda queimada | **sim, quando vem preenchido** |
| `caption_url` | legenda solta (arquivo), quando existe | não |

O download do bot prefere o `video_url_caption` e cai no `video_url` quando ele
não vem (`escolherUrl`, `inemaccbot/src/fila/tarefas/heygen.ts`). Ou seja:
gravou com legenda no estúdio, o reel sai com ela; gravou sem, sai sem.

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
isso. O teste custa um vídeo: renderize um com legenda ligada e olhe os dois
campos.

Consequências práticas de gravar com legenda queimada:

- ela vem posicionada para o enquadramento 16:9, não para a faixa do meio do
  9:16 — pode ser cortada ou colidir com a base;
- com a opção `legenda` ligada, saem **duas** legendas. **Ligar uma é decidir
  desligar a outra**: legenda no estúdio → reel sem `| legenda`; reel com
  `| legenda` → estúdio sem legenda.

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

## O que NÃO é deste repo (é do inemaccbot)

Este repo é **domínio**: ele *declara* o pipeline. Quem **executa** é o
`inemaccbot`. Procurar aqui algo que é de lá é a perda de tempo mais comum, então
segue a lista do que **não** está neste repo:

| o quê | onde vive de verdade |
|---|---|
| os comandos do chat (`/promoavatar`, `/status`, `/aprovar`, `/refazer`, `/cancelar`) e o parser de `\|` e `--` | o bot. Aqui só existe o `HELP.md`, que é o **texto** da ajuda, não o código dela |
| o motor de fases: filas, tentativas, timeouts, o congelamento na criação, o próprio conceito de portão | `inemaccbot/config/skills.json`. O `flow.json` só declara; quem obedece é o bot |
| as tarefas `heygen.gerar`, `heygen.estudio`, `heygen.baixar` — e o `escolherUrl`, que decide entre o MP4 legendado e o limpo | `inemaccbot/src/fila/tarefas/heygen.ts` |
| o estado dos fluxos e os avatares baixados (`state/artefatos/fluxos/A<N>/`) | o repo do bot |
| as pastas de canal `~/projetos/yt-pub-<canal>/imports/videos` | regra derivada pelo bot; aqui só existe o **nome** do canal |
| **como o reel é MONTADO** (cores, fontes, posições, corte de silêncio, SFX) | a skill global `~/.claude/skills/reel-edita-inema/SKILL.md` — mexer ali muda TODO reel da marca |
| o prompt que o agente recebe antes de chamar a skill do reel | `inemaccbot/prompts/reel.md` |

**Regra de bolso:** se a mudança afeta *todos* os fluxos, não é daqui. Se afeta
só o promoavatar, é daqui.

A exceção são os `scripts/*.py` — eles moram aqui e são o motor do reel deste
domínio, chamáveis direto na mão (ver "Parâmetros").

## Onde defino o prompt, e onde defino os públicos

São dois arquivos diferentes, e a confusão entre eles é comum:

| quero mudar… | arquivo |
|---|---|
| **como se escreve** (tom, regras, ganchos, imagens) | `prompts/fase1-texto.md` |
| **a dor / o ângulo de um público** | `flow.json` → `alvos.<publico>.gatilho` |
| **para qual canal vai** | `flow.json` → `alvos.<publico>.canal` |
| **o formato do arquivo de saída** (FALA / SOBREPOSIÇÕES / IMAGENS / ESTRUTURA) | a skill `inemaclub-textos` |

O `prompts/fase1-texto.md` manda usar a skill `inemaclub-textos` (linha 1), mas
**sobrescreve** a fórmula dela: "REGRAS DE ESCRITA (valem acima da fórmula
padrão da skill)". Ou seja, a skill dá a estrutura; o prompt do fluxo dá as
regras.

Os 12 públicos são as chaves de `alvos` no `flow.json`:

```
pessoacomum · jovens · profissionais · mulheres · empreendedores · tecnicos
40mais · 60mais · educadores · criadores · recolocacao · familia
```

Adicionar um público = mais uma entrada com `canal` e `gatilho`. A chave vira o
`<publico>` do título `A<N>-<publico>-v1`, então **nada de acento, espaço ou
hífen**.

## Os templates do reel

Ficam em `templates/` (apontado por `"templates_dir": "templates"` no
`flow.json`). São 4 layouts, todos 1080×1920, fundo `#0E1116` e acento âmbar
`#F5A623`:

| template | topo | meio | base | para que serve |
|---|---|---|---|---|
| **`empilhado-capa`** *(padrão da raiz)* | imagem 704px + `headline` | avatar 608px (áudio) | painel de texto 608px (`hook`) | capa de impacto — o formato original |
| **`empilhado-explicativo`** | imagem 704px + `headline` | avatar 608px (áudio) | vídeo explicativo 608px, mudo em loop | quando existe explicativo em vídeo |
| **`diptico`** | imagem 960px + `headline` | avatar 960px | **não tem** | mito×realidade e comparação — a imagem carrega o contraste |
| **`imagem-plena`** | imagem ocupa os 1920px | avatar em recorte no **topo-direita** | — | pergunta incômoda, previsão, consequência inesperada |

No `imagem-plena` o avatar vai no topo-direita por regra de produção, não por
estética: **o rodapé é proibido** — em produção a interface da rede (legenda, @,
botões) cobre o canto inferior e o avatar simplesmente não apareceria.

Cada faixa declara uma `fonte`: `imagens`, `avatar`, `texto` ou `explicativo`. É
daí que vem a exigência da regra 11b do prompt de texto — a `headline` vai na
faixa de topo, o `hook` vai no painel de base. **Layout com base e `hook`
faltando = base preta**: foi o que aconteceu no A#23 (`hook` em 0 de 8 imagens).
Por isso o prompt manda escrever `hook` sempre, mesmo nos layouts que não têm
base (`diptico` e `imagem-plena`).

### Ninguém escolhe layout na hora do render

O layout decorre da linha `Formato escolhido:` que a fase de texto grava em cada
`<publico>.md` (o PASSO ZERO do prompt) — ou seja, de uma decisão editorial que
**você já aprovou no portão**. O `templates/mapa.json` faz a tradução:

```
"mito versus realidade" → diptico        "pergunta incômoda" → imagem-plena
"comparação"            → diptico        ...
```

**Precedência** (resolvida pelo `preparar.py`):

```
--template explícito  ›  template do ALVO no flow.json  ›  mapa.json  ›  template da raiz
```

Formato que não estiver no mapa cai no padrão — não inventa. No A#19 real a fase
de texto escolheu **9 formatos diferentes para 12 públicos**, então isso produz
variação de verdade sem ninguém decidir nada em tempo de render.

## Parâmetros

### No chat (o que o `HELP.md` documenta)

| opção | efeito |
|---|---|
| `--alvo=jovens` (repetível) ou `\| alvos=a,b` | só esses públicos |
| `\| sombra` | mostra o plano, não enfileira |
| `\| legenda` | legenda palavra-a-palavra (padrão: sem) |
| `\| versao=N` | muda o `-vN` do título |
| `\| de=baixar` | começa no meio (texto e avatar já feitos) |
| `\| api` | o BOT gera o avatar (~US$ 1/min da carteira pré-paga) |
| `\| api \| sem-portao` | gera E não para para aprovar |
| `/status A#N` · `/aprovar A#N` · `/refazer A#N <publico>` · `/cancelar A#N` | acompanhar |

### Nos motores do reel (`scripts/`)

`montar-reel.py` — a fase 3 ponta a ponta:

| flag | |
|---|---|
| `--avatar` | **obrigatório** — o MP4 do HeyGen |
| `--ws` | **obrigatório** — workspace do reel |
| `--alvo` | público; vira o `seed-key` das imagens (default `reel`) |
| `--textos` | o `<publico>.md` — é de onde sai a seção `## IMAGENS` |
| `--template` | override de layout (vence tudo) |
| `--flow` / `--mapa` | de onde resolver template e mapa |
| `--qualidade` | `high` (default) · `standard` · `draft` |
| `--cta` / `--sem-cta` | o clipe de fecho (`cta/cta-9x16.mp4`) |
| `--pular-preparo` | reaproveita o preparo já feito no `--ws` |
| `--saida` | destino do MP4 |

`preparar.py` — só a preparação (imagens + transcrição). Tem as mesmas flags,
mais `--explicativo`, `--sem-imagens`, `--sem-transcricao` e `--sem-montar`.

### Exemplos

```bash
# reel padrão de um público — layout sai do mapa
python3 scripts/montar-reel.py \
  --avatar state/artefatos/fluxos/A34/A34-jovens-v1.mp4 \
  --ws /tmp/ws-A34-jovens --alvo jovens \
  --textos textos/A34/jovens.md --flow flow.json

# rascunho barato, só para conferir enquadramento
python3 scripts/montar-reel.py ... --qualidade draft --sem-cta

# forçar um layout, ignorando o mapa
python3 scripts/montar-reel.py ... --template imagem-plena

# trocar template/CTA sem regerar as imagens
python3 scripts/montar-reel.py ... --pular-preparo --saida saida/A34-jovens.mp4

# com vídeo explicativo na faixa de base
python3 scripts/preparar.py ... --alvo tecnicos \
  --explicativo saida/explicativo-tecnicos.mp4 --template empilhado-explicativo

# só preparar agora, montar depois
python3 scripts/preparar.py ... --sem-montar
```

Fixar o layout de um público direto no `flow.json` (vence o mapa, perde para
`--template`):

```json
"empreendedores": {
  "canal": "lives1",
  "gatilho": "Transforme IA em redução de custos...",
  "template": "diptico"
}
```

## Atenção: tudo aqui é congelado na criação

O `flow.json`, os prompts e as opções (`legenda`, `cta`) são **congelados quando
o fluxo nasce**. Editar vale para os PRÓXIMOS — um fluxo em andamento não muda
de regra no meio do caminho, e por isso nem `/refazer` pega a mudança.
