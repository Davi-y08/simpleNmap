import subprocess
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

class Nmap:
    def __init__(self, command = None):
        self.command = command

    def _door_scan_result_aux(self, output, doors):
        founds = []
        for line in output.stdout.splitlines(): #percorrer cada linha, onde o stdout quebra os '\n' deixando em linha unica, e com o splitlines para separar linha por linha
            for door in doors:
                if line.startswith(f"{door}/"): 
                    parts = line.split()
                    door_aux = parts[0]
                    founds.append(door_aux)

        return founds
    
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
        
        print("\fDevices in your network: ")
        for device in found:
            print(f"Device: {Colors['GREEN']}{device}{Colors['RESET']}")
    
    def indetify_doors_in_target(self, target, doors):
        string_doors = ",".join(str(door) for door in doors)
        result = subprocess.run(
            ["nmap", string_doors, target],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        #essa merda funciona por incrivel que pareça
        
        founds = self._door_scan_result_aux(output=result, doors=doors)

        print("Open doors in the target: ")
        for found in founds:
            print(found)

    def fast_doors_scan(self, target, doors):
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

        founds = self._door_scan_result_aux(output=result, doors=doors)
        
        if not founds:
            print(f"{Colors['RED']}no door open{Colors['RESET']}")
            return

        for door in founds:
            print(door)

    def detailed_door_scan(self, target, doors):
        result = subprocess.run(
            ["nmap", "-p-", target],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        if result.returncode != 0:
            print("command error")
            print(f"{Colors['RED']} {result.stderr} {Colors['RESET']}")
            return
        
        output = result.stdout

        if not output.strip():
            print("nmap return nothing")
            return
    
        founds = self._door_scan_result_aux(output=result, doors=doors)

        if not founds:
            print("no door open")
            return

        for door in founds:
            print(door)
    
    def scan_specific_doors(self, target, doors):
        string_doors = ""
        string_doors = ",".join(str(d) for d in doors) 

        result = subprocess.run(
            ["nmap", "-p", string_doors, target],
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
            print("no response of nmap")
            return
        
        founds = self._door_scan_result_aux(output=result, doors=doors)
        
        if not founds:
            print("no door open")
            return
        
        for f in founds:
            print(f)

    def scan_doors_in_range(self, begin, end, target):
        target_doors = []
        
        if begin > end:
            print("error in range specific")
            return

        for i in range(begin, end + 1):
            target_doors.append(i)
            
        string_doors = ",".join(str(d) for d in target_doors)   
        
        result = subprocess.run(
            ["nmap", "-p", string_doors, target],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        if result.returncode != 0:
            print("command error")
            print(result.stderr)
            return

        if not result.stdout.strip():
            print("nmap no responses")
            return

        founds = self._door_scan_result_aux(output=result, doors=target_doors)

        if not founds:
            print("no doors open in range")
            return

        for door in founds:
            print(door) 