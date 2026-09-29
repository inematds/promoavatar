# promoavatar

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

**Domain** repo for the `/promoavatar` flow in inemaccbot: promotional reels
for 12 audiences, with a human gate in the middle.

> ## Unfrozen on 2026-08-09
>
> Between 2026-08-06 and 2026-08-09, this repo was **frozen** (“untouchable”), and
> all work went to [`promoavatar3`](https://github.com/inematds/promoavatar3).
> The owner gave the green light: **both are evolving again**.
>
> This does **not** make them one system. They remain separate systems—each with
> its own reel engine (`scripts/`), layouts (`templates/`), targets, and prompt.
> Changes here do not affect the other repo, and vice versa. Their purpose
> remains different: here, **one video per audience** (12 audiences); there,
> **three** (reach, authority, promotional).
>
> **One thing exists only here:** the `| navega` route—the agent piloting the
> studio, which is the fallback if HeyGen’s DOM changes and the `| estudio`
> script breaks. promoavatar3 does not have this plan B.
>
> **Cost of the three-day divergence:** during the freeze, this repo received
> only the minimum needed to avoid breaking outside this machine—versioned CTA
> (`3e0da37`), paths as environment variables (`4f10c84`), and the image
> adapter. What **didn’t** come along was everything new promoavatar3 gained
> during that period. Porting it over case by case is your decision, not an
> automatic process.

## 📖 User guide

Complete guide (landing page + step-by-step instructions):
**https://inematds.github.io/promoavatar/guia/en/**

The bot writes the scripts and STOPS. You record the avatars in HeyGen; when
you’re done, you release them and it downloads them, assembles the reels, and
delivers them to each channel.

There is no **TypeScript** here—the pipeline definition (`flow.json`, prompts)
is the heart of the repo, and a new flow is an entry in the bot’s registry plus
a repo like this one. But there is Python code in `scripts/` (8 files): it’s the
reel engine, which runs as a function triggered by the `reel.montar` phase.

## What’s here

| file | what it is |
|---|---|
| `flow.json` | the phases, the 12 audiences, each audience’s channel and trigger |
| `prompts/fase1-texto.md` | what the agent receives to write the scripts |
| `templates/*.json` | the 4 reel layouts in 9:16 + the `mapa.json` format→layout mapping |
| `scripts/*.py` | the reel engines (`preparar.py`, `montar-reel.py`) |
| `HELP.md` | the help text shown in chat for `/promoavatar help` |
| `textos/A<N>/` | the generated scripts, one file per audience |
| `docs/pipeline.md` | **the full table**: steps, LLM/AI/worker, cost, and time |
| `docs/canais-e-destinos.md` | who each reel is for and where it goes |
| `docs/` | other decisions and what’s still open |

## Who it’s for, and where it goes

This question causes the most confusion, so here’s the summary—the details are
in [`docs/canais-e-destinos.md`](docs/canais-e-destinos.md):

| question | who answers it | where to change it |
|---|---|---|
| **who** the reel is for | this repo | `flow.json`, the audience’s `canal` field |
| **where** the channel lives on disk | the bot | derived: `~/projetos/yt-pub-<canal>/imports/videos` |

Example: `mulheres` has `"canal": "lives4"`, so its reel is delivered to
`~/projetos/yt-pub-lives4/imports/videos`.

**This delivery is the last step in the pipeline**—it happens inside the
`reel` phase, not in a separate “publish” phase. There is no `publicar` phase in
`flow.json`: the `canal` for each audience determines the destination.

The path **isn’t written anywhere**—it’s always
`~/projetos/yt-pub-<canal>/imports/videos`. So:

- **changing an audience’s channel** = edit `flow.json` (applies to the next flow);
- **creating a new channel** = `mkdir -p ~/projetos/yt-pub-lives33/imports/videos`,
  without touching the bot.

## The cycle, at a glance

```
/promoavatar <assunto> [--alvo=mulheres]
        │
        ▼
  1. texto     ONE script per audience, saved in textos/A<N>/<publico>.md
        │
        ⏸️  STOPS — chat sends you each script with the video TITLE
        │      you record it in HeyGen using that exact name
        │      (this is WHERE you change the cover: `capa: A#<N> <publico>` + the photo)
        │      /aprovar A#<N>
        ▼
  2.5 baixar   finds the video by title and downloads it (90-minute window)
        │
        ⏸️  STOPS — second gate: you review the downloaded avatars
        │      before spending a render queue slot
        ▼
  3. reel      assembles the 9:16 reel and DELIVERS it to the audience’s channel
        │
        ▼
  ✅ final video link in chat
```

## Phases and gates

There are **4 logical phases and 2 gates**. The gates are the `"pausa_apos": true`
settings on the `texto` and `baixar` phases in `flow.json`—the pipeline stops
there on its own and only continues when you release it.

| no. | phase | `id` in `flow.json` | queue | who does it | gate afterward? |
|---|---|---|---|---|---|
| 1 | texto | `texto` | `texto` | agent (opus) | ✅ `/aprovar A#N` |
| 2 | avatar | *5 routes, below* | — | **usually you** | — |
| 2.5 | baixar | `baixar` | `io` | `heygen.baixar` function | ✅ you review |
| 3 | reel | `reel` | `render` | `reel.montar` function | end (delivered to channel) |

`baixar` is intentionally a half-phase: it doesn’t create anything; it just
brings to disk what already exists in the studio.

Approving first is better than retrying later—avatar renders and the reel queue
are expensive and can’t be undone. That’s what the two gates are for: the first
protects the avatar expense, and the second protects the render expense.

### Phase 2 has 5 routes

Only one runs per flow. The four automatic routes are phases with the `opcional`
key in `flow.json`; the fifth is when none of them are present.

| route | `id` / `opcional` flag | who generates the avatar |
|---|---|---|
| **manual** *(promoavatar default)* | *none* | **you**, without the bot |
| studio | `estudio` (`opcional: estudio`) | bot opens it; you finish |
| API | `gerar` (`opcional: api`) | bot, via HeyGen API |
| credits | `gerar-creditos` (`opcional: creditos`) | bot, using credits |
| browser | `navega-avatar` (`opcional: navega`) | LLM agent cloning `TEMPLATE-AVATAR` |

Two of these flags are documented in chat: **`| api`** (see the “THE AVATARS:
YOUR HAND OR THE API” section in `HELP.md`) and **`| estudio`**. The
`creditos` and `navega` flags exist as phases in `flow.json`, but **aren’t in
`HELP.md`**—the flag name in chat comes from the `opcional` field, so confirm
before using them.

The `navega-avatar` route is the most expensive: **~17.8k tokens per audience**,
or ~214k for the 12-audience flow (`docs/pipeline.md`).

**The title ties all 5 routes together.** In any of them, the video must be
named `A<N>-<publico>-v1`. On the manual route, that’s entirely your
responsibility—it’s the only contract between you and the pipeline.

## Replace the cover image with one of your own

The reel images are decided in the text phase (section `## IMAGENS`, rule
11b) and generated by flux. To use **your own** image instead, send the **photo
in chat with this caption**—the image caption, not a separate message:

| caption | effect |
|---|---|
| `capa: A#25 jovens` | IMAGE 1 (the feed cover) for this audience |
| `capa: A#25 *` | the same image for **all** audiences in the flow |
| `capa: A#25 jovens 3` | replaces IMAGE 3, not the cover |
| `capa: A#25 jovens cover` | fills the frame by **cropping** the sides |

The bot writes the `arquivo: <caminho>` line under the right image in
`textos/A<N>/<publico>.md`, and `preparar.py` uses your photo instead of
generating one.

**The default is `contain`:** the whole image fits, and the rest of the frame is
filled with a blurred copy of the image. An image you send is **never cropped
unless you ask for it**—generated images start at the exact size, so cropping
doesn’t remove anything; yours is already composed, and if it has text or a
framed face, cropping destroys the work. `cover` is for background images
without text.

### When to send it: at the text-phase gate

This is the only window when changing the cover is **free**—no generated avatar,
no paid image from flux, no render. After the reel is assembled, the command
still updates the script, but the video changes only with `/refazer`—and the
bot tells you that in its response.

Without an attached photo, it refuses instead of writing an empty line. If you
already have the file on disk, you can type the path:

```
capa: A#25 jovens | arquivo=/caminho/da/imagem.png
```

## The title is the contract

In the studio, the video must be named **exactly**:

```
A<N>-<publico>-v1        ex.: A8-mulheres-v1
```

The download matches by exact string equality. A different name means the video
is never found, and the phase expires in 90 minutes. Chat sends you the ready
title with each script so you don’t have to type it from memory.

## Options when creating

| option | default | what it does |
|---|---|---|
| `--alvo=jovens` (repeatable) or `\| alvos=a,b` | all 12 | only these audiences |
| `\| legenda=nao` | **WITH captions** | turns off the reel’s word-by-word captions |
| `\| versao=N` | 1 | changes the studio title’s `-vN` |
| `\| de=<fase>` | — | starts partway through (you’ve already done text and/or avatar) |
| `\| sombra` | — | shows the plan without queueing anything |

```
/promoavatar <assunto> --alvo=jovens | legenda=nao
```

**The default was reversed (2026-08-07): captions are ON.** One word at a time,
uppercase, white, with the keyword in amber, at the bottom of the avatar band.
The design, decisions, and where to change the color and format are in
`docs/legenda.md`.

> **Attention—partial rollout.** The **engine** is ready and verified in this
> repo (`scripts/legendas.py`, layer in `montar.py`, node in the template,
> `--sem-legenda` in `preparar.py`/`montar-reel.py`). The bot **flag isn’t**:
> `| legenda=nao` only takes effect after the change in
> `inemaccbot/src/gateway/comandos-fluxo.ts` (`:282`, `:182-186`, `:336`) and
> a restart—which requires an empty queue. Until then, running from the command
> line includes captions; running through the bot doesn’t yet.

### Captions: what comes from HeyGen and what’s ours

This option controls **only the captions our editor draws**. It can’t see the
MP4 from HeyGen: if the avatar arrives with captions **burned into the pixels**,
they survive through the entire reel, even with the option turned off—there is
no removal, masking, or inpainting step in the pipeline.

**Avatar captions are decided in the studio.** What the HeyGen API offers
(`video_status.get`):

| field | what it is | do we use it? |
|---|---|---|
| `video_url` | MP4 **without** burned-in captions | yes, when there’s no captioned version |
| `video_url_caption` | MP4 **with** burned-in captions | **yes, when populated** |
| `caption_url` | standalone captions (file), when available | no |

The bot’s download prefers `video_url_caption` and falls back to `video_url`
when it isn’t available (`escolherUrl`, `inemaccbot/src/fila/tarefas/heygen.ts`).
In other words, record with captions in the studio and the reel includes them;
record without captions and it doesn’t.

**You can’t choose anything at download time.** Downloading is a `GET` to a
ready-made URL—there are no `?estilo=`, `?formato=`, `?idioma=` parameters.
Five caption endpoints were tested (`v1/video.caption`, `v2/video/caption`,
`v1/video.subtitle`, `v1/caption.list`, `v2/caption_styles`), and returned
**404**. The style, font, and position of burned-in captions are decided **in
the studio, before rendering**; after that, they’re in the pixels, and the only
way to change them is to record again.

**What was measured (2026-08-01, with the account’s real key):** the 25 most
recent complete videos—all had `video_url_caption` set to null and `caption_url`
empty.

**What was measured (2026-08-07, on `A35-tecnicos-v1`, `901cc529…`):** the
video **has** captions when downloaded through the UI, even though:

- `GET /v3/videos/{id}` returns **200** (the previous line said 404—it was the
  legacy `v2/video/{id}`, which still returns 404). The full response is `id`,
  `title`, `status`, `duration`, `created_at`, `completed_at`, `video_url`,
  `thumbnail_url`, `gif_url`, `video_page_url`. **There is no
  `captioned_video_url` or `subtitle_url`**—the fields described in the public
  docs weren’t returned;
- `v1/video_status.get` for the same video: `caption_url` is empty,
  `video_url_caption` is null.

In other words: **captions enabled in the studio don’t reach the API**, either
as a captioned MP4 or as a file. The captioned MP4 the UI downloads is an
on-demand render, inaccessible through the API. This rules out the earlier
hypothesis that `video_url_caption` would become populated.

**What is still NOT measured:** the behavior of a video created by
`POST /v3/videos` **with `caption`**—that’s a different path and may well return
the fields in the docs. It’s irrelevant here while phase 2 is human-operated:
the bot never calls create.

**Consequence for the pipeline:** captions can be removed from an already
rendered video only from the local file (ASR). See `docs/legenda.md`.

Practical consequences of recording with burned-in captions:

- they’re positioned for a 16:9 frame, not the middle band of 9:16—they may be
  cropped or overlap the bottom;
- with the `legenda` option on, you get **two** sets of captions. **Turning one
  on means deciding to turn the other off**: captions in the studio → reel
  without `| legenda`; reel with `| legenda` → studio without captions.

## Where to change what

The rule: **audience or campaign decisions belong in this repo; the brand’s
visual identity belongs in the skill.** The skill is global—changing it affects
EVERY reel, including those started directly in chat.

| I want to change… | file | layer |
|---|---|---|
| an audience’s channel | `flow.json` → `alvos.<publico>.canal` | domain |
| an audience’s hook | `flow.json` → `alvos.<publico>.gatilho` | domain |
| **how scripts are written** | `prompts/fase1-texto.md` | domain |
| **what this flow asks the reel to do** | `prompts/reel-regras.md` + `templates/*.json` | domain |
| **the closing CTA clip** | `cta/cta-9x16.mp4`—replace the file | domain |
| chat help | `HELP.md` | domain |
| **how the reel is ASSEMBLED** (colors, fonts, positions, SFX, modes) | `~/.claude/skills/reel-edita-inema/SKILL.md` | skill (global) |
| what the agent receives before calling the skill | `inemaccbot/prompts/reel.md` | bot |
| queues, timeouts, model, and effort | `inemaccbot/config/skills.json` | bot |

### The text prompt (`prompts/fase1-texto.md`)

This is where the following live, in this order:

1. **FIXED CONTEXT**—what the agent already knows (Nei and Tiza manage the
   community), so it doesn’t mention a name without a role or make up who they
   are.
2. **DON’T TOUCH THE MACHINE**—prohibits installing anything. A render installed
   the wrong binary after following a log hint and broke the next render.
3. **STEP ZERO**—central thesis, demonstrable element, and explicit choice of
   one format from 11. Without a choice, the agent always falls into
   problem→solution→CTA, an ad template, and ads aren’t shared.
4. **HOOK WORKSHOP**—five opening lines per audience, with four rejected IN
   WRITING. The criterion is the gap test: after the line, does the person need
   the next one to complete the thought? If the line stands on its own, it’s a
   statement, not a hook. Limit: 9 words.
5. **WRITING RULES**—the 16 rules: hook in the first 2 seconds, problem before
   solution, name the profession, benefit before mechanics, short sentences,
   appropriately sized promise, imperative CTA, no placeholders, no invented
   urgency, OVERLAYS as a VISUAL script with the four triggers (attention ·
   retention · engagement · CTA), the gap in the SPOKEN LINES, complete value
   before the brand, the final sentence deciding whether it gets shared, and
   write for ONE specific person.
6. **The output contract**—`{{pasta}}`, `RESULT:`/`ERRO:`.

Variables injected by the bot: `{{input}}` (the topic), `{{publicos}}` (the
flow’s ACTUAL targets), `{{pasta}}` (where to save the file, absolute path),
`{{ref}}`, `{{saida}}`.

#### For DEBATE topics, the prompt takes a position

A topic that arrives as an open question (“is this good or bad?”, “what do you
think?”) had a predictable result: the agent explained both sides and ended
with “the important thing is to be prepared.” Correct but bland—nobody comments
on a fence-sitter, and the video gets watched and forgotten.

The cause wasn’t a lack of talent: rules 9 and 10 (don’t invent data, don’t
invent urgency) make the agent retreat to the middle ground, the only place
where it’s certain it isn’t asserting anything.

So the prompt now says to **take a side** in this case and **write in the
summary which position it took and why**. This doesn’t loosen rules 9 and 10:
opinions are allowed; invented facts aren’t.

**The position you give it takes precedence.** If you write yours in the topic,
it uses yours; the block exists only for when you haven’t. Writing your own
position is still the best approach—along with a concrete fact (so the PROOF
line isn’t empty) and the question you want people to answer in the comments.

Because the summary states the chosen position, you can disagree with it **at
the gate**, before generating any avatars—`/refazer` costs a text, not a render.

### Reel style—two layers

What THIS pipeline asks of the reel lives in `prompts/reel-regras.md` and
`templates/*.json`: the four triggers, the headline based on the audience’s
`{gatilho}`, and each layout’s bands.

The `reel-edita-inema` skill knows how to assemble it: stacked 9:16
composition, colors, fonts, silence trimming, word-by-word captions, SFX.
Changing that changes the entire brand.

**Improve the reel in order, from least expensive:** replace the clip in
`cta/`; adjust `prompts/reel-regras.md` or `templates/*.json`; only then change
the skill.

## What is NOT in this repo (it’s in inemaccbot)

This repo is the **domain**: it *declares* the pipeline. `inemaccbot` is what
**runs** it. Looking here for something that belongs there is the most common
waste of time, so here’s what is **not** in this repo:

| what | where it actually lives |
|---|---|
| chat commands (`/promoavatar`, `/status`, `/aprovar`, `/refazer`, `/cancelar`) and the `\|` and `--` parser | the bot. Only the `HELP.md` is here—the **help text**, not its code |
| phase engine: queues, retries, timeouts, freezing at creation, the concept of a gate itself | `inemaccbot/config/skills.json`. `flow.json` only declares it; the bot follows it |
| the `heygen.gerar`, `heygen.estudio`, `heygen.baixar` tasks—and `escolherUrl`, which decides between the captioned and clean MP4 | `inemaccbot/src/fila/tarefas/heygen.ts` |
| flow state and downloaded avatars (`state/artefatos/fluxos/A<N>/`) | the bot repo |
| channel folders `~/projetos/yt-pub-<canal>/imports/videos` | a rule derived by the bot; only the **channel name** is here |
| **how the reel is ASSEMBLED** (colors, fonts, positions, silence trimming, SFX) | the global skill `~/.claude/skills/reel-edita-inema/SKILL.md`—changing it affects EVERY reel for the brand |
| the prompt the agent receives before calling the reel skill | `inemaccbot/prompts/reel.md` |

**Rule of thumb:** if a change affects *all* flows, it doesn’t belong here. If it
affects only promoavatar, it does.

The exception is `scripts/*.py`—they live here and are the reel engine for this
domain, callable directly by hand (see “Parameters”).

## Where to define the prompt and where to define audiences

These are two different files, and confusing them is common:

| I want to change… | file |
|---|---|
| **how it’s written** (tone, rules, hooks, images) | `prompts/fase1-texto.md` |
| **an audience’s problem/angle** | `flow.json` → `alvos.<publico>.gatilho` |
| **which channel it goes to** | `flow.json` → `alvos.<publico>.canal` |
| **the output file format** (SPOKEN LINES / OVERLAYS / IMAGES / STRUCTURE) | the `inemaclub-textos` skill |

`prompts/fase1-texto.md` tells the agent to use the `inemaclub-textos` skill
(line 1), but **overrides** its formula: “WRITING RULES (take precedence over
the skill’s default formula).” In other words, the skill provides the structure;
the flow prompt provides the rules.

The 12 audiences are the keys in `alvos` in `flow.json`:

```
pessoacomum · jovens · profissionais · mulheres · empreendedores · tecnicos
40mais · 60mais · educadores · criadores · recolocacao · familia
```

Adding an audience means adding another entry with `canal` and `gatilho`. The
key becomes `<publico>` in the title `A<N>-<publico>-v1`, so **no accents,
spaces, or hyphens**.

## How to change prompts, templates, and targets

These are the three things you’re most likely to want to change. The same
constraint applies to all of them: **everything is frozen when the flow is
created**—edits apply to FUTURE flows, and `/refazer` won’t pick up the change
either. An in-progress flow doesn’t change its rules midway.

### 1. Change the PROMPT (how scripts are written)

File: **`prompts/fase1-texto.md`**. This is the entire document phase 1 gives to
the agent. The sections, and what happens if you edit each one:

| section | edit here to… | caution |
|---|---|---|
| FIXED CONTEXT | change who the agent “already knows” (currently: Nei and Tiza as managers) | a name without a role becomes decoration—the section exists to prevent that |
| STEP ZERO | change the list of 11 formats, or what counts as a thesis/proof | **the formats are keys in `templates/mapa.json`**—if you change a name here, change it there too |
| HOOK WORKSHOP | change the hook criterion (currently: gap test, limit of 9 words) | this section has the biggest effect on reach |
| WRITING RULES (the 16) | change the tone, CTA, or what’s prohibited | rule 11b defines the `## IMAGENS` section format that the reel READS |
| output contract | change where it saves files or the `RESULT:`/`ERRO:` | breaking this breaks the entire phase |

Five variables are injected by the bot and **must not be removed**: `{{input}}`
(the topic), `{{publicos}}` (the flow’s actual targets), `{{pasta}}` (where to
save the file, absolute path), `{{ref}}`, and `{{saida}}`.

How it works with the skill: `inemaclub-textos` provides the file **structure**
(SPOKEN LINES / OVERLAYS / IMAGES / STRUCTURE); this prompt provides the
**rules** and overrides the skill where they disagree. Changed the file
structure? Do that in the skill, and it applies to everyone—not only promoavatar.

The other two prompts in the repo follow the same logic:
`prompts/fase-navega-avatar.md` (the browser route for phase 2) and
`prompts/reel-regras.md` (what this flow asks the reel to do).

### 2. Change the TEMPLATES (the reel layout)

Two different files, and confusing them is common:

**a) change how a layout looks** → edit `templates/<nome>.json`.
The schema is always the same:

