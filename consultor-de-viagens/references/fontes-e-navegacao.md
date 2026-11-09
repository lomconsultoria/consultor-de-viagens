# Fontes, navegação e pagamento

Leia antes de coletar preços. Aqui estão: quais fontes consultar e por quê, como checar agências, milhas e pagamento, o roteiro de cada site e o que fazer sem navegador.

## Sumário
1. Protocolo multifonte
2. Agências: reputação e canal de compra
3. Milhas e pontos
4. Pagamento à vista e parcelado
5. Roteiro por site (navegador)
6. Sem navegador: plano B
7. Bloqueios e limites

---

## 1. Protocolo multifonte

Cada tipo de fonte mostra uma parte diferente do preço. O metabuscador acha datas e vendedores; o site da companhia tem as regras oficiais; a agência às vezes é mais barata; milhas podem virar o jogo em alta temporada. Por isso, para os 2 ou 3 melhores voos de cada trecho, consulte **pelo menos 4 tipos de fonte**:

| Tipo | Exemplos | Para quê |
|---|---|---|
| Metabuscadores | Google Flights, Kayak, Skyscanner, Momondo | Mapa de datas, faixa típica, lista de vendedores |
| Site da companhia | Azul, Gol, LATAM, companhia estrangeira | Preço oficial, tarifas com bagagem, regras de reembolso |
| Agências online | As que aparecem nos metabuscadores (ex.: Decolar, Vai de Promo) | Às vezes mais baratas; exigem checagem de reputação |
| Milhas | Smiles (Gol), LATAM Pass, programa da Azul | Podem sair bem mais baratas em alta temporada |
| Promoções | Páginas de promoção das companhias, benefícios do cartão | Cupons vigentes, sempre com validade |
| Hospedagem | Booking, Airbnb, Google Hotels, site do hotel | Preço total com taxas |

**Ordem de prioridade:** Google Flights só para mapear datas e candidatos. Para o preço final: Kayak (lista de vendedores) → site do vendedor recomendado (preço com taxas e pagamento) → site da companhia → milhas → Skyscanner para confirmar.

**Compare a mesma coisa:** mesmo voo, mesma bagagem, mesma regra de reembolso. Se uma fonte só vende tarifa diferente, diga qual.

**O site da companhia não é automaticamente o mais barato.** Exemplo (cotação de 09/11/2026): a Azul cobrava 24% a mais que agências pelo mesmo voo. O dado envelhece; compare sempre.

## 2. Agências: reputação e canal de compra

A agência mais barata pode custar caro se der problema na remarcação ou no reembolso. Antes de recomendar uma agência:
- Verifique a reputação no Reclame Aqui (nota e % de reclamações resolvidas).
- Veja quem emite o bilhete, como funcionam remarcação e reembolso, e se há taxa de serviço que só aparece no pagamento.
- **Reputação "Ruim" ou "Não recomendada" fica de fora**, mesmo sendo a mais barata. Indique a mais barata com reputação "Bom" ou melhor e mostre quanto custa a diferença por pessoa.
- Se a agência for menos de 5% mais barata que o site da companhia (heurística da skill), recomende comprar direto na companhia: resolver imprevistos direto com ela costuma ser mais simples.

## 3. Milhas e pontos

- Pergunte uma vez quais programas e saldos a pessoa tem.
- Custo equivalente = milhas × valor do milheiro ÷ 1.000 + taxas de embarque. Use o valor do milheiro que a pessoa informar ou o preço de compra de milhas do próprio programa (com fonte).
- Compare com o melhor preço em dinheiro e diga qual vale mais. Sem saldo informado, mostre o preço em pontos e o valor por mil pontos que tornaria a emissão vantajosa.

## 4. Pagamento à vista e parcelado

Para cada vendedor recomendado ou comparado, levante:
- preço à vista e desconto no PIX, se houver;
- número máximo de parcelas sem juros, parcela mínima e valor da parcela;
- se houver juros, a partir de quantas parcelas, a taxa e o total final;
- observações (ex.: taxa de embarque cobrada inteira na 1ª parcela).

Fontes: a página de resultados do vendedor, a página de formas de pagamento ou o regulamento, sempre com data. Os metabuscadores não mostram parcelamento; o preço deles é tratado como à vista até confirmar. Algumas agências exibem no metabuscador o preço já com desconto do PIX: confira.

Não preencha dados de passageiro nem de cartão para ver condições. Se elas só aparecem no pagamento, registre "parcelamento: só no checkout" como lacuna. Preço no cartão calculado a partir do desconto do PIX é inferência: marque como "inferido".

