Colors = {
    'RESET': '\033[0m',
    'RED': '\033[31m',
    'GREEN': '\033[32m',
    'YELLOW': '\033[33m',
    'BLUE': '\033[34m',
    'MAGENTA': '\033[35m',
    'CYAN': '\033[36m',
    'WHITE': '\033[37m',
}

def scrape_subdomain(domain):
    import requests
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    try:
        r = requests.get(url, timeout=60)
        subDomains = []
        if r.status_code == 200:
            subs = set([entry['name_value'] for entry in r.json()])
            subDomains = subs

        else:
            print(f"Error, HTTP code: {Colors['RED']} {r.status_code} {Colors['RESET']}")

        for sub in subDomains:
            print(f"SUB -> {Colors['MAGENTA']}{sub}{Colors['RESET']}")

    except Exception as e:
        print(f"subdomains scanner erro: {e}")
