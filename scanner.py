import nmap

RISKY_PORTS = [21, 23, 445, 139, 3389]

def scan_network(ip_range):
    scanner = nmap.PortScanner()
    scanner.scan(hosts=ip_range, arguments="-T4 -F")
    results = []

    for host in scanner.all_hosts():
        if scanner[host].state() == "up":
            ports = [p for p in scanner[host]['tcp'].keys()] if 'tcp' in scanner[host] else []
            warning = ""
            risk_details = []
            for port in ports:
                if port in RISKY_PORTS:
                    warning = "⚠️ Risky ports open!"
                    risk_details.append(f"Port {port}: Potentially vulnerable to exploits.")
            results.append({"ip": host, "status": "up", "ports": ports, "warning": warning, "risk_details": risk_details})
    return results

def get_client_ip(req):
    return req.remote_addr