```jsonc
{
  "nome": "empilhado-capa",
  "descricao": "…",                       // free text, helps with selection
  "canvas": { "largura": 1080, "altura": 1920 },
  "cores":  { "fundo": "#0E1116", "texto": "#FFFFFF", "acento": "#F5A623" },
  "faixas": {
    "topo": { "y": 0,    "altura": 704, "fonte": "imagens",
              "escurecer": 0.62,
              "headline": { "tamanho": 76, "peso": 900, "entrelinha": 1.04,
                            "margem_lateral": 48, "base_em": 56,
                            "maiusculas": true } },
    "meio": { "y": 704,  "altura": 608, "fonte": "avatar", "audio": true },
    "base": { "y": 1312, "altura": 608, "fonte": "texto", "painel": true,
              "hook": { "tamanho": 56, "peso": 800, "entrelinha": 1.16,
                        "margem_lateral": 56 } }
  },
  "transicao": { "flash": true, "duracao": 0.42,
                 "escala_entrada": 1.08, "pulso_max_s": 3.6 }
}
```

Three rules when editing:

- **The `y` + `altura` values for the bands must add up to 1920.** They don’t
  stack themselves—`y` is an absolute position. A missing band means a black
  band.
- **`fonte` is what feeds the band**: `imagens` · `avatar` · `texto` (the
  `hook`) · `explicativo` (muted looping clip). Changing `fonte` changes the
  contract with the text phase.
