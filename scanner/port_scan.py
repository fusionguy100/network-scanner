import socket

COMMON_PORTS = [22, 23, 80, 443, 3389, 445, 139, 3306, 8080]

def scan_ports(ip: str, ports=COMMON_PORTS):
    open_ports = []

    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)

        try:
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
        except:
            pass
        finally:
            sock.close()

    return open_ports
