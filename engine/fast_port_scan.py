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


# THIS is the function your engine calls
def fast_port_scan(ip, ports=COMMON_PORTS):
    """
    If called inside FastAPI (event loop running) → schedule async task
    If called from CLI (no event loop) → asyncio.run()
    """

    try:
        loop = asyncio.get_running_loop()
        # We are inside FastAPI (async mode)
        # Must return a coroutine to be awaited by the engine
        return asyncio.ensure_future(async_scan_ports(ip, ports))

    except RuntimeError:
        # No event loop → CLI mode → safe to run blocking
        return asyncio.run(async_scan_ports(ip, ports))
