# Regras do reel do promoavatar

Estas regras nasceram na skill global `reel-edita-inema` em 2026-08-03 e foram
movidas para cá em 2026-08-04, a pedido do dono. O motivo importa: a skill é
**lida ao vivo** e vale para TODOS os domínios na hora — mexer nela mudava o
comportamento de fluxos em andamento e do `promoavatar3`, que a gente decidiu
não tocar ainda. Aqui elas são versionadas, viram snapshot por fluxo e são
revisáveis no portão.

A skill continua responsável pelo que é mecânica de reel (corte, SFX, render).
O que está abaixo é decisão editorial DESTE pipeline.

---

## 1. A imagem 1 é gatilho de atenção, não ilustração

A primeira imagem do topo **é a capa que aparece no feed**: vista pequena,
parada e ANTES de qualquer texto ser lido. Ela carrega a **provocação** — a
tensão, o custo, o absurdo ou a consequência concreta.

**Ilustrar o tema é o erro padrão.** "Pessoa olhando para uma interface azul
brilhante" é o TEMA (IA), não a provocação. Medido em 2026-08-03: cinco imagens
com prompts diferentes caíram todas no mesmo clichê.

Três testes antes de aceitar:

1. **Transferência** — serviria para qualquer outro reel sobre o tema? Então
   está errada. Tem de ser presa a ESTE assunto e ao gatilho DESTE público.
2. **Polegar** — reduzida a 1/4 e sem a headline, ainda provoca uma pergunta?
3. **Tensão** — mostra o que se PERDE, o que QUEBRA, o que fica absurdo? Ou só
   mostra o objeto do assunto? Só o objeto = ilustração = refazer.

**Clichês proibidos:** pessoa de perfil diante de tela/holograma brilhante · HUD
circular · chuva de código estilo matrix · cérebro de circuitos · robô apertando
mão de humano · lâmpada de ideia.

**Prefira:** a consequência concreta, o objeto fora de lugar, a escala
inesperada, o antes/depois no mesmo quadro, o detalhe humano que denuncia a
mudança.

## 2. A faixa da BASE é um PAINEL, não uma legenda

Conferido no reel 229 (2026-08-03): a faixa de 608px estava ~500px vazia, com
uma linha de texto colada no rodapé e um traço solto no meio — leitura de
legenda, não de bloco de design, enquanto o topo parecia pôster. A base é **1/3
da tela**.

- **Ocupe a faixa.** O bloco se distribui na altura, centrado — nunca ancorado
  no rodapé.
- **Duas linhas, tipografia grande**, no peso da manchete do topo. Se o texto
  não enche duas linhas, reescreva o hook — não diminua a fonte.
- **Dê corpo ao bloco:** caixa com fundo, faixa de cor ou imagem esmaecida. O
  topo tem a imagem para dar peso; a base precisa do equivalente.
- **O acento é o MESMO do card do topo daquele segmento.** No 229 o topo era
  âmbar e a base ciano — dois acentos brigando no mesmo quadro.

> Nos templates `diptico` e `imagem-plena` não existe faixa de base: o vazio
> some por estrutura, e esta regra não se aplica.

## 3. Imagens: proporção, seed e modelo

- **O tamanho sai do template** (`preparar.py` resolve): `empilhado-capa` 1088×704 ·
  `diptico` 1088×960 · `imagem-plena` 1088×1920. Gerar fora da proporção e
  deixar o `object-fit` cortar deforma a cena — e nenhum lint pega isso.
- **`--seed-key "<publico>#<N>"`, nunca `--seed` fixo.** Com seed 7 em tudo,
  dois públicos do mesmo assunto saem **gêmeos de composição** (medido: mudou a
  pessoa, não a cena — mesmo enquadramento, mesmo HUD, mesmo gráfico no mesmo
  canto). O `--seed-key` mantém o determinismo e dá composição própria a cada um.
- **NÃO mexa em `--steps`.** O flux2-klein é *step-distilled*; a doc do inemaimg
  diz "piora acima de 4". Testado e descartado.
- **NÃO troque para `flux2-dev`.** Não sobe nesta máquina de propósito; o erro
  500 (`bitsandbytes`) é esperado, não é bug.
- **Imagem enviada pelo dono nunca é cortada** (`arquivo:` na seção IMAGENS):
  cabe inteira, com fundo borrado no resto. `modo: cover` pede o contrário.

## 4. QC: o determinístico PRIMEIRO, o olho depois

Frame é o item mais caro do job: cada um entra no contexto e é **relido em toda
mensagem seguinte** até o fim. Medido em outra fase do mesmo sistema: um loop de
verificação por imagem levou uma tarefa de 3 min para 13 min e 13,5M tokens.

- **Portão 1, antes de renderizar (~zero):** `lint` + `lint-timeline.py` +
  `verify-cut.py`. Renderizar para descobrir com o olho o que o lint diria de
  graça é o desperdício mais caro da fase.
- **Portão 2, depois do render (~zero):** `ffprobe` — duração, 1080×1920, os
  dois streams. Render truncado ou mudo se descobre aqui.
- **Portão 3, o olho, e DIRIGIDO:** `/watch` com ~10 frames que decidem algo
  (t=0, cada troca de imagem, o CTA, e o que o portão 1 acusou). Nunca a série
  inteira duas vezes.
- **Não refaça `/watch` depois do `mix-sfx.py`:** ele roda com `-c:v copy`, o
  vídeo sai **bit a bit idêntico** ao que você já revisou. O que muda é o áudio,
  e áudio não se confere com imagem.