- **`escurecer`** is the veil over the image that makes the headline readable.
  Lower it too much and the text disappears against the bright part of the
  photo.

Creating a new layout means adding another `.json` to `templates/`, with
`"nome"` set to the filename. It’s immediately available for `--template`; to
include it in automatic selection, you also need step (b).

**b) change which layout each format maps to** → edit `templates/mapa.json`.
The keys are the STEP ZERO formats, **with and without accents** (`preparar.py`
matches the text written by the text phase, so both spellings are intentional):

```json
"mito versus realidade": "diptico",
"comparação": "diptico",
"comparacao": "diptico",
```

A format missing from the map **falls back to the default in the root of
`flow.json`**—it doesn’t invent a layout. So when you add a format to the prompt,
map it here in both spellings; otherwise, it will never use the layout you
intended.

**c) set a fixed layout for an audience**, overriding the map → the `template`
field inside the target in `flow.json` (example in the parameters section).
It overrides the map, but not `--template`.

### 3. Change the TARGETS (the audiences)

File: **`flow.json`**, key `alvos`. Each entry has two required keys and one
optional key:

```json
"empreendedores": {
  "canal": "lives24",
  "gatilho": "Transforme IA em redução de custos, vendas e novos negócios.",
  "template": "diptico"
}
```

| what I want | where |
|---|---|
| change an audience’s **problem/angle** | `gatilho`—this is what rule 2 of the prompt says to use |
| change **where the reel goes** | `canal`—becomes `~/projetos/yt-pub-<canal>/imports/videos` |
| set a fixed **layout** for that audience | `template` (optional) |
| **add** an audience | add another entry; the key is the slug |
| **remove** an audience | delete the entry |
| run **only some** without changing anything | `--alvo=jovens` or `\| alvos=a,b` when creating |

