from scapy.all import IP, ICMP, sr1

def guess_os(ip: str):
    """
    Basic OS fingerprinting based on TTL.
    """
    try:
        pkt = IP(dst=ip)/ICMP()
        reply = sr1(pkt, timeout=1, verbose=0)

        if reply:
            ttl = reply.ttl

            if ttl >= 120:
                return "Linux/Unix"
            elif ttl >= 60:
                return "Windows"
            else:
                return "Unknown"
        else:
            return "No response"
    except:
        return "Unknown"
