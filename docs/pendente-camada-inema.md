# PENDENTE — Camada "conteúdo próprio do INEMA" no prompt da fase 1

Anotado em 2026-09-10. Ainda NÃO aplicado — para discutir antes de mexer no prompt
(mudança no prompt afeta só fluxos novos).

## Origem

O dono trouxe um prompt de "agente de conteúdo do INEMA" (Camada 1 = conteúdo real do
INEMA: sistemas, testes, erros, decisões; Camada 2 = provocação natural; estrutura
gancho → fato → experiência INEMA → aplicação → provocação → interação; teste final
"poderia ter sido feito por qualquer um no ChatGPT?"). Pediu comparação com o prompt de
plano da fase 1 deste repo.

## O que já converge (não mexer)

- Gancho (oficina de 5, teste da lacuna, 9 palavras) — mais exigente que o texto novo.
- Posicionamento — "quando o assunto for um debate" obriga a tomar lado.
- Provocação — formatos (afirmação provocativa, opinião contrária, consequência
  inesperada, previsão) + lacuna aberta cedo e fechada no fim.
- Anti-genérico — pessoa concreta, nomear a coisa, benefício antes de mecânica, última
  frase repetível.
- Credibilidade — regras 9 e 10 (nada inventado) são mais duras que o texto novo.

## O que falta no prompt atual (candidato a entrar)

1. **Camada 1 não existe.** O assunto é tratado como "dado" e toda a energia vai na
   embalagem. Nenhum passo manda vasculhar o assunto atrás do que é NOSSO (sistema
   construído, teste feito, erro achado, decisão tomada, número medido) e dar
   prioridade a isso sobre conhecimento genérico.
   → Proposta: item novo no PASSO ZERO — "O que é NOSSO neste assunto" (lista). Lista
   vazia = declarar no resumo "assunto sem experiência própria", nunca inventar.
2. **Teste do ChatGPT** não está na checagem antes de gravar.
   → Proposta: 4ª pergunta ao lado de gancho / o que muda / eu mandaria.
3. **Interação integrada.** O gatilho ENGAJAMENTO aceita "salva isto" / "marca alguém",
   que é o que o texto novo quer evitar.
   → Proposta: pergunta específica que obriga a tomar posição sobre o próprio caso
   ("na sua empresa, você deixaria um agente executar isso sozinho?"); "salva" só no
   tipo autoridade.
4. **Estrutura de seis blocos** (gancho → fato → experiência → aplicação → provocação
   → interação) não existe; a atual é gancho → dor → solução → CTA (estrutura de anúncio).

## Onde o texto novo CONFLITA com regras que existem por motivo (não copiar literal)

- "Urgência" e "medo de ficar para trás" como ferramentas permitidas batem na regra 10
  (nasceu de "garanta sua vaga" sem vaga). Só entram com "se o assunto sustenta".
- "Experiência própria" em primeira pessoa ("nós testamos", "descobrimos") bate na
  regra da pessoa concreta / testemunho (nasceu de depoimento inventado). Só é legítimo
  se veio LITERALMENTE no assunto. Consequência: a Camada 1 depende de quem pede o
  fluxo colocar no assunto o que foi feito — o prompt pode exigir, não pode inventar.
- O texto novo é prompt de agente de conteúdo em geral; este arquivo é contrato de
  pipeline (caminho absoluto, seções FALA/SOBREPOSIÇÕES/IMAGENS, exit 3 do motor,
  commit sem push). Substituir quebra o fluxo — é acréscimo, não troca.

## Específico deste repo (promoavatar — um vídeo por público, promocional)

- A sequência de seis blocos entra como FORMATO ADICIONAL na lista do PASSO ZERO, não
  como padrão: aqui o vídeo é o promocional, e dor → solução → CTA continua sendo o eixo.
- Arquivo alvo: `prompts/fase1-texto.md` (PASSO ZERO, gatilho ENGAJAMENTO da regra 11,
  checagem do item 3 de "O que fazer").