**The key is a contract, not a label.** It becomes:
the filename `textos/A<N>/<publico>.md` · the studio video title
`A<N>-<publico>-v1` · the reel’s `--alvo` · the images’ `seed-key`. That’s
why it must be **lowercase, without accents, spaces, or hyphens** (which is why
`pessoa-comum` became `pessoacomum`).

### 4. Change the DESTINATION (where the reel is delivered)

The destination isn’t a path written anywhere—it’s **derived from the
audience’s `canal`**, always using the same rule:

```
<canal>  →  ~/projetos/yt-pub-<canal>/imports/videos
```

The separation is intentional: the domain (this repo) provides only the
channel **name**; translating it to a folder is the bot’s job
(`src/dominio/destinos.ts`), in one place. If `flow.json` stored the full path,
it would become a second copy of the channel list—and copies diverge.

| I want to… | how |
|---|---|
| **change the channel** for an audience | edit `alvos.<publico>.canal` in `flow.json` |
| **create a new channel** | `mkdir -p ~/projetos/yt-pub-lives33/imports/videos`—that’s all; the bot doesn’t need to know |
| **put two audiences on the same channel** | give both the same `canal`; nothing prevents it |
| **change the RULE** (the base folder, `imports/videos`) | not here—it’s in the bot’s `destinos.ts`, and changes ALL flows |
| **deliver a standalone reel**, outside the flow | run `scripts/montar-reel.py --saida <caminho>` manually |

