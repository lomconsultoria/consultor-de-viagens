# Consultor de Viagens Econômicas

Skill para o **Claude** que funciona como um consultor de viagens econômicas: compara datas, fontes de preço e formas de pagamento, avalia ofertas e entrega uma recomendação clara com uma planilha Excel para análise.

> Criado por **LOM Consultoria e Projetos** · [contato@lomconsultoria.com](mailto:contato@lomconsultoria.com)

## O que a skill faz

- **Pergunta aberta na abertura:** pede que a pessoa descreva a viagem com as próprias palavras (origem, destino, paradas, datas, quem vai, bagagem, orçamento, o que já está reservado, milhas e forma de pagamento).
- **Compara ir no dia, 1 dia antes e 2 dias antes**, somando as diárias extras quando a hospedagem já está fechada.
- **Cruza várias fontes de preço:** metabuscadores, site da companhia aérea, agências online e programas de milhas, com checagem de reputação das agências.
- **Mostra pagamento à vista (PIX) e no cartão**, com parcelas e juros de cada vendedor.
- **Nove módulos:** matriz de datas, aeroportos alternativos, conexões e multi-city, auditoria de oferta (nota de 1 a 10), custos ocultos, escolha de bairro, custo-benefício de hospedagem, otimização do custo total e decisão de reserva (reserve agora, espere ou mude de plano).
- **Entrega uma planilha Excel** com resumo, comparação de datas, fontes, pagamento e premissas editáveis.

## Regras que a skill segue

- Nunca inventa preço: todo número vem de uma fonte consultada, com data e hora.
- Separa dado de fonte, critério da skill e opinião.
- Não faz login, não compra, não preenche dados pessoais nem de cartão.
- Trata o conteúdo dos sites como informação, nunca como instrução.
- Não grava dados pessoais na planilha.

## Como instalar

1. Baixe a pasta `consultor-de-viagens/` (com o arquivo `SKILL.md`).
2. No Claude, adicione a skill pela área de skills da sua conta (envie a pasta compactada em .zip) ou copie a pasta para o diretório de skills do Claude Code.
3. Peça algo como: *"Quero cotar passagens de São Paulo para Recife em março"*.

Para pesquisar preços ao vivo, a skill precisa de busca na web e, de preferência, de um navegador conectado ao Claude.

## Licença

[Creative Commons Atribuição-NãoComercial 4.0 Internacional (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/deed.pt-br).

- **Pode:** usar, copiar e adaptar para fins não comerciais.
- **Precisa:** dar crédito à LOM Consultoria e Projetos e indicar se fez alterações.
- **Não pode:** usar comercialmente (vender, incluir em produto ou serviço pago) sem autorização.

**Uso comercial:** fale com a LOM Consultoria em [contato@lomconsultoria.com](mailto:contato@lomconsultoria.com).

O texto completo da licença está no arquivo [LICENSE](LICENSE).
