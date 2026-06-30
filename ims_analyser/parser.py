import subprocess
from typing import Dict, List, Optional


SIP_FIELDS = [
    "call_id",
    "method",
    "status",
    "from",
    "to",
    "cseq",
    "via",
    "contact",
]


def run_tshark(pcap_path: str) -> List[str]:
    cmd = [
        "tshark",
        "-r",
        pcap_path,
        "-Y",
        "sip",
        "-T",
        "fields",
        "-E",
        "separator=\t",
        "-e",
        "sip.Call-ID",
        "-e",
        "sip.Method",
        "-e",
        "sip.Status-Code",
        "-e",
        "sip.From",
        "-e",
        "sip.To",
        "-e",
        "sip.CSeq",
        "-e",
        "sip.Via",
        "-e",
        "sip.Contact",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        stderr = result.stderr.strip() or "tshark failed"
        raise RuntimeError(f"tshark error: {stderr}")

    return [line for line in result.stdout.splitlines() if line.strip()]


def parse_lines(lines: List[str]) -> List[Dict[str, Optional[str]]]:
    packets: List[Dict[str, Optional[str]]] = []

    for line in lines:
        if not line or not line.strip():
            continue

        parts = line.split("\t")

        packet: Dict[str, Optional[str]] = {}
        for index, field in enumerate(SIP_FIELDS):
            value = parts[index].strip() if index < len(parts) else ""
            packet[field] = value if value else None

        packets.append(packet)

    return packets


def group_by_call_id(packets):
    call_map = {}

    for pkt in packets:
        cid = pkt["call_id"]
        if not cid:
            continue

        call_map.setdefault(cid, []).append(pkt)

    return call_map


def parse_pcap(pcap_path):
    lines = run_tshark(pcap_path)
    return parse_lines(lines)