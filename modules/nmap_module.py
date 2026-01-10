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

    def _parse_on_detection(self, output):
        os_info = []

        for line in output.stdout.splitlines():
            line = line.strip()

            if line.startswith("Running:"):
                os_info.append(line.replace("Running:", "").strip())

            elif line.startswith("OS details:"):
                os_info.append(line.replace("OS details:", "").strip())

            elif line.startswith("Aggressive OS guesses:"):
                os_info.append(line.replace("Aggressive OS guesses:", "").strip())

        return os_info

    def print_doors(self, doors):
        if not doors:
            print("no doors open")
            return
        
        for door in doors:
            print(door)

    def _door_scan_result_aux(self, output, doors):
        founds = []
        for line in output.stdout.splitlines(): #percorrer cada linha, onde o stdout quebra os '\n' deixando em linha unica, e com o splitlines para separar linha por linha
            for door in doors:
                if line.startswith(f"{door}/"): 
                    parts = line.split()
                    door_aux = parts[0]
                    founds.append(door_aux)

        return founds

    def _verify_response(self, result):
        if result.returncode != 0:
            print("command error")
            print(result.stderr)
            return
        
        output = result.stdout

        if not output.strip():
            print("nmap return nothing")
            return

    
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
        self.print_doors(founds)

    def fast_doors_scan(self, target, doors):
        result = subprocess.run(
            ["nmap", "-F", target],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        self._verify_response(result)
        founds = self._door_scan_result_aux(output=result, doors=doors)
        self.print_doors(founds)

    def detailed_door_scan(self, target, doors):
        result = subprocess.run(
            ["nmap", "-p-", target],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        self._verify_response(result)
        founds = self._door_scan_result_aux(output=result, doors=doors)
        self.print_doors(founds)
    
    def scan_specific_doors(self, target, doors):
        string_doors = ""
        string_doors = ",".join(str(d) for d in doors) 

        result = subprocess.run(
            ["nmap", "-p", string_doors, target],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        self._verify_response(result)
        founds = self._door_scan_result_aux(output=result, doors=doors)
        self.print_doors(founds)

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

        self._verify_response(result)
        founds = self._door_scan_result_aux(output=result, doors=target_doors)
        self.print_doors(founds) 
    
    def detect_os(self, target):
        result = subprocess.run(
            ["nmap", "-O", str(target)],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        
        self._verify_response(result)
        
        os_list = self._parse_on_detection(output=result)

        if not os_list:
            print(f"{Colors['RED']}OS not detected{Colors['RESET']}")

        for os in os_list:
            print(f" - {Colors['BLUE']}OS: {os}{Colors['RESET']}")