Current mapping for the 12 (from `docs/canais-e-destinos.md`, remapped on
2026-07-31):

```
empreendedores lives24  pessoacomum lives2   recolocacao lives3   mulheres  lives4
tecnicos       lives6   40mais      lives7   60mais      lives8   educadores lives9
criadores      lives11  jovens      lives22  profissionais lives23  familia  lives31
```

Like everything here, this **applies to the NEXT flow**: a flow in progress
doesn’t change destination midway.

## Reel templates

They live in `templates/` (set by `"templates_dir": "templates"` in
`flow.json`). There are 4 layouts, all 1080×1920, with `#0E1116` backgrounds
and `#F5A623` amber accents:

| template | top | middle | bottom | purpose |
|---|---|---|---|---|
| **`empilhado-capa`** *(root default)* | 704px image + `headline` | 608px avatar (audio) | 608px text panel (`hook`) | high-impact cover—the original format |
| **`empilhado-explicativo`** | 704px image + `headline` | 608px avatar (audio) | 608px explainer video, muted loop | when an explainer video is available |
| **`diptico`** | 960px image + `headline` | 960px avatar | **none** | myth vs. reality and comparisons—the image carries the contrast |
| **`imagem-plena`** | image fills all 1920px | avatar cropped at the **top right** | — | uncomfortable question, prediction, unexpected consequence |

