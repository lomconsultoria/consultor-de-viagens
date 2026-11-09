#!/usr/bin/env python3
"""
Gera a planilha Excel da cotação de viagem (skill consultor-de-viagens).

Uso:
    python gerar_planilha.py dados.json saida.xlsx [--fonte "Gothic A1"]

- Entrada: JSON no formato descrito em references/planilha-e-exportacao.md.
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
import math
import os
import re
import sys
from urllib.parse import urlparse

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
# Caracteres que fazem Excel, LibreOffice ou Google Sheets tratar o texto como fórmula
# (OWASP WSTG-INPV-21: =, +, -, @, tabulação, CR, LF e as variantes de largura total)
PERIGOSOS = ("=", "+", "-", "@", "\t", "\r", "\n", "\uff1d", "\uff0b", "\uff0d", "\uff20")
# Caracteres de controle que corrompem o .xlsx (o openpyxl recusa) ou escondem conteúdo
_CONTROLE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
LIMITE_TEXTO = 32000  # o Excel aceita até 32.767 caracteres por célula
# Formatos de número aceitos nas premissas (um formato livre poderia exibir um valor falso)
FORMATOS = {'"R$" #,##0.00', "0", "0.00", "0%", "0.0%", "General"}
_FORMULAS = set()  # células criadas pela função formula(); todas as outras ficam como texto

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
    _FORMULAS.add((cell.parent.title, cell.coordinate))
    cell.value = f
    cell.number_format = fmt
    cell.font = fnt(bold=bold, color=color)
    cell.border = BORDA
    cell.alignment = Alignment(vertical="top")
    return cell


def _host(url):
    """Domínio de um link http(s) válido; None para qualquer outro esquema."""
    if not isinstance(url, str) or not url.lower().startswith(("http://", "https://")):
        return None
    try:
        h = urlparse(url).hostname
    except ValueError:
        return None
    return h or None


def link(cell, url):
    host = _host(url)
    if host:
        # Mostra o domínio de destino, para a pessoa ver para onde o link leva antes de clicar
        cell.value = host
        cell.hyperlink = url
        cell.font = fnt(color=LINK)
    else:
        # Esquemas como javascript:, file: ou \\servidor não viram link nem ficam visíveis como texto
        texto(cell, "—" if not url or (isinstance(url, str) and _ESQUEMAS_RUINS.search(url)) else url)
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


def checar_saida(path, ext=None):
    """Recusa caminhos com '..' ou caracteres de controle e garante a extensão."""
    if _CONTROLE.search(path) or "\n" in path or "\r" in path:
        sys.exit("Erro: o caminho de saída tem caracteres inválidos.")
    if ".." in re.split(r"[\\/]", path):
        sys.exit("Erro: o caminho de saída não pode subir pastas com '..'.")
    if ext and not path.lower().endswith(ext):
        path += ext
    return path


def caminho_livre(path):
    if not os.path.lexists(path):
        return path
    base, ext = os.path.splitext(path)
    cand = f"{base}_{dt.datetime.now():%H%M}{ext}"
    n = 2
    while os.path.lexists(cand):
        cand = f"{base}_{dt.datetime.now():%H%M}_{n}{ext}"
        n += 1
    return cand


def validar(d):
    faltando = [k for k in ("titulo", "consulta", "recomendacao", "premissas", "opcoes") if k not in d]
    if faltando:
        sys.exit(f"Erro: JSON sem os campos obrigatórios: {', '.join(faltando)}")
    if isinstance(d.get("recomendacao"), str):
        d["recomendacao"] = [d["recomendacao"]]
    if isinstance(d.get("riscos"), str):
        d["riscos"] = [d["riscos"]]
    for k in ("recomendacao", "premissas", "opcoes", "riscos", "fontes", "pagamento", "simulacao", "lacunas"):
        if k in d and not isinstance(d[k], list):
            sys.exit(f"Erro: '{k}' precisa ser uma lista.")
    for k in ("premissas", "opcoes", "fontes", "pagamento", "simulacao", "lacunas"):
        if any(not isinstance(x, dict) for x in d.get(k, [])):
            sys.exit(f"Erro: cada item de '{k}' precisa ser um objeto.")
    if any(not isinstance(p.get("chave"), str) for p in d["premissas"]):
        sys.exit("Erro: toda premissa precisa de 'chave'.")
    pax = next((p.get("valor") for p in d["premissas"] if p["chave"] == "passageiros"), None)
    if pax is None:
        sys.exit("Erro: premissa obrigatória ausente: passageiros")
    if not (isinstance(pax, int) and not isinstance(pax, bool) and 1 <= pax <= 99):
        sys.exit("Erro: 'passageiros' precisa ser um número inteiro entre 1 e 99.")
    if not d["opcoes"]:
        sys.exit("Erro: 'opcoes' está vazio.")
    normalizar(d)


def _soma(vals):
    return round(sum(vals), 2) if vals and all(_num(v) for v in vals) else None


def _limpar(x):
    """Limpa em profundidade o que veio de sites: tira caracteres de controle, corta textos
    longos demais e troca números não finitos (NaN, infinito) por vazio ("lacuna")."""
    if isinstance(x, dict):
        for k in list(x):
            x[k] = _limpar(x[k])
    elif isinstance(x, list):
        for i, v in enumerate(x):
            x[i] = _limpar(v)
    elif isinstance(x, str):
        return _CONTROLE.sub("", x)[:LIMITE_TEXTO]
    elif isinstance(x, float) and not math.isfinite(x):
        return None
    return x


def normalizar(d):
    """Prepara o JSON para os cálculos, sem inventar valores.

    - Sem hospedagem fixa, 'diaria_extra_grupo' pode faltar: vira premissa vazia ("lacuna"),
      e opções com 0 noites extras calculam normalmente (hospedagem extra = 0).
    - Viagens com várias cidades: 'trechos' (lista) substitui ida/volta. A soma de todos os
      trechos vai para as colunas de passagens; a volta fica 0 porque já está somada.
    """
    _limpar(d)
    for o in d["opcoes"]:
        if "noites_extras" in o and not (_num(o["noites_extras"]) and o["noites_extras"] >= 0):
            o["noites_extras"] = None  # vira "lacuna"
    for sm in d.get("simulacao", []):
        if "parcelas" in sm and not (_num(sm["parcelas"]) and sm["parcelas"] >= 1):
            sm["parcelas"] = None
    for p in d["premissas"]:
        if p.get("formato") not in FORMATOS:
            p.pop("formato", None)
    if not any(p.get("chave") == "diaria_extra_grupo" for p in d["premissas"]):
        d["premissas"].append({
            "chave": "diaria_extra_grupo", "rotulo": "Diária extra do grupo (R$)", "valor": None,
            "fonte": "Não se aplica: sem hospedagem fixa. Preencha só se for comparar noites extras."})
    for o in d["opcoes"]:
        tr = o.get("trechos")
        if not tr:
            continue
        o["ida_pix_pp"] = _soma([t.get("pix_pp") for t in tr])
        o["ida_cartao_pp"] = _soma([t.get("cartao_pp") for t in tr])
        o["volta_pp"] = 0
        o.setdefault("trecho", " → ".join(str(t.get("rota", "?")) for t in tr))
        o.setdefault("ida_data", str(tr[0].get("data", "")))
        o.setdefault("partida", str(tr[0].get("horario", "")))
        o.setdefault("companhia", " / ".join(dict.fromkeys(str(t["companhia"]) for t in tr if t.get("companhia"))))
        o.setdefault("volta", "Somada nos trechos (detalhe no comentário da coluna de ida)")
        o.setdefault("noites_extras", 0)
        det = []
        for t in tr:
            pix = t.get("pix_pp")
            car = t.get("cartao_pp")
            det.append(f"{t.get('rota', '?')} {t.get('data', '')} {t.get('horario', '')}, {t.get('companhia', '?')}: "
                       f"PIX {('R$ %.2f' % pix) if _num(pix) else 'lacuna'}, "
                       f"cartão {('R$ %.2f' % car) if _num(car) else 'lacuna'}"
                       + (f" ({t['fonte']})" if t.get("fonte") else ""))
        o.setdefault("fonte_ida", "Trechos por pessoa:\n" + "\n".join(det))


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
        if _host(como) or (isinstance(como, str) and _ESQUEMAS_RUINS.search(como)):
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
            "Ida (ou todos os trechos) por pessoa (PIX)", "Ida (ou todos os trechos) por pessoa (cartão)", "Volta por pessoa", "Noites extras",
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
            cd.cell(row=r, column=9).comment = Comment(str(o["fonte_ida"])[:LIMITE_TEXTO], "Cotação")
        if o.get("fonte_volta"):
            cd.cell(row=r, column=11).comment = Comment(str(o["fonte_volta"]), "Cotação")
        formula(cd.cell(row=r, column=13), f'=IF(L{r}=0,0,IFERROR(L{r}*{diaria}/{pax},"lacuna"))')
        formula(cd.cell(row=r, column=14), f'=IFERROR(I{r}+K{r}+M{r},"lacuna")', bold=True)
        formula(cd.cell(row=r, column=15), f'=IFERROR(J{r}+K{r}+M{r},"lacuna")', bold=True)
        formula(cd.cell(row=r, column=16), f'=IFERROR(N{r}*{pax},"lacuna")')
        formula(cd.cell(row=r, column=17), f'=IFERROR(O{r}*{pax},"lacuna")')
        formula(cd.cell(row=r, column=18), f'=IFERROR(N{r}-$N${r0},"lacuna")')
        formula(cd.cell(row=r, column=19), f'=IF(L{r}=0,"—",IFERROR(($N${r0}-I{r}-K{r})/L{r},"lacuna"))')
        if o.get("recomendada"):
            texto(cd.cell(row=r, column=20), o.get("veredito", "Recomendada"), bold=True)
        elif o.get("veredito"):
            # Veredito escrito pelo consultor (ex.: mais barata, mas com 5 h a mais de viagem)
            texto(cd.cell(row=r, column=20), o["veredito"])
        else:
            extra = f'&IF(L{r}>0," (só vale se a noite custar até R$ "&TEXT(S{r},"0")&" por pessoa)","")'
            sem_preco = (f'IF(AND(ISNUMBER(L{r}),L{r}>0,ISNUMBER(M{r})),"Preencher preços: só compensa se a passagem sair mais de R$ "&TEXT(M{r},"0")'
                         f'&" por pessoa mais barata que a recomendada",IF(AND(ISNUMBER(L{r}),L{r}>0),"Preencher preços e a diária extra","Preencher preços"))')
            formula(cd.cell(row=r, column=20),
                    f'=IF(ISNUMBER(R{r}),IF(R{r}<0,"Vale a pena: economiza R$ "&TEXT(-R{r},"0"),'
                    f'"Não vale: R$ "&TEXT(R{r},"0")&" a mais por pessoa"{extra}),{sem_preco})', fmt="General")
            cd.cell(row=r, column=20).alignment = Alignment(wrap_text=True, vertical="top")
        if o.get("recomendada"):
            for j in range(1, 21):
                cd.cell(row=r, column=j).fill = REC
        # conferência em Python
        try:
            pax_v = next(p["valor"] for p in d["premissas"] if p["chave"] == "passageiros")
            diaria_v = next(p["valor"] for p in d["premissas"] if p["chave"] == "diaria_extra_grupo")
            n_ext = o.get("noites_extras", 0)
            hosp = n_ext * diaria_v / pax_v if n_ext else (0 if n_ext == 0 else None)
            totais_py.append((o.get("opcao"), round(o["ida_pix_pp"] + o["volta_pp"] + hosp, 2),
                              round(o["ida_cartao_pp"] + o["volta_pp"] + hosp, 2)
                              if isinstance(o.get("ida_cartao_pp"), (int, float)) else "lacuna"))
        except (KeyError, TypeError, StopIteration, ZeroDivisionError):
            totais_py.append((o.get("opcao"), "lacuna", "lacuna"))
    fim = r0 + len(opcoes) - 1
    notas = [
        "Células azuis: valores coletados nas fontes (ver comentários). Células pretas: fórmulas.",
        "Hospedagem extra = noites extras × diária extra do grupo ÷ passageiros (aba 'Premissas e lacunas'); sem noites extras, é 0.",
        "Várias cidades: a coluna de ida soma todos os trechos e a volta fica 0; o detalhe por trecho está no comentário da célula.",
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
        formula(pg.cell(row=i, column=3), f'=IFERROR({C}!{col}{r0}*{pax},"lacuna")')
        c = numero(pg.cell(row=i, column=4), s.get("parcelas", 1), fmt="0")
        c.fill = INP
        formula(pg.cell(row=i, column=5), f'=IFERROR(C{i}/D{i},"lacuna")')
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

    # Defesa em profundidade: qualquer célula com cara de fórmula que não foi criada por
    # formula() vira texto (ex.: um título vindo de site que comece com "=").
    for ws in wb:
        for row in ws.iter_rows():
            for cel in row:
                if (isinstance(cel.value, str) and cel.value.startswith(PERIGOSOS)
                        and (ws.title, cel.coordinate) not in _FORMULAS):
                    cel.data_type = "s"
    saida = caminho_livre(checar_saida(saida, ".xlsx"))
    os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)
    wb.save(saida)
    return saida, totais_py


# ---------------------------------------------------------------------------
# Exportação em CSV (valores calculados; CSV não guarda fórmulas)
# ---------------------------------------------------------------------------

def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def calcular(d):
    """Mesmos cálculos das fórmulas do Excel, em Python."""
    normalizar(d)
    prem = {p["chave"]: p.get("valor") for p in d["premissas"]}
    pax, diaria = prem["passageiros"], prem.get("diaria_extra_grupo")
    opcoes = sorted(d["opcoes"], key=lambda o: not o.get("recomendada", False))
    linhas = []
    for o in opcoes:
        n = o.get("noites_extras", 0)
        hosp = None if n is None else 0 if not n else (n * diaria / pax if _num(diaria) and _num(pax) and pax else None)
        ida_p, ida_c, volta = o.get("ida_pix_pp"), o.get("ida_cartao_pp"), o.get("volta_pp")
        t_pix = ida_p + volta + hosp if all(_num(x) for x in (ida_p, volta, hosp)) else None
        t_car = ida_c + volta + hosp if all(_num(x) for x in (ida_c, volta, hosp)) else None
        linhas.append(dict(o, hosp_pp=hosp, total_pix_pp=t_pix, total_cartao_pp=t_car,
                           grupo_pix=t_pix * pax if _num(t_pix) else None,
                           grupo_cartao=t_car * pax if _num(t_car) else None))
    base = linhas[0]["total_pix_pp"]
    for li in linhas:
        n = li.get("noites_extras", 0)
        li["diferenca"] = li["total_pix_pp"] - base if _num(li["total_pix_pp"]) and _num(base) else None
        if n is None:
            li["equilibrio"] = None
        elif not n:
            li["equilibrio"] = "—"
        elif _num(base) and _num(li.get("ida_pix_pp")) and _num(li.get("volta_pp")):
            li["equilibrio"] = (base - li["ida_pix_pp"] - li["volta_pp"]) / n
        else:
            li["equilibrio"] = None
        if li.get("recomendada"):
            li["veredito_calc"] = li.get("veredito", "Recomendada")
        elif li.get("veredito"):
            li["veredito_calc"] = li["veredito"]
        elif li["diferenca"] is None:
            n = li.get("noites_extras", 0) or 0
            li["veredito_calc"] = (f"Preencher preços: só compensa se a passagem sair mais de R$ {li['hosp_pp']:.0f} "
                                   "por pessoa mais barata que a recomendada") if n and _num(li["hosp_pp"]) else (
                                   "Preencher preços e a diária extra" if n else "Preencher preços")
        elif li["diferenca"] < 0:
            li["veredito_calc"] = f"Vale a pena: economiza R$ {-li['diferenca']:.0f}"
        else:
            li["veredito_calc"] = f"Não vale: R$ {li['diferenca']:.0f} a mais por pessoa" + (
                f" (só vale se a noite custar até R$ {li['equilibrio']:.0f} por pessoa)" if _num(li["equilibrio"]) else "")
    return linhas, pax


def _cel_csv(v, decimal):
    if v is None or v == "":
        return "lacuna" if v is None else ""
    if _num(v):
        s = f"{v:.2f}" if isinstance(v, float) else str(v)
        return s.replace(".", decimal) if decimal != "." else s
    s = str(v)
    # Proteção contra injeção de fórmula ao abrir o CSV no Excel/Sheets
    return "'" + s if s.startswith(PERIGOSOS) else s


_ESQUEMAS_RUINS = re.compile(r"^\s*(javascript|vbscript|data|file|ms-[a-z-]+|about|blob):|^\s*\\\\", re.I)


def _texto_csv_link(v):
    """Campo que pode ser link ou texto: mantém http(s) e texto comum, descarta esquemas perigosos."""
    return "—" if isinstance(v, str) and _ESQUEMAS_RUINS.search(v) else v


def _link_csv(url):
    return url if _host(url) else "—"


def gerar_csv(d, pasta, sep=";", decimal=","):
    import csv
    validar(d)
    pasta = caminho_livre(checar_saida(pasta))
    os.makedirs(pasta, exist_ok=True)
    linhas, pax = calcular(d)

    def grava(nome, cab, rows):
        with open(os.path.join(pasta, nome), "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.writer(fh, delimiter=sep)
            w.writerow(cab)
            for r in rows:
                w.writerow([_cel_csv(v, decimal) for v in r])

    rec = linhas[0]
    resumo = [["Título", d["titulo"]], ["Consulta", d["consulta"]]]
    resumo += [["Recomendação", t] for t in d["recomendacao"]]
    resumo += [["Total por pessoa (PIX)", rec["total_pix_pp"]], ["Total por pessoa (cartão)", rec["total_cartao_pp"]],
               ["Total do grupo (PIX)", rec["grupo_pix"]], ["Total do grupo (cartão)", rec["grupo_cartao"]]]
    resumo += [[f"{li.get('opcao')}: diferença por pessoa", li["diferenca"]] for li in linhas[1:]]
    resumo += [["Risco", t] for t in d.get("riscos", [])]
    resumo += [["Crédito", CREDITO]]
    grava("1-resumo.csv", ["Item", "Valor"], resumo)

    grava("2-comparacao-de-datas.csv",
          ["Opção", "Data da ida", "Partida", "Chegada", "Trecho", "Companhia", "Escalas", "Volta",
           "Ida (ou todos os trechos) por pessoa (PIX)", "Ida (ou todos os trechos) por pessoa (cartão)", "Volta por pessoa", "Noites extras",
           "Hospedagem extra por pessoa", "TOTAL por pessoa (PIX)", "TOTAL por pessoa (cartão)",
           "Total do grupo (PIX)", "Total do grupo (cartão)", "Diferença vs. recomendada (PIX)",
           "Diária máx. por pessoa para empatar", "Veredito"],
          [[li.get(k) for k in ("opcao", "ida_data", "partida", "chegada", "trecho", "companhia", "escalas", "volta",
                                "ida_pix_pp", "ida_cartao_pp", "volta_pp", "noites_extras", "hosp_pp", "total_pix_pp",
                                "total_cartao_pp", "grupo_pix", "grupo_cartao", "diferenca", "equilibrio", "veredito_calc")]
           for li in linhas])

    grava("3-fontes.csv", ["Trecho", "Voo", "Fonte", "Por pessoa (PIX / à vista)", "Por pessoa (cartão)",
                           "Parcelamento", "Tarifa e bagagem", "Reputação / observação", "Link", "Hora da consulta"],
          [[f.get(k) if k != "link" else _link_csv(f.get(k)) for k in ("trecho", "voo", "fonte", "pix_pp", "cartao_pp",
                                                                       "parcelamento", "tarifa", "reputacao", "link", "hora")]
           for f in d.get("fontes", [])])

    colmap = {"ida_pix": "ida_pix_pp", "ida_cartao": "ida_cartao_pp", "volta": "volta_pp"}
    pag = [[p.get(k) if k != "link" else _link_csv(p.get(k))
            for k in ("canal", "desconto_pix", "parcelas_sem_juros", "parcela_minima", "juros", "observacoes", "link")]
           for p in d.get("pagamento", [])]
    for s in d.get("simulacao", []):
        v = rec.get(colmap.get(s.get("base", ""), "ida_pix_pp"))
        tot = v * pax if _num(v) else None
        parc = s.get("parcelas", 1)
        pag.append([f"Simulação: {s.get('trecho')}", s.get("forma"), f"{parc}x" if _num(parc) else "lacuna", None, None,
                    f"Total do grupo {_cel_csv(tot, decimal)}; parcela {_cel_csv(tot / parc if _num(tot) and _num(parc) else None, decimal)}. {s.get('obs', '')}", None])
    grava("4-pagamento.csv", ["Canal", "Desconto no PIX", "Parcelas sem juros", "Parcela mínima", "Juros",
                              "Observações", "Fonte"], pag)

    prem = [["Premissa", p.get("rotulo", p["chave"]), p.get("valor"), p.get("fonte", "")] for p in d["premissas"]]
    prem += [["Lacuna", l.get("item"), l.get("situacao"), _texto_csv_link(l.get("como_conferir"))] for l in d.get("lacunas", [])]
    grava("5-premissas-e-lacunas.csv", ["Tipo", "Item", "Valor / situação", "Fonte / como conferir"], prem)
    return pasta, [(li.get("opcao"), li["total_pix_pp"], li["total_cartao_pp"]) for li in linhas]


def main():
    global FONTE
    ap = argparse.ArgumentParser(description="Gera a planilha da cotação de viagem (Excel e/ou CSV).")
    ap.add_argument("dados", help="arquivo JSON de entrada")
    ap.add_argument("saida", help="caminho do .xlsx (com --formato csv, vira o nome da pasta dos CSVs)")
    ap.add_argument("--formato", choices=["xlsx", "csv", "todos"], default="xlsx",
                    help="xlsx (padrão; também serve para Google Sheets), csv ou todos")
    ap.add_argument("--fonte", default=FONTE, help="fonte das células do Excel (padrão: Gothic A1)")
    ap.add_argument("--separador", default=";", help="separador do CSV (padrão ';', o que o Excel em português espera)")
    ap.add_argument("--decimal", default=",", help="separador decimal do CSV (padrão ',')")
    a = ap.parse_args()
    FONTE = a.fonte
    with open(a.dados, encoding="utf-8") as fh:
        d = json.load(fh)
    totais = None
    if a.formato in ("xlsx", "todos"):
        saida, totais = gerar(d, a.saida)
        print(f"Excel salvo em: {saida}")
    if a.formato in ("csv", "todos"):
        pasta = os.path.splitext(a.saida)[0] + "_csv"
        pasta, totais_csv = gerar_csv(d, pasta, a.separador, a.decimal)
        print(f"CSVs salvos em: {pasta}")
        totais = totais or totais_csv
    print("Conferência (por pessoa: PIX | cartão):")
    for nome, pix, cartao in totais:
        f = lambda v: f"{v:.2f}" if _num(v) else "lacuna"
        print(f"  - {nome}: {f(pix)} | {f(cartao)}")


if __name__ == "__main__":
    main()
