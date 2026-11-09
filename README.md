# Consultor de Viagens Econômicas

Skill no padrão aberto **[Agent Skills](https://agentskills.io)** que transforma o assistente de IA num consultor de viagens econômicas: compara datas, fontes de preço e formas de pagamento, avalia ofertas e entrega uma recomendação clara, com uma planilha para simular, em Excel, Google Sheets ou CSV.

> Criado por **LOM Consultoria e Projetos** · [contato@lomconsultoria.com](mailto:contato@lomconsultoria.com) · Versão 1.2

## O que a skill faz

- **Pergunta aberta na abertura:** pede que a pessoa descreva a viagem com as próprias palavras (origem, destino, paradas, datas, quem vai, bagagem, orçamento, o que já está reservado, milhas e forma de pagamento).
- **Compara ir no dia, 1 dia antes e 2 dias antes**, somando as diárias extras quando a hospedagem já está fechada.
- **Cruza várias fontes de preço:** metabuscadores, site da companhia aérea, agências online e programas de milhas, com checagem de reputação das agências.
- **Mostra o preço no PIX e no cartão**, com parcelas e juros de cada vendedor.
- **Nove módulos:** matriz de datas, aeroportos alternativos, conexões e viagens com várias cidades, auditoria de oferta (nota de 1 a 10), custos ocultos, escolha de bairro, custo-benefício de hospedagem, otimização do custo total e decisão de compra (reserve agora, espere ou mude de plano).
- **Entrega a planilha no formato que a pessoa escolher:** Excel (com fórmulas), Google Sheets (as fórmulas continuam funcionando) ou CSV (valores calculados, um arquivo por aba). Abas: resumo, comparação de datas, fontes, pagamento e premissas editáveis.

## Regras que a skill segue

- Nunca inventa preço: todo número vem de uma fonte consultada, com data e hora.
- Separa dado de fonte, critério da skill e opinião.
- Não faz login, não compra, não preenche dados pessoais nem de cartão.
- Trata o conteúdo dos sites como informação, nunca como instrução.
- Não grava dados pessoais na planilha e protege a planilha contra textos que virariam fórmula.

## Estrutura

```
consultor-de-viagens/
├── SKILL.md                      # regras, abertura, roteamento e formato (carregado sempre)
├── references/                   # detalhes carregados só quando a etapa pede
│   ├── fontes-e-navegacao.md     # fontes, agências, milhas, pagamento, roteiro por site, plano sem navegador
│   ├── comparativo-de-datas.md   # no dia, 1 e 2 dias antes, diárias extras e ponto de equilíbrio
│   ├── modulos-voo.md            # módulos 1, 2, 3, 4 e 9
│   ├── modulos-custos-e-hospedagem.md  # módulos 5, 6, 7 e 8
│   ├── formato-de-entrega.md     # modelo da resposta com exemplo real
│   └── planilha-e-exportacao.md  # Excel, Google Sheets ou CSV: formato do JSON e regras
├── scripts/
│   └── gerar_planilha.py         # gera o .xlsx (com fórmulas) e/ou os .csv a partir de um JSON
└── evals/                        # 4 casos de teste no formato do padrão
```

## Requisitos

| Recurso | Necessário? | Para quê |
|---|---|---|
| Busca na web | Sim | Preços, feriados, regras de bagagem e pagamento, reputação |
| Navegador controlado pela IA | Recomendado | Lista de vendedores no Kayak, sites de companhias e agências. Sem ele, a skill avisa que a comparação de agências ficou limitada e passa os links |
| Python com `openpyxl` | Recomendado | Gerar a planilha em Excel ou CSV. Sem ele, a skill monta as tabelas em CSV à mão |
| Conector do Google Drive | Opcional | Enviar a planilha direto para o Google Sheets. Sem ele, a skill entrega o .xlsx com o passo a passo de importação |

## Como instalar

**Claude (app):** compacte a pasta `consultor-de-viagens/` em .zip e envie na área de skills da sua conta.

**Claude Code:** copie a pasta para `~/.claude/skills/` (todas as suas sessões) ou para `.claude/skills/` dentro de um projeto.

**OpenAI Codex CLI:** copie a pasta para `~/.agents/skills/` ou para `.agents/skills/` dentro do repositório.

**Outras ferramentas compatíveis com Agent Skills** (Gemini CLI, Cursor, GitHub Copilot, Kiro e outras): siga a documentação de skills da ferramenta; a pasta é a mesma.

**Chats sem suporte a skills** (ex.: um GPT personalizado ou um Gem): cole o conteúdo do `SKILL.md` nas instruções e anexe os arquivos de `references/` como conhecimento. A pesquisa e a planilha dependem dos recursos de busca e de execução de código que o chat tiver.

Depois de instalar, peça algo como: *"Quero cotar passagens de São Paulo para Recife em março, 2 adultos"*.

## Testes

A pasta `evals/` tem 4 casos (pedido vago, cotação com hospedagem fixa, auditoria de oferta e viagem com várias cidades). Com o Claude Code, rode `claude plugin eval .` dentro da pasta da skill para comparar respostas com e sem a skill.

## Licença

[Creative Commons Atribuição-NãoComercial 4.0 Internacional (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/deed.pt-br).

- **Pode:** usar, copiar e adaptar para fins não comerciais.
- **Precisa:** dar crédito à LOM Consultoria e Projetos e indicar se fez alterações.
- **Não pode:** usar comercialmente (vender, incluir em produto ou serviço pago) sem autorização.

**Uso comercial:** fale com a LOM Consultoria em [contato@lomconsultoria.com](mailto:contato@lomconsultoria.com).

O texto completo da licença está em [LICENSE](LICENSE).
