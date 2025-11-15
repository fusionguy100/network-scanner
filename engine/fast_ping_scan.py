import subprocess
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed

def ping_ip(ip):
    cmd = ["ping", "-n", "1", "-w", "200", ip]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if b"TTL=" in result.stdout:
        return ip

    return None


def fast_ping_scan(subnet, threads=100):
    network = ipaddress.ip_network(subnet, strict=False)
    hosts = [str(ip) for ip in network.hosts()]

    active = []

    print(f"[+] Starting fast ping scan with {threads} threads...")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(ping_ip, ip): ip for ip in hosts}

        for future in as_completed(futures):
            ip = future.result()
            if ip:
                active.append(ip)

    print(f"[+] Ping scan complete. {len(active)} hosts active.")
    return active