In `imagem-plena`, the avatar goes at the top right as a production rule, not
for aesthetics: **the bottom is prohibited**—in production, the social
network’s interface (captions, @, buttons) covers the lower corner and the
avatar simply wouldn’t be visible.

Each band declares a `fonte`: `imagens`, `avatar`, `texto`, or `explicativo`.
That’s why rule 11b in the text prompt requires a `headline` for the top band
and a `hook` for the bottom panel. **A layout with a bottom band and no `hook`
means a black bottom band**: that’s what happened in A#23 (`hook` in 0 of 8
images). That’s why the prompt says to always write a `hook`, even for layouts
without a bottom band (`diptico` and `imagem-plena`).

### No one chooses a layout at render time

The layout comes from the `Formato escolhido:` line that the text phase saves
in each `<publico>.md` (the prompt’s STEP ZERO)—in other words, an editorial
decision that **you’ve already approved at the gate**. `templates/mapa.json`
does the mapping:

```
"mito versus realidade" → diptico        "pergunta incômoda" → imagem-plena
"comparação"            → diptico        ...
```

**Precedence** (handled by `preparar.py`):

```
explicit --template  ›  target’s template in flow.json  ›  mapa.json  ›  root template
```

A format that isn’t in the map falls back to the default; it doesn’t invent
one. In the real A#19, the text phase chose **9 different formats for 12
audiences**, producing real variation without anyone deciding anything at
render time.

