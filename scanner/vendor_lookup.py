import requests

def lookup_vendor(mac: str):
    try:
        # API: https://macvendors.com/
        url = f"https://api.macvendors.com/{mac}"
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return response.text
    except:
        pass

    return "Unknown Vendor"
