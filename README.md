# promoavatar

Repo de **domínio** do fluxo `/promoavatar` do inemaccbot: reels de divulgação
para 12 públicos, com portão humano no meio.

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
| `docs/` | as decisões e o que ainda está aberto |

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

## Ajustes mais comuns

| quero… | mexo em |
|---|---|
| trocar o canal de um público | `flow.json` → `alvos.<publico>.canal` |
| mudar o gancho de um público | `flow.json` → `alvos.<publico>.gatilho` |
| mudar como os roteiros são escritos | `prompts/fase1-texto.md` |
| mudar como o reel é montado | `flow.json` → fase `reel`, campo `entrega` |
| mudar a ajuda do chat | `HELP.md` |

**Atenção:** o `flow.json` e os prompts são **congelados na criação de cada
fluxo**. Editar aqui vale para os PRÓXIMOS — um fluxo em andamento não muda de
regra no meio do caminho, e por isso `/refazer` também não pega a mudança.
