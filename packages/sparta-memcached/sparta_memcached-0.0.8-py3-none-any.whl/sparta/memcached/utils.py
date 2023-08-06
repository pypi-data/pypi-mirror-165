import ipaddress
import socket
import typing
from urllib.parse import urlsplit


# Solution copied from this lab https://www.cloudskillsboost.google/focuses/615?parent=catalog

def _is_valid_ip(addr, _class: typing.Any = ipaddress.IPv4Network):
    try:
        _class(addr)
        return True
    except ValueError:
        return False


def is_valid_ipv4(addr):
    return _is_valid_ip(addr)


def is_valid_ipv6(addr):
    return _is_valid_ip(addr, _class=ipaddress.IPv6Network)


def _append_port(addr: str, port: typing.Optional[int]):
    return f"{addr}:{port}" if port else addr


def _resolve_dns(server: str) -> typing.List[str]:
    try:
        # urlparse() and urlsplit() insists on absolute URLs starting with "//"
        result = urlsplit('//' + server)
        addr = result.hostname
        port = result.port
        if is_valid_ipv4(addr):  # memcached supports only IPv4
            return [_append_port(addr, port)]
        _, _, ips = socket.gethostbyname_ex(addr)
        return [_append_port(ip, port) for ip in ips]
    except Exception as error:
        raise ValueError(f"Invalid server '{server}'") from error


def resolve_dns(
        servers: typing.Union[str, typing.List[str]]
) -> typing.List[str]:
    if isinstance(servers, str):
        return _resolve_dns(servers)
    return [x for server in servers for x in _resolve_dns(server)]
