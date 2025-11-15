import socket

def grab_banner(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(0.5)
        sock.connect((ip, port))
        sock.send(b"\r\n\r\n")

        banner = sock.recv(1024)
        sock.close()

        return banner.decode(errors="ignore").strip()
    except:
        return None