## Parameters

### In chat (what `HELP.md` documents)

| option | effect |
|---|---|
| `--alvo=jovens` (repeatable) or `\| alvos=a,b` | only these audiences |
| `\| sombra` | shows the plan without queueing |
| `\| legenda` | word-by-word captions (default: off) |
| `\| versao=N` | changes the title’s `-vN` |
| `\| de=baixar` | starts partway through (text and avatar already done) |
| `\| api` | the BOT generates the avatar (~US$ 1/min from the prepaid wallet) |
| `\| api \| sem-portao` | generates it AND doesn’t stop for approval |
| `/status A#N` · `/aprovar A#N` · `/refazer A#N <publico>` · `/cancelar A#N` | check status |

### In the reel engines (`scripts/`)

`montar-reel.py`—phase 3 from start to finish:

| flag | |
|---|---|
| `--avatar` | **required**—the HeyGen MP4 |
| `--ws` | **required**—the reel workspace |
| `--alvo` | audience; becomes the images’ `seed-key` (default `reel`) |
| `--textos` | the `<publico>.md`—the `## IMAGENS` section comes from here |
| `--template` | layout override (takes precedence over everything) |
| `--flow` / `--mapa` | where to resolve the template and map |
| `--qualidade` | `high` (default) · `standard` · `draft` |
| `--cta` / `--sem-cta` | closing clip (`cta/cta-9x16.mp4`) |
| `--pular-preparo` | reuses the preparation already done in `--ws` |
| `--saida` | MP4 destination |

