#!/usr/bin/env python3
"""
Gera a planilha Excel da cotação de viagem (skill consultor-de-viagens).

Uso:
    python gerar_planilha.py dados.json saida.xlsx [--fonte "Gothic A1"]

- Entrada: JSON no formato descrito em references/planilha-excel.md.
- Saída: .xlsx com 5 abas (Resumo, Comparação de datas, Fontes, Pagamento,
  Premissas e lacunas). Totais, hospedagem extra, diferenças e parcelas são
  FÓRMULAS que referenciam as premissas editáveis.
- Nunca sobrescreve: se o arquivo já existir, acrescenta _hhmm ao nome.
- Imprime no fim os totais por pessoa calculados em Python, para conferir
  com a resposta (o Excel recalcula as fórmulas ao abrir).

Requer: openpyxl.

Criado por LOM Consultoria e Projetos · contato@lomconsultoria.com
Licença CC BY-NC 4.0.
"""
import argparse
import datetime as dt
import json
import os
import sys

try:
    from openpyxl import Workbook
    from openpyxl.comments import Comment
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
except ImportError:  # pragma: no cover
    sys.exit("Erro: instale o openpyxl (pip install openpyxl).")

BRL = '"R$" #,##0.00'
AZUL = "0000FF"
VERDE = "008000"
LINK = "0563C1"
HDR = PatternFill("solid", fgColor="1F3864")
REC = PatternFill("solid", fgColor="E2EFDA")
INP = PatternFill("solid", fgColor="FFF2CC")
_thin = Side(style="thin", color="BFBFBF")
BORDA = Border(left=_thin, right=_thin, top=_thin, bottom=_thin)
CREDITO = "Gerado com a skill Consultor de Viagens — LOM Consultoria e Projetos — contato@lomconsultoria.com"
PERIGOSOS = ("=", "+", "-", "@")

FONTE = "Gothic A1"


def fnt(bold=False, color="000000", size=10, italic=False):
    return Font(name=FONTE, bold=bold, color=color, size=size, italic=italic)


def texto(cell, valor, **font_kw):
    """Grava texto vindo de fontes externas sem permitir que vire fórmula."""
    if valor is None:
        valor = ""
    valor = str(valor)
    cell.value = valor
    if valor.startswith(PERIGOSOS):
        cell.data_type = "s"
    cell.font = fnt(**font_kw)
    cell.alignment = Alignment(wrap_text=True, vertical="top")
    cell.border = BORDA
    return cell


def numero(cell, valor, fmt=BRL, entrada=True, bold=False):
    """Número de fonte (azul) ou 'lacuna' quando não há dado."""
    if isinstance(valor, (int, float)) and not isinstance(valor, bool):
        cell.value = valor
        cell.number_format = fmt
        cell.font = fnt(bold=bold, color=AZUL if entrada else "000000")
    else:
        cell.value = "lacuna" if valor in (None, "") else str(valor)
        if str(cell.value).startswith(PERIGOSOS):
            cell.data_type = "s"
        cell.font = fnt(bold=bold)
    cell.border = BORDA
    cell.alignment = Alignment(wrap_text=True, vertical="top")
    return cell


def formula(cell, f, fmt=BRL, bold=False, color="000000"):
    cell.value = f
    cell.number_format = fmt
    cell.font = fnt(bold=bold, color=color)
    cell.border = BORDA
    cell.alignment = Alignment(vertical="top")
    return cell


def link(cell, url):
    if isinstance(url, str) and url.lower().startswith(("http://", "https://")):
        cell.value = "abrir"
        cell.hyperlink = url
        cell.font = fnt(color=LINK)
    else:
        texto(cell, url or "—")
    cell.border = BORDA
    return cell


def cabecalho(ws, linha, colunas):
    for i, c in enumerate(colunas, 1):
        cell = ws.cell(row=linha, column=i, value=c)
        cell.font = fnt(True, "FFFFFF")
        cell.fill = HDR
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        cell.border = BORDA
    ws.row_dimensions[linha].height = 42


