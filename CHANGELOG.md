# Histórico de versões

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