`preparar.py`—preparation only (images + transcription). It has the same flags,
plus `--explicativo`, `--sem-imagens`, `--sem-transcricao`, and `--sem-montar`.

### Examples

```bash
# default reel for one audience—the layout comes from the map
python3 scripts/montar-reel.py \
  --avatar state/artefatos/fluxos/A34/A34-jovens-v1.mp4 \
  --ws /tmp/ws-A34-jovens --alvo jovens \
  --textos textos/A34/jovens.md --flow flow.json

# cheap draft, just to check framing
python3 scripts/montar-reel.py ... --qualidade draft --sem-cta

# force a layout, ignoring the map
python3 scripts/montar-reel.py ... --template imagem-plena

# change template/CTA without regenerating images
python3 scripts/montar-reel.py ... --pular-preparo --saida saida/A34-jovens.mp4

# with an explainer video in the bottom band
python3 scripts/preparar.py ... --alvo tecnicos \
  --explicativo saida/explicativo-tecnicos.mp4 --template empilhado-explicativo

# prepare now, assemble later
python3 scripts/preparar.py ... --sem-montar
```

Set an audience’s layout directly in `flow.json` (overrides the map, but not
`--template`):

```json
"empreendedores": {
  "canal": "lives24",
  "gatilho": "Transforme IA em redução de custos...",
  "template": "diptico"
}
```

## Attention: everything here is frozen at creation

`flow.json`, the prompts, and options (`legenda`, `cta`) are **frozen when the
flow is created**. Edits apply to FUTURE flows—a flow in progress doesn’t
change its rules midway, so `/refazer` won’t pick up the change either.
