# Módulos de voo

Leia o módulo indicado pela tabela de roteamento do SKILL.md. Quando o pedido for uma cotação de voo, as tabelas pedidas aqui vão para a planilha e a resposta segue `formato-de-entrega.md`.

## Sumário
- Módulo 1. Matriz de datas flexíveis
- Módulo 2. Aeroportos próximos e rotas alternativas
- Módulo 3. Conexões por conta própria, multi-city e várias cidades
- Módulo 4. Auditoria: é mesmo uma boa oferta?
- Módulo 9. Decisão final: reserve agora, espere ou mude de plano

---

## Módulo 1. Matriz de datas flexíveis

**Entrada:** origem, destino, mês, duração.

1. Consulte o calendário e o gráfico de preços (Google Flights; Skyscanner em "mês inteiro") para a duração pedida.
2. Monte a matriz ida × volta (no mínimo as 5 melhores e as 3 piores combinações).
3. Identifique picos: feriados no Brasil e no destino, eventos, férias escolares. Cada pico com fonte.
4. Tendência histórica: só o que a fonte mostra (faixa típica do Google Flights, artigos citados). Sem dado, lacuna.
5. Teste duração ±1 e ±2 dias quando gerar economia relevante.
6. Compare ida e volta com **duas passagens só de ida**, inclusive em companhias diferentes. Em viagens ponto a ponto, o risco é baixo porque um bilhete não depende do outro; diga isso.
7. Com hospedagem já fechada, aplique `comparativo-de-datas.md`.
8. Para os finalistas, aplique o protocolo multifonte (`fontes-e-navegacao.md`).

**Para a planilha:** melhores combinações, períodos a evitar e tendência. **Na resposta:** a combinação escolhida, onde comprar e por quê.

## Módulo 2. Aeroportos próximos e rotas alternativas

**Entrada:** origem, destino, datas. Raio padrão de 240 km (≈150 milhas), ajustável.

1. Liste os aeroportos com voos regulares no raio, nos dois lados.
2. Para cada combinação viável: tarifa, transporte terrestre (ônibus, carro com combustível, pedágio e estacionamento, ou transfer), tempo extra porta a porta e riscos (último ônibus, pernoite).
3. Custo efetivo = tarifa + terrestre ida e volta + pernoites extras + refeições extras.
4. Economia líquida versus a rota direta e **custo por hora extra** (economia ÷ horas a mais), para a pessoa julgar se vale o tempo.

**Veredito:** "compensa", "não compensa" ou "compensa só se…", com o limite (ex.: "só vale se sua hora valer menos de R$ X").

## Módulo 3. Conexões por conta própria, multi-city e várias cidades

**Entrada:** origem, destino(s), datas.

1. Pesquise: bilhete único com escalas; multi-city ou open-jaw; trechos separados (incluindo low-cost); stopover oferecido pela companhia.
2. Para bilhetes separados com conexão, verifique:
   - **Bagagem:** se precisa retirar e despachar de novo; franquia de cada bilhete.
   - **Imigração:** se retirar a bagagem obriga a entrar no país da conexão, é preciso visto ou autorização (fonte oficial). Exemplo: conexão nos EUA exige visto mesmo em trânsito.
   - **Terminal ou aeroporto:** troca na mesma cidade.
   - **Proteção:** com bilhetes separados, um atraso não é coberto; a segunda companhia não reacomoda.
3. Margem segura de conexão por conta própria (heurística da skill, não regra oficial): 3 h doméstica sem bagagem; 4 a 5 h internacional com novo despacho e imigração; pernoite se o último voo do dia for o único.
4. **Várias cidades:** compare a soma dos trechos separados com um bilhete multi-city na mesma companhia ou aliança.
5. **Hidden city (descer na escala):** só explique se a pessoa mencionar. Riscos: viola o contrato da maioria das companhias; a bagagem despachada vai até o destino final; os trechos seguintes do bilhete são cancelados; risco de perder milhas ou a conta do programa; a companhia pode mudar a rota. Recomendação padrão: evitar.

**Saída:** opções com preço, tempo total, número de bilhetes, novo despacho, visto, margem de conexão e nível de risco (baixo, médio, alto), mais o checklist de riscos da recomendada.

## Módulo 4. Auditoria: é mesmo uma boa oferta?

**Entrada:** a oferta (rota, datas, preço, companhia, tarifa, bagagem, regras).

1. Busque a faixa típica de preço da rota (Google Flights "preço típico", histórico, preços atuais em outras companhias).
   - Use a faixa **por pessoa** (busca com 1 passageiro). A faixa exibida para vários passageiros pode não bater com a de 1; se divergir, relate e não use na nota.
   - No gráfico de histórico do voo, um degrau súbito com preço parado no alto costuma indicar que as tarifas baratas esgotaram. Valores lidos do gráfico são aproximados; diga isso.
   - Confira o mesmo voo no site da companhia, em agências e em milhas.
2. Normalize: mesma bagagem, mesma flexibilidade, mesmo número de escalas.
3. Leia as regras da tarifa: remarcação, reembolso, assento, bagagem, no-show.
4. Aplique a nota.

**Nota (heurística da skill)**, pelo preço normalizado versus a faixa típica:

| Diferença vs. típico | Nota base |
|---|---|
| −30% ou menos | 9–10 |
| de −29,9% a −15% | 7–8 |
| de −14,9% a +15% | 5–6 |
| de +15,1% a +30% | 3–4 |
| acima de +30% | 1–2 |

Ajustes: −1 a −2 por tarifa restritiva, escalas longas ou horários ruins; +1 por bagagem ou flexibilidade incluída. Sem referência histórica, não dê nota: diga "nota impossível sem referência" e compare só com as alternativas atuais.

**Saída:** nota com a conta mostrada, 2 ou 3 alternativas atuais, sinais de alerta (tarifa básica disfarçada, agência desconhecida, preço sem taxas, conexão curta, reembolso em voucher) e taxas ocultas prováveis com fonte.

## Módulo 9. Decisão final: reserve agora, espere ou mude de plano

**Fatores:** preço atual versus típico; antecedência; sazonalidade e eventos; flexibilidade (reembolso, remarcação, cancelamento grátis do hotel); assentos restantes, quando a fonte mostrar; folga no orçamento; e mais:
- **Folga logística:** chegada versus check-in, check-out versus voo de volta, tempo de traslado (Google Maps ou similar) e encerramento do check-in da companhia (fonte oficial). Se estiver apertado, proponha ação concreta (sair mais cedo, late check-out, guardar malas).
- **Escassez por trecho:** se o voo bom de um trecho for o único barato do dia (ex.: único direto acessível na volta de feriado), esse trecho pede mais urgência.
- **Canal de compra:** onde está o menor preço confiável e o risco de cada canal.

**Lógica (heurística da skill):**
- **Reserve agora:** preço no típico ou abaixo e (alta temporada ou evento, ou viagem próxima, ou oferta com cancelamento grátis que trava o preço sem risco).
- **Espere:** preço acima do típico, viagem distante, sem evento, e a pessoa aceita monitorar. Defina preço-alvo e data-limite.
- **Mude de plano:** custo acima do orçamento sem alternativa viável, risco alto de conexão ou visto, ou alternativa claramente melhor encontrada nos outros módulos.

Oscilação esperada: só com base no que a fonte mostra; sem dado, diga que não há como prever.

**Saída:** veredito por trecho quando ida e volta forem passagens separadas, sempre dizendo onde comprar; justificativa em 3 a 5 tópicos; riscos e como reduzi-los; se "espere", preço-alvo, data-limite e o que monitorar.
