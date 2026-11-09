# Política de segurança

## Versões cobertas

| Versão | Recebe correções de segurança |
|---|---|
| 1.2.1 (atual) | Sim |
| 1.2 ou anterior | Não: atualize para a 1.2.1 |

## Como reportar

Encontrou uma vulnerabilidade na skill ou no script `gerar_planilha.py`? Escreva para **contato@lomconsultoria.com** com:

- o que acontece e como reproduzir (de preferência com o JSON de entrada);
- a ferramenta usada (Claude, Claude Code, Codex etc.) e a versão da skill;
- o impacto que você vê.

Não abra uma issue pública antes da correção. A LOM Consultoria responde em até 5 dias úteis e combina com você o prazo de correção e de divulgação.

## O que está no escopo

- Injeção de fórmula ou de links na planilha (Excel, Google Sheets, CSV).
- Falhas do script com dados vindos de sites (quebra, gravação fora da pasta, sobrescrita de arquivos).
- Instruções da skill que levem o assistente a comprar, fazer login, expor dados pessoais ou seguir instruções de sites.

## Teste automatizado

`python tests/teste_seguranca.py` roda a bateria de ataques ao script e sai com código 1 se encontrar problema. Rode antes de publicar qualquer mudança no script.

---
LOM Consultoria e Projetos · contato@lomconsultoria.com
