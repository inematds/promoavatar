---
name: reel-promoavatar
description: Monta o reel 9:16 do promoavatar a partir do MP4 do avatar HeyGen, usando os motores DESTE repo (scripts/montar-reel.py). Use quando um job da fase `reel` do fluxo promoavatar chegar. Não use para outros domínios — para reel genérico é a skill global reel-edita-inema.
---

# reel-promoavatar — o reel deste projeto, com os motores deste projeto

## Por que esta skill existe

A skill global `reel-edita-inema` tem **cópias próprias** de `preparar.py` e
`montar.py` em `~/.claude/skills/reel-edita-inema/scripts/`. No A#23 o agente
rodou aquelas cópias em vez das deste repo, e o resultado foi medido:

- `template: None` no manifesto — o layout não foi resolvido, e os dois públicos
  saíram no mesmo empilhado em vez de `imagem-plena` e `diptico`;
- `html: None` — o encadeamento não rodou e o agente **escreveu o HTML à mão**,
  que é de onde vêm a base desalinhada, a headline pequena e o painel vazio;
- `hook` inventado na hora em um público e ausente no outro.

O `reel-regras.md` já dizia "os scripts deste fluxo são os do REPO, não os de
`~/.claude/skills/`". Não adiantou: **instrução não é portão** — foi a sexta vez
medida no mesmo dia. Esta skill é o portão. Ela não conhece outro caminho.

## O caminho

**UM comando. Não existe outro.**

```
python3 <repo>/scripts/montar-reel.py \
    --avatar <mp4 do avatar> \
    --ws ~/projetos/output/reels/<slug> \
    --alvo <publico> \
    --textos <repo>/textos/<REF>/<publico>.md \
    [--saida <caminho final exigido pelo job>]
```

Ele faz, nesta ordem: preparar (mídia, transcrição, imagens da seção `IMAGENS`,
tempos a partir do transcript, template, `index.html`) → portão 1 (lint + ritmo
visual) → render → revisor → CTA → QC (portões 2 e 3).

Saídas com nome **fixo**:

| arquivo | o que é |
|---|---|
| `<ws>/motion/index.html` | composição (gerada do template — nunca escrita à mão) |
| `<ws>/motion/corpo.mp4` | render sem CTA |
| `<ws>/final/reel.mp4` | entregável |
| `<ws>/qc/mosaico.png` | a única imagem que precisa de olho |

Exit **0** pronto · **3** algum portão reprovou (a saída diz qual) · **2** erro
de arquivo.

## O que você NÃO faz

- **Não escreva `index.html`.** Se o script falhou, conserte a causa que ele
  apontou e rode de novo. HTML à mão foi o defeito, não a solução.
- **Não escolha o layout.** Ele decorre do `Formato escolhido:` que a fase de
  texto gravou e o dono aprovou no portão. A regra que venceu fica no manifesto.
- **Não invente headline nem hook.** Vêm da seção `## IMAGENS` do texto do
  público (regra 11b). Se faltarem, o script reprova — é o comportamento certo,
  e o conserto é na fase de texto.
- **Não gere nem mixe SFX**, **não ligue legenda**, **não spawne subagente
  revisor**. Ver `docs/decisoes-reel.md` para a evidência e o caminho de volta
  de cada uma.
- **Não use `/watch` nem extraia frames com `ffmpeg` na mão.** O QC já escolheu
  os frames e montou o mosaico; cada frame solto é relido em toda mensagem
  seguinte até o fim do job.
- **Não instale nada** (`npm i`, `pip`, `apt`, browsers). Se faltar ferramenta,
  declare `ERRO: falta <o quê>` e pare.

## O que sobra para você

Olhar **`<ws>/qc/mosaico.png`** — uma imagem — e responder três perguntas:
a imagem 1 provoca? a headline lê de relance? o fecho tem o CTA?

E reagir a exit != 0: ler qual portão reprovou e consertar a causa.

## Regras editoriais

Estão em `<repo>/prompts/reel-regras.md`, versionadas neste projeto: imagem 1
como gatilho (com os três testes e os clichês proibidos), a faixa de base como
painel, proporção e seed das imagens, e os portões. **Elas valem sobre o que a
skill global disser.**
