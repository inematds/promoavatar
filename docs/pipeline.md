# O pipeline inteiro, etapa por etapa

O que roda em cada ponto, quem executa, e quanto custa. Números refeitos em
**2026-08-05** sobre 48 reels (A#25 a A#28) — ver
`inemaccbot/docs/amostra-a23-a24-fase-reel.md`. A medição original é do A#4
(1 público, 2026-07-31, `amostra-a4-custo-e-tempo.md`) e ficou obsoleta quando a
fase reel deixou de escrever HTML à mão.

## Tabela mestre

| # | etapa | onde roda | fila (simultâneos) | tipo | o que usa | tokens (saída) | tempo |
|---|---|---|---|---|---|---|---|
| 0 | comando no chat | gateway | — | **código** | parser de verbo e campos | 0 | ms |
| 1 | criação do fluxo | gateway | — | **código** | lê e CONGELA o `flow.json` | 0 | ms |
| 2 | fase `texto` | agente | `texto` (2) | **LLM** | Claude sonnet/low + skill `inemaclub-textos` | **16.525** | **2min45** |
| 3 | ⏸️ portão | **pessoa** | — | **humano + IA externa** | HeyGen (avatar) | 0 | você |
| 3b | fase `navega-avatar` | agente | `navegador` | **LLM** | Claude no navegador, clona `TEMPLATE-AVATAR` | **17.800** | **5min48** |
| 4 | fase `baixar` | worker | `io` (10) | **sem IA** | API do HeyGen, casa por título exato | 0 | **~61 min de FILA** |
| 5 | fase `reel` | agente | `render` (**1**) | **LLM + IA + determinístico** | ver detalhe abaixo | **6.700** | **3min54** |
| 6 | entrega | gateway | — | **código** | copia para `yt-pub-<canal>/imports/videos/` | 0 | ms |
| 7 | aviso no chat | gateway | — | **código** | link + `✅ terminou` | 0 | ms |
| 8 | publicação | worker do canal | — | **fora do bot** | `scheduler.py` / `import_worker.py` → YouTube | 0 | agendado |

**Total por público:** ~28 mil tokens de saída (`navega` 17,8k + `reel` 6,7k +
a fatia do `texto`, que é ~3,5k porque ele é UM job para os 12).
Gastam modelo as etapas **2**, **3b** e **5**.

> **Números refeitos em 2026-08-05**, sobre 48 reels (A#25 a A#28), depois de a
> fase `reel` passar a usar `montar-reel.py` pela skill do projeto. Os valores
> anteriores (73.372 tokens e 21min34 no reel) são de quando o agente escrevia o
> HTML à mão. Método: `inemaccbot/docs/amostra-a23-a24-fase-reel.md` — continua
> sendo arqueologia de log, não instrumentação.

### A fase reel deixou de ser a maior — a NAVEGAÇÃO é

| fase | mediana por público | × jobs | soma num fluxo de 12 |
|---|---|---|---|
| `texto` | 41,8k (o fluxo inteiro) | **1** | 42k |
| `navega-avatar` | **17,8k** | 12 | **214k** |
| `reel` | 6,7k | 12 | 80k |

Este documento dizia que o reel era 64% do gasto. Não é mais: hoje ele é a
**menor** das três fases com modelo, e a navegação do HeyGen é ~2,5× ele. O
tempo diz o mesmo — `navega` 5min48 contra `reel` 3min54.

**Onde otimizar agora, se for pelo custo:** a navegação. Buscar o template,
clonar, renomear, colar o texto e clicar Generate são passos FIXOS, e cada um é
hoje uma ida ao modelo com o contexto inteiro. O caminho já está anotado em
`inemaccbot/docs/rota-navega-avatar.md`: trocar o agente por Playwright nos
passos mecânicos.

**Uma ressalva honesta sobre o número do reel:** dois casamentos de log
discordam — 6,7k por janela de tempo e 15,3k por título do avatar. Os dois
concordam na ORDEM (`navega` > `reel`) e na ordem de grandeza; a precisão do
valor exato não está estabelecida.

**O `baixar` não é custo:** os ~61 min de média são **fila do HeyGen** (ver a
seção abaixo), não processamento nosso.

## Dentro da etapa 5

| parte | natureza | ferramenta |
|---|---|---|
| ler o mosaico do QC e decidir se refaz | **LLM** | Claude sonnet/low |
| reagir a `exit != 0` de algum portão | **LLM** | idem |
| headline, hook, segmentação e tempos | **nada** — vêm da fase 1 e do transcript | `preparar.py` |
| escolha do layout | **nada** — decorre do formato editorial | `templates/mapa.json` |
| transcrição do avatar (corte de silêncio, legenda palavra-a-palavra) | **IA, não LLM** | Whisper via **Groq** |
| imagens da capa | **IA, não LLM** | **flux2-klein** (inemaimg, `localhost:8000`) |
| HTML → frames → MP4 | **sem IA** | Hyperframes / Remotion |
| corte, mixagem, ducking, encode | **sem IA** | FFmpeg |

SFX saíram da receita e a legenda é SEM por padrão — ver `decisoes-reel.md`.

A repartição antiga (**96% agente, 4% render**) valia quando a fase levava
21min34. Hoje ela leva 3min54 e o render é a maior parte dela: o que sumiu foi
justamente o tempo de agente.

## O tempo do HeyGen é fila, não custo (medido no A#23, 2026-08-04)

O render de um avatar de **36s levou ~65 minutos** entre `pending`,
`processing` e `completed`, com só 2 vídeos na fila. **Isso é a fila do plano da
conta, não um gargalo do pipeline** — decisão do dono: *faz parte, não é custo*.
Não medir contra isso, não tentar otimizar, não confundir com job travado.

O que o log mostra durante essa espera é o comportamento CERTO:

```
[job 361] ainda não: "A23-jovens-v1" está pending — nova checagem em 120s
[job 361] ainda não: "A23-jovens-v1" está processing — nova checagem em 120s
```

O que **é** consequência real disto, e vale vigiar: `espera.timeout` da fase
`baixar` é **5400s (90 min)** por job. Com fila lenta e muitos públicos na mesma
conta, um vídeo pode passar de 90 min esperando e o job cai por timeout **mesmo
com o avatar ficando pronto depois**. O avatar não se perde (fica `completed` no
HeyGen); o conserto é `/refazer` daquele público, e aí o `baixar` acha na hora,
por título exato.

Lembre que `espera.timeout` é **congelado por fluxo**: mudá-lo no `flow.json`
não alcança fluxo já criado.

## Como escala

| | 1 público | 12 públicos |
|---|---|---|
| fase `texto` | 1 job | **1 job** (escopo `fluxo`) |
| fase `baixar` | 1 job | 12 jobs (paralelos, fila `io` = 10) |
| fase `reel` | 1 job | 12 jobs **em sequência** (fila `render` = 1) |
| avatares a gravar à mão | 1 | **12** |
| tempo total | ~25 min | **~1h05** (medido no A#8) |

A fase de reel é a única que multiplica por público E é serializada — mas
deixou de ser o custo. Num fluxo de 12 ela soma ~80k de saída contra ~214k da
`navega-avatar`, que multiplica igual e roda na fila `navegador`.

## Quem decide o quê

| decisão | quem | onde |
|---|---|---|
| públicos, canal e gatilho de cada um | domínio | `flow.json` deste repo |
| como o roteiro é escrito | domínio | `prompts/fase1-texto.md` |
| como o reel é montado | domínio | `flow.json`, campo `entrega` da fase `reel` |
| onde o canal fica no disco | bot | derivado: `~/projetos/yt-pub-<canal>/imports/videos` |
| motor, modelo e esforço | bot | `config/skills.json` + perfil padrão |
| quantos jobs simultâneos por fila | bot | `src/fila/filas.ts` |

## Contratos que não podem quebrar

| contrato | onde | o que acontece se quebrar |
|---|---|---|
| título `A<N>-<publico>-v1` | `tituloEstudio()` = nome no HeyGen | download não acha, fase expira em 90 min |
| última linha `RESULT:` ou `ERRO:` | saída de todo agente | job falha (e é o certo) |
| `{{pasta}}` absoluto | prompt da fase 1 | agente escolhe repo/slug sozinho |
| um público = um vídeo | roteiro com UMA fala | vídeo a mais sem título para casar |

## O que NÃO está confirmado

A etapa **8** nunca foi observada funcionando: há lotes de 22 a 25 de julho
parados em `lives2`, `lives3` e `lives4`, e nenhum processo `import_worker.py`
aparece rodando. Os reels entregues podem estar esperando um gatilho que não
acontece.
