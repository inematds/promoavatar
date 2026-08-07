/promoavatar <assunto> — reels de divulgação com portão humano

O bot escreve os textos e PARA. Você gera os avatares no HeyGen; quando
terminar, /aprovar libera o download e os reels.

COMO USAR

  /promoavatar Não comece aprendendo ferramentas
  /promoavatar Assunto | alvos=mulheres           só um público (barato p/ testar)
  /promoavatar Assunto --alvo=jovens --alvo=40mais   mesma coisa, forma curta
  /promoavatar Assunto | sombra                   mostra o plano, não enfileira
  /promoavatar Assunto | legenda                  COM legenda (padrão é sem)
  /promoavatar Assunto | de=baixar                você já fez texto E avatar

FLUXO — 4 fases, 2 portões

  1. texto    o bot escreve UM roteiro por público
     ⏸️  PORTÃO 1 — você revisa os textos e gera os avatares no estúdio
  2. avatar   normalmente VOCÊ, na mão (ver "OS AVATARES" abaixo)
  2.5 baixar  /aprovar A#N → o bot acha os vídeos pelo TÍTULO e baixa
     ⏸️  PORTÃO 2 — você confere os avatares antes de gastar render
  3. reel     monta o reel (capa de impacto com o gatilho do público) e
              ENTREGA no canal lives daquele público

Não há fase separada de publicação: a entrega é o fim da fase reel, e o
destino é o `canal` do público.

TROCAR A IMAGEM DE CAPA (foto sua no lugar da gerada)

Mande a FOTO no chat COM esta legenda — a legenda da imagem, não uma
mensagem separada:

  capa: A#25 jovens          IMAGEM 1 (a capa do feed) desse público
  capa: A#25 *               a mesma imagem em TODOS os públicos do fluxo
  capa: A#25 jovens 3        troca a IMAGEM 3, não a capa
  capa: A#25 jovens cover    preenche CORTANDO as laterais

O padrão é `contain`: a imagem cabe INTEIRA, e o resto da faixa é preenchido
com uma cópia borrada dela mesma. Imagem sua não é cortada sem você pedir —
se ela traz texto ou um rosto enquadrado, cortar destrói o trabalho. Use
`cover` só quando a imagem for de fundo, sem texto.

QUANDO mandar: no PORTÃO da fase de texto, ANTES do /aprovar. É a única
janela em que trocar a capa é de graça — nenhum avatar gerado, nenhuma
imagem paga, nenhum render. Mandar depois do reel montado ainda escreve no
roteiro, mas o vídeo só muda com /refazer (o bot avisa).

Sem foto anexada ele recusa em vez de gravar linha vazia. Se você já tem o
caminho no disco, dá para digitar:

  capa: A#25 jovens | arquivo=/caminho/da/imagem.png

O TÍTULO É O CONTRATO

No estúdio, nomeie cada vídeo EXATAMENTE assim:

  A<N>-<publico>-v1        ex.: A7-mulheres-v1

O <N> é o número do fluxo, que aparece quando você cria (`criado: A#7`). É por
esse nome que o download encontra o vídeo — nome diferente, vídeo não
encontrado, e a fase expira em 90 minutos. O /status A#7 mostra os títulos.

A LEGENDA DO AVATAR SE DECIDE NO ESTÚDIO

Gravou com legenda no HeyGen, o download traz o vídeo legendado; gravou sem,
traz o limpo. O bot não escolhe — ele pega a versão legendada quando ela
existe.

A opção `| legenda` acima é OUTRA coisa: é a legenda que o NOSSO editor
desenha. Ligar as duas faz sair DUAS legendas. Escolha uma:

  legenda no estúdio   ->  crie o fluxo SEM `| legenda`
  reel com `| legenda` ->  grave SEM legenda no estúdio

E lembre: legenda queimada vem enquadrada para 16:9 — no 9:16 ela pode ser
cortada ou colidir com a base, e não há como removê-la depois. Detalhe e o
que foi medido: README.md.

ACOMPANHAR

  /status A#7              fase × público, e o que está esperando você
  /aprovar A#7             libera o portão (= "terminei os avatares")
  /refazer A#7 mulheres    só o público que falhou, tentativas zeradas
  /cancelar A#7 [publico]  cancela; o que já foi criado no estúdio continua lá

PÚBLICOS

  pessoacomum jovens profissionais mulheres empreendedores tecnicos
  40mais 60mais educadores criadores recolocacao familia

Cada um tem canal (livesN) e gatilho próprios — a lista mora no flow.json
deste repo, e é ele que o bot lê. Mudou um público? Muda ali, sem tocar no bot.

ONDE O REEL É ENTREGUE

O canal do público vira pasta pela regra:

  lives4  ->  ~/projetos/yt-pub-lives4/imports/videos

O caminho não está escrito em lugar nenhum: é derivado. Trocar o canal de um
público = editar o flow.json. Criar canal novo = criar a pasta, só isso.
Detalhe em docs/canais-e-destinos.md.

OS AVATARES: SUA MÃO OU A API

Por padrão você grava no HeyGen (é o de sempre). Com `| api`, o BOT gera —
e isso gasta da carteira pré-paga da HeyGen (~US$ 1 por minuto de vídeo).

  /promoavatar <assunto> | api
  /promoavatar <assunto> | api | sem-portao   gera E não para para aprovar

`| api` NÃO tira o portão: você ainda revisa os textos e dá /aprovar antes de
gastar. Para a esteira inteira sem parar, peça as duas flags.

Confira antes com `| sombra`: a fase `gerar` só aparece no plano quando a
opção `| api` está ligada.

A fase 2 tem 5 rotas, e só uma roda por fluxo:

  manual      nenhuma flag — o padrão; você grava e o bot só espera
  | estudio   o bot abre/prepara o estúdio, você conclui
  | api       o bot gera pela API (carteira pré-paga)
  creditos    fase `gerar-creditos` no flow.json — flag não documentada aqui
  navega      fase `navega-avatar` (agente no navegador) — cara: ~17,8k
              tokens por público, ~214k nos 12; flag não documentada aqui

Qualquer rota que você use, o TÍTULO continua sendo o contrato.

O QUE NÃO É DESTE REPO

Este repo é só a DEFINIÇÃO do pipeline. Quem executa é o inemaccbot: os
comandos do chat, as filas e timeouts, as tarefas heygen.*, o estado em
state/artefatos/fluxos/A<N>/ e as pastas ~/projetos/yt-pub-<canal>/. E
COMO o reel é montado (cores, fontes, SFX) é da skill global
reel-edita-inema — mexer nela muda todo reel da marca.

Regra de bolso: se muda TODOS os fluxos, não é daqui; se muda só o
promoavatar, é daqui.
