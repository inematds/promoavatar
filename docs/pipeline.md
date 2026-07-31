# O pipeline inteiro, etapa por etapa

O que roda em cada ponto, quem executa, e quanto custa. Números medidos no A#4
(1 público, 2026-07-31) — ver `inemaccbot/docs/amostra-a4-custo-e-tempo.md`.

## Tabela mestre

| # | etapa | onde roda | fila (simultâneos) | tipo | o que usa | tokens (saída) | tempo |
|---|---|---|---|---|---|---|---|
| 0 | comando no chat | gateway | — | **código** | parser de verbo e campos | 0 | ms |
| 1 | criação do fluxo | gateway | — | **código** | lê e CONGELA o `flow.json` | 0 | ms |
| 2 | fase `texto` | agente | `texto` (2) | **LLM** | Claude sonnet/low + skill `inemaclub-textos` | **16.525** | **2min45** |
| 3 | ⏸️ portão | **pessoa** | — | **humano + IA externa** | HeyGen (avatar) | 0 | você |
| 4 | fase `baixar` | worker | `io` (10) | **sem IA** | API do HeyGen, casa por título exato | 0 | **~3s** |
| 5 | fase `reel` | agente | `render` (**1**) | **LLM + IA + determinístico** | ver detalhe abaixo | **73.372** | **21min34** |
| 6 | entrega | gateway | — | **código** | copia para `yt-pub-<canal>/imports/videos/` | 0 | ms |
| 7 | aviso no chat | gateway | — | **código** | link + `✅ terminou` | 0 | ms |
| 8 | publicação | worker do canal | — | **fora do bot** | `scheduler.py` / `import_worker.py` → YouTube | 0 | agendado |

**Total por público:** ~90 mil tokens de saída, ~24 min de relógio.
Só as etapas **2** e **5** gastam modelo.

## Dentro da etapa 5 (onde está o custo)

| parte | natureza | ferramenta |
|---|---|---|
| headline-choque a partir do gatilho do público | **LLM** | Claude sonnet/low |
| segmentação, timing, escolha de SFX, composição | **LLM** | idem |
| transcrição do avatar (corte de silêncio, legenda palavra-a-palavra) | **IA, não LLM** | Whisper via **Groq** |
| imagens da capa | **IA, não LLM** | **flux2-klein** (inemaimg, `localhost:8000`) |
| HTML → frames → MP4 | **sem IA** | Hyperframes / Remotion |
| corte, mixagem, ducking, encode | **sem IA** | FFmpeg |

Repartição de tempo medida: **96% agente, 4% render** (50,8 s de 21min34).
Mexer em qualidade ou resolução mexe nos 4%.

## Como escala

| | 1 público | 12 públicos |
|---|---|---|
| fase `texto` | 1 job | **1 job** (escopo `fluxo`) |
| fase `baixar` | 1 job | 12 jobs (paralelos, fila `io` = 10) |
| fase `reel` | 1 job | 12 jobs **em sequência** (fila `render` = 1) |
| avatares a gravar à mão | 1 | **12** |
| tempo total | ~25 min | **~1h05** (medido no A#8) |

A fase de reel é a única que multiplica por público E é serializada. Num fluxo
de 12, ela é praticamente o custo inteiro — em token e em relógio.

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
