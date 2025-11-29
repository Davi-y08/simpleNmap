import os
import pyfiglet #pip
import platform
import shutil
import netifaces #pip
import subprocess

sair = False

class Nmap:
    def __init__(self, command = None):
        self.command = command

    def scan_devices_on_network(self, target):
        result = subprocess.run(
        ["nmap", "-sn", "-oG", "-", target],
        capture_output=True,
        text=True
        )

        found = []

        for line in result.stdout.splitlines():
            if line.startswith("Host:") and "Status: Up" in line:
                parts = line.split()
                ip = parts[1]
                found.append(ip)
        
        print("\nDispositivos na sua rede: ")
        for device in found:
            print("Device: ", device)
    
    def indetity_ports_in_a_target(self, target, ports):
        result = subprocess.run(
            ["nmap", target],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        #essa merda funciona por incrivel que pareça
        founds = []
        for line in result.stdout.splitlines():
            for port in ports:
                if line.startswith(f"{port}/"):
                    parts = line.split()
                    porta = parts[0]
                    founds.append(porta)

        print("Portas abertas no alvo: ")
        for found in founds:
            print(found)

    def fast_doors_scan(self, target, ports):
        result = subprocess.run(
            ["nmap", "-F", target],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        if result.returncode != 0:
            print("command error")
            print(result.stderr)
            return
        
        output = result.stdout

        if not output.strip():
            print("nmap return nothing")
            return

        found = []
        for line in result.stdout.splitlines():
            for port in ports:
                if line.startswith(f"{port}/"):
                    parts = line.split()
                    porta = parts[0]
                    found.append(porta)
        
        if not found:
            print("no door open")
            return

        for f in found:
            print(f)

    def detailed_door_scan(self, target, ports):
        result = subprocess.run(
            ["nmap", "-p-", target],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        if result.returncode != 0:
            print("command error")
            print(result.stderr)
            return
        
        output = result.stdout

        if not output.strip():
            print("nmap return nothing")
            return
    
        found = []
        for line in result.stdout.splitlines():
            for port in ports:
                if line.startswith(f"{port}/"):
                    parts = line.split()
                    porta = parts[0]
                    found.append(porta)
        if not found:
            print("no door open")
            return

        for f in found:
            print(f)

nmap = Nmap()

ready_commands = {
    "disp_scan": "-sn"
}

options = ["Dispositivos ativos na sua rede", "Identificar portas abertas", ""]
operational_system = platform.system()

def print_main_screen():
    result = pyfiglet.figlet_format("simple nmap")
    print(result)    

def print_options():
    print("|-------------------------------------------------------------|")
    print("Insira uma opção abaixo: ")

    tam = len(options)
    i = 0
    for option in options:
        i+=1
        print(i, "-", option)

    print("|-------------------------------------------------------------|")

def define_target():
   exit_target = False
   target = ""
   while not exit_target:
    target = input("insira um alvo ( 0 para sair ): ")
    if not target:
           print("inválido")
    else:
        return target

def identify_choose(ipt):
    if ipt == 0:
        print("Volte sempre!")
        return True
    elif ipt == 1:
        gateway = netifaces.gateways()["default"][netifaces.AF_INET][0]
        nmap.scan_devices_on_network(f"{gateway}/24")
        print(f"gateway: {gateway}")
    elif ipt == 2:
        print("\ndoor scanner")
        target = define_target()

        intern_options = ["fast scan", "default scan", "detailed scan", "specific doors", "door range"]
        i = 0
        for options in intern_options:
            i+=1
            print(f"{i} - {options}")

        intern_option_string = input("enter a option (0 to exit): ") 
        opcao = -1
        try:
            opcao = int(intern_option_string)
        except ValueError:
            print("enter data correctly")
            return 
        
        if opcao == 1:
            ports = open("fast_door_scan.txt").read().strip().split(", ")
            nmap.fast_doors_scan(target, ports)
        elif opcao == 2:
            ports = open("ports.txt").read().strip().split(",")
            nmap.indetity_ports_in_a_target()
        elif opcao == 3:
            ports = open("all_ports.txt").read().strip().split(", ")
            nmap.detailed_door_scan(target, ports)
    

def nmap_is_installed():
    if shutil.which("nmap"):
        return
    else:
        print("Por favor, instale o nmap")

print_main_screen()
nmap_is_installed()
print_options()

while not sair:
    user_input_str = input("Insira uma opção: ")
    try:
        result = identify_choose(int(user_input_str))
        sair = result

    except ValueError:  
        print("Insira os dados corretamente")