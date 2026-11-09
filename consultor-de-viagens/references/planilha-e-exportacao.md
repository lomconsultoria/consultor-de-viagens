# Planilha: Excel, Google Sheets ou CSV

A planilha deixa a pessoa simular (outra diária, outro número de pessoas, outra quantidade de parcelas) sem pedir uma nova cotação. Por isso, no Excel e no Google Sheets, os totais são fórmulas e as premissas ficam em células editáveis.

## Qual formato usar

| Formato | Quando | Fórmulas editáveis? | Como gerar |
|---|---|---|---|
| **Excel (.xlsx)** | Padrão, quando a pessoa não pede outro | Sim | `--formato xlsx` (padrão) |
| **Google Sheets** | A pessoa usa Google Drive ou quer compartilhar a planilha | Sim (o Google converte as fórmulas do .xlsx) | Gerar o .xlsx e enviar ao Drive convertendo (abaixo) |
| **CSV** | A pessoa vai importar em outro sistema ou não tem Excel | Não: valores já calculados | `--formato csv` (um arquivo por aba) |

Pergunte o formato na abertura; sem resposta, use Excel. Pode gerar mais de um (`--formato todos` gera Excel e CSV).

### Google Sheets
1. Gere o `.xlsx` com o script.
2. **Com conector do Google Drive:** envie o arquivo pedindo conversão para Planilhas Google (no Drive, o tipo de destino é `application/vnd.google-apps.spreadsheet`; muitos conectores convertem por padrão ao enviar um .xlsx). Depois, confira em uma célula de total que a fórmula foi mantida. O arquivo fica privado, só para a pessoa: não compartilhe com ninguém sem ela pedir.
3. **Sem conector:** entregue o `.xlsx` e o passo a passo: no Google Drive, "Novo" → "Upload de arquivo" → abrir com "Planilhas Google"; ou, numa planilha nova, "Arquivo" → "Importar".
4. A fonte Gothic A1 existe no Google Sheets (menu de fontes → "Mais fontes"); se não aparecer, o Sheets usa a padrão.

### CSV
- Um arquivo por aba, em uma pasta `<nome>_csv/`: `1-resumo.csv`, `2-comparacao-de-datas.csv`, `3-fontes.csv`, `4-pagamento.csv`, `5-premissas-e-lacunas.csv`.
- Padrão para o Excel em português: separador `;`, decimal `,` e codificação UTF-8 com BOM (acentos aparecem certos). Para outro sistema, use `--separador ","` e `--decimal "."`.
- Valores já calculados, porque CSV não guarda fórmulas. Diga isso à pessoa.
- Texto que começa com `=`, `+`, `-` ou `@` ganha um apóstrofo na frente, para não virar fórmula ao abrir. Links que não sejam `http(s)` viram "—".

## Como gerar

1. Monte um JSON no formato abaixo com os dados da cotação.
2. Rode: `python scripts/gerar_planilha.py dados.json "Viagem_ORIG-DEST_dd-mm-aaaa_cotacao_aaaa-mm-dd.xlsx" --formato xlsx|csv|todos`
   - Opcional: `--fonte "Arial"` para trocar a fonte (padrão: Gothic A1, identidade da LOM).
3. O script nunca sobrescreve: se o arquivo existir, acrescenta a hora ao nome.
4. O script imprime os totais por pessoa calculados em Python. **Confira com os da resposta** antes de entregar. Se houver LibreOffice, recalcule as fórmulas para os valores aparecerem também em visualizadores que não calculam.
5. Salve na pasta do projeto da pessoa e diga onde ficou. Sem pasta, envie o arquivo na conversa. Sem Python, monte os CSV à mão com as mesmas colunas e avise.

## Abas geradas (as mesmas no Excel, no Google Sheets e nos CSV)
1. **Resumo:** recomendação, totais por pessoa e do grupo (PIX e cartão), diferença de cada alternativa, riscos e crédito.
2. **Comparação de datas:** uma linha por opção, com voos, preços coletados (azul), hospedagem extra, totais, diferença, diária de equilíbrio e veredito (fórmulas).
3. **Fontes:** trecho, voo, fonte, PIX e cartão por pessoa, parcelamento, tarifa e bagagem, reputação, link e hora.
4. **Pagamento:** condições por canal e simulação de parcelas (nº de parcelas editável).
5. **Premissas e lacunas:** premissas editáveis (amarelo) e o que falta confirmar.

## Formato do JSON

