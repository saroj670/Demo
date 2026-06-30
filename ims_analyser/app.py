from fastapi import FastAPI, UploadFile, File
import pandas as pd
import tempfile

from parser import parse_pcap, group_by_call_id
from validator import validate_all
from filter import filter_by_msisdn

app = FastAPI()


@app.post("/analyze")
async def analyze(
    excel_file: UploadFile = File(...),
    pcap_file: UploadFile = File(...)
):

    # ==============================
    # Read Excel directly (FIXED)
    # ==============================
    try:
        df = pd.read_excel(excel_file.file, engine="openpyxl")
    except Exception as e:
        return {"error": f"Excel read failed: {str(e)}"}

    # ==============================
    # Save PCAP
    # ==============================
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pcap") as tmp_pcap:
        tmp_pcap.write(await pcap_file.read())
        pcap_path = tmp_pcap.name

    # ==============================
    # Parse PCAP
    # ==============================
    try:
        packets = parse_pcap(pcap_path)
        call_map = group_by_call_id(packets)
    except Exception as e:
        return {"error": f"PCAP parsing failed: {str(e)}"}

    results = []

    # ==============================
    # Process Excel rows
    # ==============================
    for index, row in df.iterrows():

        call_type = str(row.get("call_type", "")).strip()
        a_party = str(row.get("a_party", "")).strip()
        b_party = str(row.get("b_party", "")).strip()

        filtered_calls = filter_by_msisdn(call_map, a_party, b_party)

        for call_id, flow in filtered_calls.items():

            validation = validate_all(flow, call_type)

            results.append({
                "row": int(index),
                "call_id": call_id,
                "call_type": call_type,
                "a_party": a_party,
                "b_party": b_party,
                "result": validation
            })

    return {"results": results}