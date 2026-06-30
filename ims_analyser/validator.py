from utils import normalize, extract_headers


CALL_FLOWS = {
    "MO": ["INVITE", "100", "180", "200", "ACK"],
    "REGISTER": ["REGISTER", "200"]
}


def validate_flow(flow, call_type):
    expected = CALL_FLOWS.get(call_type, [])

    detected = []

    for pkt in flow:
        msg = normalize(pkt)
        if msg:
            detected.append(msg)

    missing = [x for x in expected if x not in detected]

    return detected, missing


def validate_headers(flow):
    errors = []

    call_id = None

    for pkt in flow:
        h = extract_headers(pkt)

        if not call_id:
            call_id = h["call_id"]
        elif call_id != h["call_id"]:
            errors.append("Call-ID mismatch")

        if not h["from"] or not h["to"]:
            errors.append("Missing From/To")

        if not h["via"]:
            errors.append("Missing Via")

    return list(set(errors))


def validate_sdp(flow):
    # tshark version does not extract SDP yet → keep simple
    return []


def validate_all(flow, call_type):

    detected, missing = validate_flow(flow, call_type)
    header_errors = validate_headers(flow)
    sdp_errors = validate_sdp(flow)

    status = "PASS" if not (missing or header_errors or sdp_errors) else "FAIL"

    return {
        "status": status,
        "detected_flow": detected,
        "missing_steps": missing,
        "header_errors": header_errors,
        "sdp_errors": sdp_errors
    }