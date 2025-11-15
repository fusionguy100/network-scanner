from scapy.all import ARP, Ether, srp

def discover_hosts(subnet: str):
    """
    Returns a list of active devices on the subnet.
    """
    print(f"[+] Scanning subnet: {subnet}")

    arp = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=2, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({
            "ip": received.psrc,
            "mac": received.hwsrc
        })

    return devices
