# Módulos de custos e hospedagem

Leia o módulo indicado pela tabela de roteamento do SKILL.md. Em pedidos sem cotação de voo (ex.: só bairros ou só hospedagem), a resposta usa a saída do módulo, mantendo as regras de clareza do SKILL.md.

## Sumário
- Módulo 5. Custos ocultos
- Módulo 6. Escolha de bairro
- Módulo 7. Custo-benefício da hospedagem
- Módulo 8. Otimização do custo total

---

## Módulo 5. Custos ocultos

**Entrada:** voos e hospedagens da pessoa. Cada valor com fonte.

- **Aéreo:** assento, bagagem despachada (por trecho e pessoa), bagagem de mão em low-cost, check-in no aeroporto, alterações, pagamento com cartão.
- **Hospedagem:** taxa de resort ou destino, limpeza, taxa de serviço, impostos não incluídos, caução, estacionamento, café da manhã, check-in tardio.
- **Destino:** taxa turística municipal (por pessoa e noite, com limite de noites), autorização eletrônica de entrada, seguro viagem obrigatório.
- **Traslados:** aeroporto ↔ hospedagem (transporte público, aplicativo, táxi oficial) e se há transporte no horário de chegada.
- **Financeiro (viagem internacional):** IOF vigente no cartão (verifique a alíquota atual), spread de câmbio, saque no exterior. Mostre em BRL e na moeda original, citando a cotação usada.

**Saída:** item, tipo de custo, valor unitário, quantidade, total em BRL, fonte e status (confirmado, provável, lacuna); custo real total versus anunciado, com a diferença em %.

## Módulo 6. Escolha de bairro

**Entrada:** destino, estilo de viagem, orçamento por noite.

1. Levante bairros candidatos em fontes recentes (guias, prefeitura, fóruns) e dados de segurança quando existirem (estatística oficial, alerta consular). Não rotule um bairro como "seguro" ou "perigoso" sem fonte: rótulo sem base pode levar a pessoa a uma decisão ruim.
2. Transporte: distância a pé até metrô ou trem, tempo até as atrações e até o aeroporto.
3. Oferta real no orçamento (amostra em Booking ou Airbnb para as datas).
4. Critérios por estilo: trabalho remoto (cafés, coworking, internet, silêncio); família (parques, mercado, farmácia, ruído, acessibilidade); casal ou lazer (gastronomia, vida noturna).

**Saída:** top 3 com segurança (com fonte), transporte, serviços a pé, preço médio, prós e contras; recomendação do 1º e para quem os outros fazem mais sentido.

## Módulo 7. Custo-benefício da hospedagem

**Entrada:** destino, datas, número de hóspedes, necessidades (cozinha, quartos, trabalho).

1. Amostre as melhores opções de cada tipo: hotel, aluguel por temporada, hostel (quarto privativo e dormitório quando fizer sentido), apart-hotel.
2. Valor total a pagar = diárias + limpeza + taxa de serviço + impostos + taxa turística + café ou estacionamento, se necessário.
3. Economia com cozinha: só quando a pessoa pretende cozinhar, com preços de mercado e refeição local com fonte, ou como premissa declarada.
4. Compare cancelamento e localização (use o bairro do módulo 6, se feito).

**Saída:** tipo, opção, total da estadia, total por noite, cancelamento, localização, cozinha e observações; recomendação com o porquê.

## Módulo 8. Otimização do custo total

**Entrada:** roteiro completo.

1. Linha de base: custo atual por categoria (aéreo, hospedagem, traslados, transporte local, passeios, alimentação, seguro, taxas).
2. As 3 maiores alavancas, normalmente as categorias de maior peso.
3. Para cada uma, uma alternativa concreta pesquisada, com preço e economia em %.
4. Confirme que a alternativa não piora a segurança (bairro, horário de chegada, conexão arriscada) nem o conforto relevante; se piorar, diga.
5. Meta de 20% por área: se não der sem comprometer segurança ou conforto, diga claramente e mostre a melhor economia real. Forçar o número levaria a uma recomendação pior.

**Saída:** área, custo atual, alternativa, novo custo, economia em R$ e %, impacto em conforto e segurança; total economizado e novo custo total.
