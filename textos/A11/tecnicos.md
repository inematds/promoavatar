## Versão única — o context bloat que ninguém mede

### FALA (texto para o HeyGen — falar exatamente isto)
Sua fatura de API subiu e o volume de chamadas não explica o motivo? O problema é context bloat: cada turno reenvia histórico, tool results e instruções acumuladas. Um caso extremo processou 3,77 bilhões de tokens em um dia — 96% era conteúdo reutilizado. Dá pra cortar isso na engenharia: prompt caching em produção, limite rígido de entrada e saída, compactação de contexto em sessões longas, e carregar só as ferramentas necessárias por tarefa. Pare de só testar prompt solto — construa o pipeline certo. Existe uma skill que automatiza esse controle, a Token Saver. A trilha CCTop, no inema.club, ensina a arquitetura completa disso. Entre agora no inema.club e comece pela trilha de IA.

### SOBREPOSIÇÕES DE TELA (fase do reel — NÃO falar)
**ATENÇÃO (0–2s):** "Sua fatura de API subiu e o volume de chamadas não explica"
**RETENÇÃO (miolo):** "3,77B tokens/dia · 96% reused" — vira "aqui está o context bloat".
**ENGAJAMENTO:** "Comenta: já mediu o token overhead da sua stack?"
**CTA (fecho):** "Entre agora no inema.club — trilha CCTop"

## ESTRUTURA
Dor (fatura de API sem explicação óbvia) → possibilidade (arquitetura, não só uso de ferramenta) → demonstração (dado real, técnicas: prompt caching, limites, compactação) → nome da técnica (skill Token Saver) → trilha real (CCTop) → CTA imperativo.
