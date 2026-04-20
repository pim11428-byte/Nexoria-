import re
import socket
import requests


def detect_entity_type(entity: str):
    if re.match(r"[^@]+@[^@]+\.[^@]+", entity):
        return "email"
    if re.match(r"^\+?\d{10,15}$", entity):
        return "phone"
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", entity):
        return "ip"
    if re.match(r"^[a-zA-Z0-9\-]+\.[a-zA-Z]{2,}$", entity):
        return "domain"
    if " " in entity:
        return "fio"
    return "username"


def analyze_email(email: str):
    return {
        "type": "email",
        "valid": True,
        "breached": False,
        "mx_records": ["mx.example.com"],
    }


def analyze_phone(phone: str):
    return {
        "type": "phone",
        "country": "Unknown",
        "valid": True,
    }


def analyze_ip(ip: str):
    try:
        host = socket.gethostbyaddr(ip)[0]
    except:
        host = None

    return {
        "type": "ip",
        "hostname": host,
    }


def analyze_domain(domain: str):
    try:
        ip = socket.gethostbyname(domain)
    except:
        ip = None

    return {
        "type": "domain",
        "ip": ip,
    }


def analyze_username(username: str):
    return {
        "type": "username",
        "profiles": [],
    }


def analyze_fio(fio: str):
    return {
        "type": "fio",
        "matches": [],
    }


def analyze_entity(entity: str):
    t = detect_entity_type(entity)

    if t == "email":
        return analyze_email(entity)
    if t == "phone":
        return analyze_phone(entity)
    if t == "ip":
        return analyze_ip(entity)
    if t == "domain":
        return analyze_domain(entity)
    if t == "fio":
        return analyze_fio(entity)
    return analyze_username(entity)
