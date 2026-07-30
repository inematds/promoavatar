# promoavatar

Derivado do `inemaclubpromover` com **portão humano**: o bot escreve os textos e
PARA. Quem gera os avatares no HeyGen é você; quando terminar, `/aprovar A#N`
libera o download e o reel.

## Diferença para o `promoclub`

| | promoclub | promoavatar |
|---|---|---|
| fase 1 (texto) | bot | bot |
| fase 2 (avatar) | bot, `claude --chrome` no Chromium `:99` | **você, no estúdio** |
| portão | não tem | `/aprovar A#N` depois dos avatares prontos |
| fase 2.5 (baixar) | bot | bot |
| fase 3 (reel) | bot | bot |

Referência: `A#3` (o promoclub usa `P#3`). São fluxos diferentes e o bot recusa
a referência com prefixo trocado.

## Por que existe

Render de avatar e fila de reel custam caro e não se desfazem. Aprovar o texto
antes vale mais que retentar depois. E com a fase 2 na mão some a peça mais
frágil do pipeline: o navegador headless, o Chromium `:99`, o Xvfb, a aba que
nasce escondida.

## Onde vive o quê

- `flow.json` — os 12 públicos (canal + gatilho) e as 3 fases;
- `prompts/fase1-texto.md` — o prompt da fase de texto, congelado a cada fluxo
  criado (editar aqui só afeta fluxos NOVOS);
- os textos gerados e os artefatos ficam onde a skill `inemaclub-textos` grava.

Os avatares baixados vão para `state/artefatos/fluxos/A<N>/` no repo do bot, com
o título `A<N>-<publico>-v1` — o MESMO nome que você deve usar no estúdio, senão
o download não encontra o vídeo.
