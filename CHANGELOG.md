# Histórico de versões

## 1.3.0 — novembro de 2026 (velocidade e cruzeiros)
Motivo: numa cotação real de cruzeiro (Santos → Salvador, abril de 2027), a pesquisa levou 2h22 sem notícias; cerca de 25 de ~60 chamadas foram em sites que falhavam ou em tentativas repetidas.
- **Status a cada 5 minutos (obrigatório):** mensagem de até 3 linhas com o que está confirmado, o que está em andamento e a previsão de entrega.
- **Orçamento de tempo:** até 15 min para um item, até 30 min para a cotação completa; ao estourar, entrega o que tem com as lacunas. Achado que muda o pedido sai na hora.
- **Teto de 3 fontes por item** (1 oficial + 1 metabuscador/agência + 1 confirmação); pesquisa exaustiva só se a pessoa pedir.
- **Regra das 2 falhas:** site que falha 2 vezes vira lacuna com link.
- **Módulo de cruzeiros:** temporada primeiro (Brasil: novembro a abril), trechos só de ida no fim e no início da temporada, preço por tipo de cabine e conta porta a porta.
- **Atalhos testados:** URLs que funcionaram (Kayak com vários aeroportos, Booking com filtro de nota, MSC, CVC cruzeiros, Cruzeiros Travel, DeÔnibus) e sites a evitar (Decolar para cruzeiros, site da Costa na automação, WebFetch em páginas que dependem de JavaScript).
- **Planilha:** aba "Detalhamento por item" (campo `item` nos trechos) e CSV `6-detalhamento-por-item.csv`.
- **Corrigido:** "Diária máx. para empatar" mostrava valor sem sentido (ex.: −R$ 125) quando a opção tinha hotel no destino ou outro voo de volta; agora mostra "não se aplica".
- **Corrigido:** cabeçalho do CSV não protegia rótulos vindos do JSON contra injeção de fórmula (achado pelo teste de segurança ao incluir o campo `item`).

## 1.2.2 — novembro de 2026 (segurança)
- **Teste de comportamento** em `tests/comportamento/`: 4 cenários de sites mal-intencionados (injeção de recomendação, pressão de compra com script, "regulamento" executável e pedido de CPF), mapeados no OWASP Top 10 para IA 2025. Versões 1.2.1 e 1.0: todas resistiram, 0 armadilhas disparadas.
- **Regra 12 mais clara:** a tentativa de manipulação é relatada de forma visível (aviso do topo ou Parte 3) e vira sinal de alerta sobre o vendedor. No teste, uma execução tinha relatado só nas lacunas.
- **Corrigido:** veredito mostrava "R$ lacuna" quando faltava a diária; agora pede "Preencher preços e a diária extra".
- README com a tabela de alinhamento à OWASP.
- README com a seção "Quanto custa usar": consumo medido por cotação, onde ver os tokens em cada ferramenta e como gastar menos.

## 1.2.1 — novembro de 2026 (segurança)
Teste de segurança com dados maliciosos (`tests/teste_seguranca.py`): a 1.2 tinha 7 tipos de falha (394 ocorrências somando os cenários); a 1.2.1 passa sem nenhuma.
- **Corrigido:** o título da cotação podia virar fórmula no Excel e no Google Sheets (ex.: `=HYPERLINK` para vazar dados). Agora uma varredura final deixa como fórmula só o que o script criou.
- **Corrigido:** o formato de número das premissas era livre e podia exibir um valor falso. Agora só formatos da lista do script.
- **Corrigido:** CSV não protegia textos começando com tabulação ou quebra de linha.
- **Corrigido:** caracteres de controle vindos de sites quebravam a geração; texto no lugar de número também. Agora são limpos ou viram "lacuna".
- **Novo:** links mostram o domínio de destino; `javascript:`, `file:`, `data:` e caminhos de rede são descartados.
- **Novo:** validação de passageiros (1 a 99), caminho de saída sem `..`, sem seguir atalho (symlink) pendente, extensão `.xlsx` garantida.
- **Novo:** a skill não baixa nem abre arquivos de sites; o nome do arquivo usa só códigos, datas e caracteres seguros.
- Alinhado ao guia de testes da OWASP (WSTG-INPV-21): proteção também para `＋`, `－` e `＠` de largura total e teste de fuga da célula com separador e aspas.
- README com a seção Segurança (o que o aviso "executa código" significa, proteções, riscos que continuam) e `SECURITY.md` para reportar vulnerabilidades.

## 1.2 — novembro de 2026
- **Três formatos de planilha:** Excel (padrão, com fórmulas), Google Sheets (envio ao Drive convertendo o .xlsx, fórmulas preservadas) e CSV (um arquivo por aba, valores calculados, `;` e vírgula decimal para o Excel em português).
- A pergunta de abertura passa a perguntar o formato da planilha.
- CSV protegido contra injeção de fórmula (apóstrofo antes de `=`, `+`, `-`, `@`) e com links só `http(s)`.
- **Várias cidades na planilha:** campo `trechos` soma os trechos de cada opção e mostra o preço de cada um; a resposta compara trechos separados com o bilhete multi-city numa linha própria, mesmo quando o preço do multi-city fica como lacuna.
- **Sem hospedagem fixa:** a diária extra deixou de ser obrigatória; não é mais preciso gravar 0 para o script rodar.
- **Veredito escrito pelo consultor** (`opcoes[].veredito`) para quando o preço sozinho não decide.
- Veredito sem preço mostra o limite em reais ("só compensa se a passagem sair mais de R$ X por pessoa mais barata") em vez de erro; simulação de parcelas sem `#VALUE!`.
- Critérios de avaliação nos 4 casos de teste de `evals/`, com rodada de testes comparando a 1.0 e a 1.2.

## 1.1 — novembro de 2026
- **Portável entre ferramentas:** segue o padrão aberto Agent Skills e passa no validador oficial (`skills-ref`). Novo campo `compatibility` no cabeçalho com o que a skill precisa.
- **Mais leve:** o `SKILL.md` caiu de 420 para 120 linhas (de cerca de 39 mil para 10,5 mil caracteres). Os detalhes foram para `references/` e são lidos só quando a etapa pede.
- **Script da planilha:** `scripts/gerar_planilha.py` gera o Excel a partir de um JSON, com fórmulas, proteção contra texto que viraria fórmula, links só `http(s)`, sem sobrescrever arquivos e com conferência dos totais. Substitui a dependência de uma skill exclusiva do Claude.
- **Plano B sem navegador:** a skill avisa quando a comparação de agências ficou limitada e passa os links para conferir.
- **Descrição reescrita** para a skill ser acionada nos pedidos certos, mesmo sem a palavra "consultor".
- **Regras explicadas:** cada regra traz o motivo, para o assistente aplicá-la em casos não previstos.
- **Exemplo real** de resposta no `formato-de-entrega.md`.
- **Casos de teste** em `evals/`.
- Roteiro da Vai de Promo incluído nas fontes.

## 1.0 — novembro de 2026
- Primeira versão pública.
- Pergunta aberta na abertura e suporte a viagens com várias cidades.
- Comparação obrigatória: no dia, 1 dia antes e 2 dias antes, com diárias extras.
- Protocolo multifonte (metabuscadores, companhia aérea, agências, milhas) com checagem de reputação.
- Preço à vista (PIX) e no cartão, com condições de parcelamento.
- Formato de resposta em 3 partes e planilha Excel com fórmulas.
- Regras de segurança: conteúdo de sites não é instrução, limites de navegação, sem dados pessoais.
