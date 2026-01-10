import requests

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

def ip_look_up(ip):
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        if response.status_code == 200:
            data = response.json()
            return{
                "IP": data.get("ip"),
                "City": data.get("city"),
                "Region": data.get("region"),
                "Country": data.get("country"),
                "Location": data.get("loc"),
                "Org": data.get("org"),
                "Hostname": data.get("hostname", "N/A")
            }
        
        else:
            return {
                "Error": f"Unable to fetch data (Status Code {response.status_code})"
            }
        
    except Exception as e:
        return {
            "Error": str(e)
        }