```json
{
  "titulo": "POA → Rio de Janeiro — Carnaval 2027 — 4 adultos",
  "consulta": "09/11/2026, 10h40–11h25",
  "observacao_bagagem": "sem mala despachada",
  "recomendacao": [
    "Ida: sex 05/02/2027, Azul 14:00 POA → 18:25 SDU, 1 parada, na Vai de Promo (PIX).",
    "Volta: qua 10/02/2027, Gol 12:25 GIG → 14:35 POA, direto, no site da Gol (3x sem juros)."
  ],
  "riscos": ["Tarifas sem mala e sem reembolso."],
  "premissas": [
    {"chave": "passageiros", "rotulo": "Número de passageiros", "valor": 4, "fonte": "Reserva: 4 hóspedes"},
    {"chave": "diaria_extra_grupo", "rotulo": "Diária extra do grupo (R$/noite)", "valor": 792, "fonte": "Contrato: R$ 3.960 ÷ 5 noites"},
    {"chave": "diaria_mercado_grupo", "rotulo": "Diária de mercado (R$/noite)", "valor": 477, "fonte": "Google Hotels, amostra"}
  ],
  "opcoes": [
    {"opcao": "No dia (recomendada)", "recomendada": true, "ida_data": "sex 05/02/2027",
     "partida": "14:00", "chegada": "18:25", "trecho": "POA → SDU", "companhia": "Azul",
     "escalas": "1 parada (Campinas)", "volta": "qua 10/02, 12:25 GIG → 14:35 POA, direto, Gol",
     "ida_pix_pp": 818.66, "ida_cartao_pp": 860.41, "volta_pp": 817, "noites_extras": 0,
     "fonte_ida": "Vai de Promo, 09/11 11h20: R$ 3.274,63 PIX ÷ 4", "fonte_volta": "Site da Gol via Kayak"}
  ],
  "fontes": [
    {"trecho": "Ida no dia", "voo": "sex 05/02, 14:00 POA → 18:25 SDU", "fonte": "Vai de Promo",
     "pix_pp": 818.66, "cartao_pp": 860.41, "parcelamento": "Só no checkout",
     "tarifa": "Mala de mão 10 kg", "reputacao": "RA1000", "link": "https://www.vaidepromo.com.br/...",
     "hora": "11h20", "recomendada": true}
  ],
  "pagamento": [
    {"canal": "Site da Gol", "desconto_pix": "Não", "parcelas_sem_juros": "3x", "parcela_minima": "R$ 100",
     "juros": "4x–12x com acréscimo", "observacoes": "Taxa de embarque na 1ª parcela", "link": "https://www.voegol.com.br/informacoes/formas-de-pagamento"}
  ],
  "simulacao": [
    {"trecho": "Volta (Gol)", "forma": "Cartão 3x sem juros", "base": "volta", "parcelas": 3, "obs": "1ª parcela maior"}
  ],
  "lacunas": [
    {"item": "Smiles", "situacao": "Bloqueado", "como_conferir": "https://www.smiles.com.br"}
  ]
}
```

- Obrigatórios: `titulo`, `consulta`, `recomendacao`, `premissas` (com `passageiros`) e `opcoes`.
- `diaria_extra_grupo` só quando há hospedagem fixa e noites extras para comparar. Sem ela, o script cria a premissa vazia ("lacuna", com a observação "não se aplica") e as opções sem noites extras calculam normalmente. Não grave 0 para preencher.
- **Várias cidades:** em vez de `ida_*` e `volta_pp`, use `opcoes[].trechos`, uma lista na ordem da viagem: `{"rota": "CWB→SCL", "data": "sáb 10/04", "horario": "08:00", "companhia": "LATAM", "pix_pp": 900, "cartao_pp": 950, "fonte": "Kayak"}`. O script soma todos os trechos nas colunas de ida (PIX e cartão), deixa a volta em 0 e põe o preço de cada trecho no comentário da célula. Trecho sem preço (`null`) deixa o total como "lacuna". Inclua a linha do bilhete multi-city, com `pix_pp: null` se não foi possível cotar.
- `opcoes`: a recomendada primeiro (o script reordena se `recomendada: true`). Valores por pessoa como número; sem dado, `null` (vira "lacuna").
- `simulacao.base`: `ida_pix`, `ida_cartao` ou `volta` (da opção recomendada).
- `opcoes[].veredito` (opcional): texto que substitui o veredito automático. Use quando o preço sozinho não decide, por exemplo uma opção mais barata mas com horas a mais de viagem ou chegada de madrugada. Sem ele, a planilha calcula o veredito só pelo preço.

## Regras do arquivo (já aplicadas pelo script)
- Totais, hospedagem extra, diferenças e parcelas são fórmulas ligadas às premissas.
- Moeda no formato `"R$" #,##0.00` (o Excel exibe vírgula e ponto conforme o idioma). Sem dado: "lacuna", nunca zero.
- Texto vindo de sites que comece com `=`, `+`, `-` ou `@` é gravado como texto, para não virar fórmula.
- Links só `http(s)` dos vendedores consultados ou montados pela pesquisa; nunca de anúncios ou do texto de páginas.
- Sem dados pessoais: nada de nomes, CPF, endereço, e-mail ou telefone; hóspedes só como número.
- Rodapé do Resumo com o crédito da LOM Consultoria.
