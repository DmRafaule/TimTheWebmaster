import json
from .proxy_rotator import Proxy, Rotator

def proxy_to_requests_proxy(proxy_path, type):
    return {'http': f'{type}://{proxy_path}', 'https': f'{type}://{proxy_path}'}

def load_proxies(file_path):
    result = []
    with open(file_path, 'r', encoding='utf-8') as file:
        result = json.loads(file.read())
    return result