import pyfiglet #pip
import platform
import shutil
import netifaces #pip
from modules import Nmap
from modules import scrape_subdomain
from pathlib import Path

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

sair = False
nmap = Nmap()

ready_commands = {
    "disp_scan": "-sn"
}

BASE_DIR = Path(__file__).resolve().parent

options = ["Active devices in yout network", "Identify open doors", "Subdomains scraper"]
operational_system = platform.system()

def print_main_screen():
    result = pyfiglet.figlet_format("simple nmap")
    print(result)    

def print_options():
    print("|-------------------------------------------------------------|")
    print("Enter an option below: ")

    tam = len(options)
    i = 0
    for option in options:
        i+=1
        print(i, "-", option)

    print("|-------------------------------------------------------------|")

def load_doors(relative_path):
    path = BASE_DIR / relative_path
    return [int(p.strip()) for p in path.read_text().split(",") if p.strip()]


def define_target():
   exit_target = False
   target = ""
   while not exit_target:
    target = input("Enter a target (0 to exit): ")
    if not target:
           print("Invalid")
    else:
        return target

def identify_choose(ipt):
    if ipt == 0:
        print("Come back often!")
        return True
    elif ipt == 1:
        gateway = netifaces.gateways()["default"][netifaces.AF_INET][0]
        nmap.scan_devices_on_network(f"{gateway}/24")
        print(f"gateway: {gateway}")
    elif ipt == 2:
        print("\ndoor scanner")
        target = define_target()

        intern_options = ["Fast scan", "Default scan", "Detailed scan", "Specific doors", "Door range"]
        i = 0
        for options in intern_options:
            i+=1
            print(f"{i} - {options}")

        intern_option_string = input("Enter a option (0 to exit): ") 
        opcao = -1
        try:
            opcao = int(intern_option_string)
        except ValueError:
            print("Enter data correctly")
            return 
        
        if opcao == 1:
            nmap.fast_doors_scan(target, doors=load_doors("txtlist/fast_door_scan.txt"))
        elif opcao == 2:
            nmap.indetify_doors_in_target(target=target, doors=load_doors("txtlist/ports.txt"))
        elif opcao == 3:
            nmap.detailed_door_scan(target, ports=load_doors("txtlist/all_ports.txt"))

    elif ipt == 3:
        print("\nsubdomain scaner")
        target = define_target()
        
        scrape_subdomain(target)

def nmap_is_installed():
    if shutil.which("nmap"):
        return
    else:
        print("Please, install the nmap")

print_main_screen()
nmap_is_installed()
print_options()

while not sair:
    user_input_str = input("Enter a option: ")
    try:
        result = identify_choose(int(user_input_str))
        sair = result

    except ValueError:  
        print("Enter data correctly")