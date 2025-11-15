import asyncio

COMMON_PORTS = [22, 23, 80, 443, 445, 139, 3389, 8080, 3306]


async def scan_port(ip, port):
    try:
        conn = asyncio.open_connection(ip, port)
        reader, writer = await asyncio.wait_for(conn, timeout=0.3)
        writer.close()
        return port
    except:
        return None


async def async_scan_ports(ip, ports=COMMON_PORTS):
    tasks = [scan_port(ip, port) for port in ports]
    results = await asyncio.gather(*tasks)
    return [port for port in results if port is not None]


def fast_port_scan(ip, ports=COMMON_PORTS):
    return asyncio.run(async_scan_ports(ip, ports))
