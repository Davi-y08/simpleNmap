import requests, json, csv, pathlib, time, sys

BASE   = ""
ENDP   = "/api/v1/products"
PARAMS = {"per-page": 9999, "page": 1}   # lote máximo
HEADERS= {"User-Agent": "Mozilla/5.0"}

def get_page(p):
    """Baixa uma página e devolve lista de produtos (pode ser vazia)."""
    url = BASE+ENDP
    pr  = PARAMS.copy()
    pr["page"] = p
    r = requests.get(url, params=pr, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()   # espera lista [{}]

def main():
    all_prods = []
    page = 1
    while True:
        print(f"[+] página {page}")
        data = get_page(page)
        if not data: break
        all_prods.extend(data)
        page += 1
        # se vier menos que 9999 já era o fim
        if len(data) < 9999: break
        time.sleep(0.3)  # evita gatilho de WAF

    # salva JSON brutos
    pathlib.Path("catalogo.json").write_text(json.dumps(all_prods, ensure_ascii=False, indent=2))
    print(f"[+] {len(all_prods)} produtos salvos em catalogo.json")

    # CSV resumido
    with open("catalogo.csv","w",encoding="utf-8",newline="") as f:
        w = csv.writer(f)
        w.writerow(["id","nome","preco","estoque","url_foto"])
        for p in all_prods:
            w.writerow([
                p.get("id"),
                p.get("name"),
                p.get("price"),
                p.get("stock_quantity"),
                (p.get("images") or [{}])[0].get("url")
            ])
    print("[+] catalogo.csv pronto")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)