Diga qual forma vale mais e marque como análise: parcelado sem juros pelo mesmo preço costuma ser melhor que à vista sem desconto; com desconto no PIX, compare o desconto com o benefício de parcelar.

## 5. Roteiro por site (navegador)

As URLs abaixo funcionavam em novembro de 2026. Se uma não carregar o resultado certo (data errada, página não encontrada), use o formulário do site. Recuse cookies não essenciais. Feche as abas ao terminar.

**Google Flights**
- Veja primeiro "Preços monitorados" na página inicial: se a pessoa já monitora a rota, aquele voo é a oferta candidata para auditoria, e o gráfico de histórico dele é a melhor fonte de tendência.
- A URL com `?q=` não dispara a busca de forma confiável: preencha o formulário (datas como dd/mm/aaaa).
- Use o destino no nível da cidade (ex.: "Rio de Janeiro" cobre GIG e SDU).
- "Calendário" em ida e volta = matriz ida × volta; em só ida = preço por dia.
- Leia a aba "Menores preços" além de "Melhor opção".
- Os preços exibidos são o total do grupo: divida pelo número de passageiros.
- O painel "Os preços estão altos/típicos/baixos" traz a faixa típica; expanda para ler os valores.

**Kayak** (melhor fonte isolada)
- `https://www.kayak.com.br/flights/ORIG-DEST/AAAA-MM-DD/Nadults?sort=price_a` (código de cidade, ex.: RIO).
- Clique em "Selecionar" no voo: abre a lista de vendedores com preço por pessoa e total, o preço direto da companhia e as famílias tarifárias.

**Skyscanner** (confirmação)
- `https://www.skyscanner.com.br/transporte/passagens-aereas/orig/dest/AAMMDD/?adultsv2=N&cabinclass=economy&rtn=0` (Rio: `rioa`).

**Azul** (preço oficial e pontos)
- `https://www.voeazul.com.br/br/pt/home/selecao-voo?c[0].ds=ORIG&c[0].std=MM/DD/AAAA&c[0].as=DEST&p[0].t=ADT&p[0].c=N&p[0].cp=false&f.dl=3&f.dr=3&cc=BRL`
- O botão "Pontos" mostra o preço em pontos sem login. "Ver mais voos" carrega o resto da lista.

**Vai de Promo** (agência)
- `https://www.vaidepromo.com.br/passagens-aereas/pesquisa/ORIGDESTAAMMDD/N/0/0/Y/` (ex.: `POARIO270205/4/0/0/Y/`).
- O resultado mostra o preço no PIX com taxa de embarque, taxa de serviço e desconto; o preço no cartão não aparece antes do pagamento.

**Smiles**
- Costuma travar com navegação automatizada. Tente uma vez; se travar, marque como bloqueado e passe o link.

**Reclame Aqui**
- Abra pelo navegador (a leitura direta pela web costuma ser bloqueada) e registre a reputação e o % de reclamações resolvidas.

## 6. Sem navegador: plano B

Algumas ferramentas só têm busca na web, e os testes mostraram que, sem navegador, as páginas de busca por data (Kayak, Skyscanner, Azul, agências) costumam ser recusadas. Na prática, quase sempre faltará o preço exato das datas. Nesse caso:
- **Avise no topo da resposta** que não foi possível cotar as datas exatas e por quê.
- **Use o que a busca alcança:** páginas de rota sem data (faixa típica e mês mais caro no Kayak, Momondo, Skyscanner), promoções publicadas, regras de bagagem e pagamento, reputação de agências.
- **Entregue a regra de decisão em reais**, que vale mesmo sem preço: "ir 1 dia antes só compensa se a passagem sair mais de R$ X por pessoa mais barata que no dia" (X = hospedagem extra por pessoa). Diga também até quanto o preço está dentro da faixa típica.
- **Monte os links prontos** (seção 5) para a pessoa conferir cada data e fonte, já com o número de passageiros.
- Na tabela e na planilha, preço que você não viu é "lacuna". A planilha calcula sozinha quando a pessoa digitar os preços.

## 7. Bloqueios e limites

- Site que bloqueia a automação: tente uma vez, registre como "bloqueado" e siga com as outras fontes. Liste no fim o que a pessoa precisa conferir, com link.
- Nunca: login, criação de conta, CAPTCHA, "Comprar"/"Reservar"/"Continuar" para pagamento, aceite de termos, CPF, e-mail ou telefone.
- Anúncios e patrocinados ("Anúncio", "Patrocinado", "Sponsored") não são fonte; não siga links deles.