def larguras(ws, ws_larguras):
    for i, w in enumerate(ws_larguras, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


def caminho_livre(path):
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(path)
    cand = f"{base}_{dt.datetime.now():%H%M}{ext}"
    n = 2
    while os.path.exists(cand):
        cand = f"{base}_{dt.datetime.now():%H%M}_{n}{ext}"
        n += 1
    return cand


def validar(d):
    faltando = [k for k in ("titulo", "consulta", "recomendacao", "premissas", "opcoes") if k not in d]
    if faltando:
        sys.exit(f"Erro: JSON sem os campos obrigatórios: {', '.join(faltando)}")
    chaves = {p.get("chave") for p in d["premissas"]}
    for k in ("passageiros", "diaria_extra_grupo"):
        if k not in chaves:
            sys.exit(f"Erro: premissa obrigatória ausente: {k}")
    if not d["opcoes"]:
        sys.exit("Erro: 'opcoes' está vazio.")


def gerar(d, saida):
    validar(d)
    wb = Workbook()

    # ---------- Premissas e lacunas ----------
    pr = wb.active
    pr.title = "Premissas e lacunas"
    P = "'Premissas e lacunas'"
    pr["A1"] = "Premissas: as células amarelas são editáveis e as outras abas recalculam"
    pr["A1"].font = fnt(True, size=12)
    cabecalho(pr, 2, ["Premissa", "Valor", "Fonte / observação"])
    ref = {}
    for i, p in enumerate(d["premissas"], start=3):
        texto(pr.cell(row=i, column=1), p.get("rotulo", p["chave"]))
        c = pr.cell(row=i, column=2)
        numero(c, p.get("valor"), fmt=p.get("formato", BRL) if p["chave"] != "passageiros" else "0")
        c.fill = INP
        texto(pr.cell(row=i, column=3), p.get("fonte", ""))
        ref[p["chave"]] = f"{P}!$B${i}"
    lin = 3 + len(d["premissas"]) + 2
    pr.cell(row=lin, column=1, value="Lacunas e o que confirmar antes de pagar").font = fnt(True, size=12)
    cabecalho(pr, lin + 1, ["Item", "Situação", "Como conferir"])
    for i, l in enumerate(d.get("lacunas", []), start=lin + 2):
        texto(pr.cell(row=i, column=1), l.get("item"))
        texto(pr.cell(row=i, column=2), l.get("situacao"))
        como = l.get("como_conferir", "")
        if isinstance(como, str) and como.lower().startswith(("http://", "https://")):
            link(pr.cell(row=i, column=3), como)
        else:
            texto(pr.cell(row=i, column=3), como)
    larguras(pr, [46, 36, 80])

    # ---------- Comparação de datas ----------
    cd = wb.create_sheet("Comparação de datas", 0)
    C = "'Comparação de datas'"
    cd["A1"] = "Comparação de datas — valores POR PESSOA" + (" — " + d["observacao_bagagem"] if d.get("observacao_bagagem") else "")
    cd["A1"].font = fnt(True, size=12)
    cols = ["Opção", "Data da ida", "Partida", "Chegada", "Trecho", "Companhia", "Escalas", "Volta",
            "Ida por pessoa (PIX)", "Ida por pessoa (cartão)", "Volta por pessoa", "Noites extras",
            "Hospedagem extra por pessoa", "TOTAL por pessoa (PIX)", "TOTAL por pessoa (cartão)",
            "Total do grupo (PIX)", "Total do grupo (cartão)", "Diferença vs. recomendada (PIX, por pessoa)",
            "Diária máx. por pessoa para empatar", "Veredito"]
    cabecalho(cd, 3, cols)
    opcoes = sorted(d["opcoes"], key=lambda o: not o.get("recomendada", False))
    r0 = 4
    pax, diaria = ref["passageiros"], ref["diaria_extra_grupo"]
    totais_py = []
    for idx, o in enumerate(opcoes):
        r = r0 + idx
        for j, k in enumerate(["opcao", "ida_data", "partida", "chegada", "trecho", "companhia", "escalas", "volta"], 1):
            texto(cd.cell(row=r, column=j), o.get(k, ""), bold=(o.get("recomendada") and j == 1))
        numero(cd.cell(row=r, column=9), o.get("ida_pix_pp"))
        numero(cd.cell(row=r, column=10), o.get("ida_cartao_pp"))
        numero(cd.cell(row=r, column=11), o.get("volta_pp"))
        numero(cd.cell(row=r, column=12), o.get("noites_extras", 0), fmt="0")
        if o.get("fonte_ida"):
            cd.cell(row=r, column=9).comment = Comment(str(o["fonte_ida"]), "Cotação")
        if o.get("fonte_volta"):
            cd.cell(row=r, column=11).comment = Comment(str(o["fonte_volta"]), "Cotação")
        formula(cd.cell(row=r, column=13), f"=L{r}*{diaria}/{pax}")
        formula(cd.cell(row=r, column=14), f'=IFERROR(I{r}+K{r}+M{r},"lacuna")', bold=True)
        formula(cd.cell(row=r, column=15), f'=IFERROR(J{r}+K{r}+M{r},"lacuna")', bold=True)
        formula(cd.cell(row=r, column=16), f'=IFERROR(N{r}*{pax},"lacuna")')
        formula(cd.cell(row=r, column=17), f'=IFERROR(O{r}*{pax},"lacuna")')
        formula(cd.cell(row=r, column=18), f'=IFERROR(N{r}-$N${r0},"lacuna")')
        formula(cd.cell(row=r, column=19), f'=IF(L{r}=0,"—",IFERROR(($N${r0}-I{r}-K{r})/L{r},"lacuna"))')
        if o.get("recomendada"):
            texto(cd.cell(row=r, column=20), o.get("veredito", "Recomendada"), bold=True)
        else:
            extra = f'&IF(L{r}>0," (só vale se a noite custar até R$ "&TEXT(S{r},"0")&" por pessoa)","")'
            formula(cd.cell(row=r, column=20),
                    f'=IFERROR(IF(R{r}<0,"Vale a pena: economiza R$ "&TEXT(-R{r},"0"),'
                    f'"Não vale: R$ "&TEXT(R{r},"0")&" a mais por pessoa"{extra}),"lacuna")', fmt="General")
            cd.cell(row=r, column=20).alignment = Alignment(wrap_text=True, vertical="top")
        if o.get("recomendada"):
            for j in range(1, 21):
                cd.cell(row=r, column=j).fill = REC
        # conferência em Python
        try:
            pax_v = next(p["valor"] for p in d["premissas"] if p["chave"] == "passageiros")
            diaria_v = next(p["valor"] for p in d["premissas"] if p["chave"] == "diaria_extra_grupo")
            hosp = o.get("noites_extras", 0) * diaria_v / pax_v
            totais_py.append((o.get("opcao"), round(o["ida_pix_pp"] + o["volta_pp"] + hosp, 2),
                              round(o["ida_cartao_pp"] + o["volta_pp"] + hosp, 2)
                              if isinstance(o.get("ida_cartao_pp"), (int, float)) else "lacuna"))
        except (KeyError, TypeError, StopIteration, ZeroDivisionError):
            totais_py.append((o.get("opcao"), "lacuna", "lacuna"))
    fim = r0 + len(opcoes) - 1
    notas = [
        "Células azuis: valores coletados nas fontes (ver comentários). Células pretas: fórmulas.",
        "Hospedagem extra = noites extras × diária extra do grupo ÷ passageiros (aba 'Premissas e lacunas').",
        "'Diária máx. por pessoa para empatar': quanto cada noite extra pode custar por pessoa para a opção empatar com a recomendada.",
        f"Preços mudam a cada minuto: retrato de {d['consulta']}.",
    ]
    for i, n in enumerate(notas):
        cd.cell(row=fim + 2 + i, column=1, value=n).font = fnt(italic=True)
    larguras(cd, [26, 15, 8, 8, 24, 11, 22, 34, 13, 13, 12, 9, 13, 14, 14, 14, 14, 15, 14, 36])
    cd.freeze_panes = "B4"
    cd.auto_filter.ref = f"A3:T{fim}"

    # ---------- Fontes ----------
    fo = wb.create_sheet("Fontes")
    fo["A1"] = f"Comparativo de fontes — preço POR PESSOA ({d['consulta']})"
    fo["A1"].font = fnt(True, size=12)
    cabecalho(fo, 3, ["Trecho", "Voo", "Fonte", "Por pessoa (PIX / à vista)", "Por pessoa (cartão)",
                      "Parcelamento", "Tarifa e bagagem", "Reputação / observação", "Link", "Hora da consulta"])
    fontes = d.get("fontes", [])
    for i, f_ in enumerate(fontes, start=4):
        rec = f_.get("recomendada", False)
        texto(fo.cell(row=i, column=1), f_.get("trecho"), bold=rec)
        texto(fo.cell(row=i, column=2), f_.get("voo"), bold=rec)
        texto(fo.cell(row=i, column=3), f_.get("fonte"), bold=rec)
        numero(fo.cell(row=i, column=4), f_.get("pix_pp"), bold=rec)
        numero(fo.cell(row=i, column=5), f_.get("cartao_pp"), bold=rec)
        texto(fo.cell(row=i, column=6), f_.get("parcelamento", "lacuna"))
        texto(fo.cell(row=i, column=7), f_.get("tarifa", ""))
        texto(fo.cell(row=i, column=8), f_.get("reputacao", ""))
        link(fo.cell(row=i, column=9), f_.get("link"))
        texto(fo.cell(row=i, column=10), f_.get("hora", ""))
        if rec:
            for j in range(1, 11):
                fo.cell(row=i, column=j).fill = REC
    larguras(fo, [18, 40, 28, 15, 15, 36, 30, 34, 8, 12])
    fo.freeze_panes = "A4"
    if fontes:
        fo.auto_filter.ref = f"A3:J{3 + len(fontes)}"

    # ---------- Pagamento ----------
    pg = wb.create_sheet("Pagamento")
    pg["A1"] = "Condições de pagamento por canal"
    pg["A1"].font = fnt(True, size=12)
    cabecalho(pg, 3, ["Canal", "Desconto no PIX", "Parcelas sem juros", "Parcela mínima", "Juros", "Observações", "Fonte"])
    pag = d.get("pagamento", [])
    for i, p in enumerate(pag, start=4):
        for j, k in enumerate(["canal", "desconto_pix", "parcelas_sem_juros", "parcela_minima", "juros", "observacoes"], 1):
            texto(pg.cell(row=i, column=j), p.get(k, "lacuna"))
        link(pg.cell(row=i, column=7), p.get("link"))
    ls = 4 + len(pag) + 2
    pg.cell(row=ls, column=1, value="Simulação do pagamento da opção recomendada (grupo)").font = fnt(True, size=12)
    cabecalho(pg, ls + 1, ["Trecho", "Forma", "Total do grupo", "Nº de parcelas", "Valor da parcela (se sem juros)", "Observação"])
    colref = {"ida_pix": "I", "ida_cartao": "J", "volta": "K"}
    for i, s in enumerate(d.get("simulacao", []), start=ls + 2):
        texto(pg.cell(row=i, column=1), s.get("trecho"))
        texto(pg.cell(row=i, column=2), s.get("forma"))
        col = colref.get(s.get("base", ""), "I")
        formula(pg.cell(row=i, column=3), f"={C}!{col}{r0}*{pax}")
        c = numero(pg.cell(row=i, column=4), s.get("parcelas", 1), fmt="0")
        c.fill = INP
        formula(pg.cell(row=i, column=5), f"=C{i}/D{i}")
        texto(pg.cell(row=i, column=6), s.get("obs", ""))
    larguras(pg, [26, 30, 34, 14, 26, 50, 8])

    # ---------- Resumo ----------
    rs = wb.create_sheet("Resumo", 0)
    rs["A1"] = d["titulo"]
    rs["A1"].font = fnt(True, size=14)
    rs["A2"] = f"Cotação de {d['consulta']}. Preços mudam a cada minuto."
    rs["A2"].font = fnt(italic=True)
    rs["A4"] = "Recomendação"
    rs["A4"].font = fnt(True, size=12)
    lr = 5
    for t in d["recomendacao"]:
        c = rs.cell(row=lr, column=1)
        c.value = str(t)
        if str(t).startswith(PERIGOSOS):
            c.data_type = "s"
        c.font = fnt()
        lr += 1
    lr += 1
    cabecalho(rs, lr, ["Indicador", "Valor"])
    ind = [("Total por pessoa (PIX)", f"={C}!N{r0}"),
           ("Total por pessoa (cartão)", f"={C}!O{r0}"),
           ("Total do grupo (PIX)", f"={C}!P{r0}"),
           ("Total do grupo (cartão)", f"={C}!Q{r0}")]
    for k in range(1, len(opcoes)):
        ind.append((f"{opcoes[k].get('opcao')}: diferença por pessoa", f"={C}!R{r0 + k}"))
    for i, (k, v) in enumerate(ind, start=lr + 1):
        texto(rs.cell(row=i, column=1), k)
        formula(rs.cell(row=i, column=2), v, bold=True, color=VERDE)
    lr = lr + len(ind) + 2
    if d.get("riscos"):
        rs.cell(row=lr, column=1, value="Riscos").font = fnt(True, size=12)
        for i, t in enumerate(d["riscos"], start=lr + 1):
            c = rs.cell(row=i, column=1)
            c.value = "• " + str(t)
            c.font = fnt()
        lr = lr + len(d["riscos"]) + 2
    rs.cell(row=lr, column=1, value=CREDITO).font = fnt(italic=True, color="808080")
    larguras(rs, [70, 18])

    saida = caminho_livre(saida)
    os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)
    wb.save(saida)
    return saida, totais_py


def main():
    global FONTE
    ap = argparse.ArgumentParser(description="Gera a planilha da cotação de viagem.")
    ap.add_argument("dados", help="arquivo JSON de entrada")
    ap.add_argument("saida", help="caminho do .xlsx de saída")
    ap.add_argument("--fonte", default=FONTE, help="fonte das células (padrão: Gothic A1)")
    a = ap.parse_args()
    FONTE = a.fonte
    with open(a.dados, encoding="utf-8") as fh:
        d = json.load(fh)
    saida, totais = gerar(d, a.saida)
    print(f"Planilha salva em: {saida}")
    print("Conferência (por pessoa: PIX | cartão):")
    for nome, pix, cartao in totais:
        print(f"  - {nome}: {pix} | {cartao}")


if __name__ == "__main__":
    main()
