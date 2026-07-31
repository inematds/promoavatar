/promoavatar <assunto> — reels de divulgação com portão humano

O bot escreve os textos e PARA. Você gera os avatares no HeyGen; quando
terminar, /aprovar libera o download e os reels.

COMO USAR

  /promoavatar Não comece aprendendo ferramentas
  /promoavatar Assunto | alvos=mulheres           só um público (barato p/ testar)
  /promoavatar Assunto --alvo=jovens --alvo=40mais   mesma coisa, forma curta
  /promoavatar Assunto | sombra                   mostra o plano, não enfileira
  /promoavatar Assunto | de=baixar                você já fez texto E avatar

FLUXO

  1. texto    o bot escreve UM roteiro por público
     ⏸️  PARA — você revisa os textos e gera os avatares no estúdio
  2. baixar   /aprovar A#N → o bot acha os vídeos pelo TÍTULO e baixa
  3. reel     monta o reel (capa de impacto com o gatilho do público) e
              entrega no canal lives daquele público

O TÍTULO É O CONTRATO

No estúdio, nomeie cada vídeo EXATAMENTE assim:

  A<N>-<publico>-v1        ex.: A7-mulheres-v1

O <N> é o número do fluxo, que aparece quando você cria (`criado: A#7`). É por
esse nome que o download encontra o vídeo — nome diferente, vídeo não
encontrado, e a fase expira em 90 minutos. O /status A#7 mostra os títulos.

ACOMPANHAR

  /status A#7              fase × público, e o que está esperando você
  /aprovar A#7             libera o portão (= "terminei os avatares")
  /refazer A#7 mulheres    só o público que falhou, tentativas zeradas
  /cancelar A#7 [publico]  cancela; o que já foi criado no estúdio continua lá

PÚBLICOS

  pessoa-comum jovens profissionais mulheres empreendedores tecnicos
  40mais 60mais educadores criadores recolocacao familia

Cada um tem canal (livesN) e gatilho próprios — a lista mora no flow.json
deste repo, e é ele que o bot lê. Mudou um público? Muda ali, sem tocar no bot.

ONDE O REEL É ENTREGUE

O canal do público vira pasta pela regra:

  lives24  ->  ~/projetos/yt-pub-lives24/imports/videos

O caminho não está escrito em lugar nenhum: é derivado. Trocar o canal de um
público = editar o flow.json. Criar canal novo = criar a pasta, só isso.
Detalhe em docs/canais-e-destinos.md.
