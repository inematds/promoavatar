# A segunda metade da fase reel: o que é fixo, o que é decisão

Levantamento de 2026-08-04, para decidir se a fase `reel` pode virar
`kind: function` com o agente entrando só na exceção.

A primeira metade já é determinística: `preparar.py` (mídia, transcrição,
imagens, tempos, template, `segmentos.json`) → `montar.py` (index.html) →
render → `qc-frames.py` (portões 2 e 3). O que se levanta aqui é o que vem
**depois do QC**.

## Evidência: hoje ela não é fixa — mas não por precisar de decisão

Sete workspaces do A#22, **sete estruturas diferentes**. Nenhuma igual a outra:

| workspace | artefatos próprios |
|---|---|
| `A22-40mais` | nenhum além do mínimo |
| `A22-capa-impacto-lives11` | `segmentos.json` |
| `A22-lives9-educadores` | `segmentos.json` |
| `A22-mulheres-capa` | `motion/reel-body.mp4` |
| `A22-profissionais-capa-impacto` | `final/`, `motion/avatar-crop.mp4` |
| `A22-recolocacao-lives3` | `concat-list.txt`, `render-standard.mp4`, `render-high.mp4` |
| `A22-tecnicos-lives6-capa` | `captions.json`, `captions-words.json`, `concat-cta.txt`, `corpo-final.mp4`, `preview-standard.mp4` |

Nomes de saída diferentes para a mesma coisa (`reel-body` / `corpo-final` /
`render-high`), listas de concat escritas à mão com nomes diferentes, e três
reels que sequer chegaram a um MP4 de corpo. Isso é improviso, não variação
editorial: nada no conteúdo desses sete públicos justifica sete caminhos.

## Peça por peça

| peça | precisa de modelo? | evidência |
|---|---|---|
| corte de repetições (`islands.py`, `cut.py`, `verify-cut.py`) | **não — não se aplica** | `repeticoes=0` em **18 de 18** reels (A#21 e A#22). O avatar é TTS do HeyGen: não tem falso começo, blooper nem tomada repetida. Esses scripts existem para bruto gravado por humano. |
| CTA no fim | **não** | arquivo fixo `cta/cta-9x16.mp4`, sempre o mesmo, concatenado. Hoje cada reel escreve seu próprio `concat-*.txt`. |
| render final `--quality high` | **não** | mesmo comando sempre. |
| legendas (`captions.py`) | **quase não** | default é SEM. Quando ligada, o único parâmetro editorial é `--keywords`, e ele pode vir da fase 1 do mesmo jeito que `headline:`/`hook:` vêm hoje (regra 11b). |
| SFX (`make-sfx.sh`, `mix-sfx.py`) | **na prática, não roda** | nenhum dos 18 workspaces tem pasta `sfx/`. A skill manda mixar; não aconteceu em nenhum. Decidir se entra de verdade ou sai da receita. |
| revisor da FASE 5 (subagente obrigatório) | **sim, e é caro** | subagente independente que re-transcreve o render inteiro e o lê procurando repetição. Mas o que ele checa (`verify-cut.py`, `lint-timeline.py`) é script, e a repetição que ele caça é a que dá 0 em 18 de 18. |
| o olho no mosaico | **sim** | imagem 1 provoca? headline lê de relance? o fecho tem CTA? Não é automatizável e não se tentou. |
| reagir a exit != 0 | **sim** | é o papel legítimo do agente aqui. |

## Conclusão

Tirando o olho e a recuperação de falha, **a segunda metade é tão fixa quanto a
primeira** — ela só não parece, porque nunca foi escrita como uma. Duas peças
mudam de status ao serem olhadas de perto:

- o **corte** não é opcional nem caro: é **inaplicável** a este pipeline;
- o **revisor da fase 5** é o maior gasto restante e checa sobretudo aquilo que
  já é script ou que nunca ocorreu.

Caminho: um `montar-reel.py` que encadeie corpo → CTA → render high → QC e
devolva o mosaico, com nomes de arquivo fixos. Aí a fase `reel` vira
`kind: function` e o modelo entra por exceção (exit != 0) e para o julgamento
visual — que é onde ele vale o que custa.

Decisões pendentes antes de escrever isso, e são suas:
1. **SFX entram ou saem?** Hoje estão na receita e não acontecem.
2. **Legenda:** manter default SEM, ou ligar e trazer `keywords:` da fase 1?
3. **Revisor da fase 5:** mantém, corta, ou vira script?
