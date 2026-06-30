from typing import Dict, Optional


def read_file(path: str):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            yield line


def normalize(pkt: Dict[str, Optional[str]]) -> Optional[str]:
    if not pkt:
        return None

    method = pkt.get("method")
    status = pkt.get("status")

    if method:
        return method.strip().upper()
    if status:
        return status.strip()
    return None


def extract_headers(pkt: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]:
    return {
        "call_id": pkt.get("call_id"),
        "from": pkt.get("from"),
        "to": pkt.get("to"),
        "via": pkt.get("via"),
        "contact": pkt.get("contact"),
    }
