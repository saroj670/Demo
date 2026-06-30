def filter_by_msisdn(call_map, a_party, b_party):

    filtered = {}

    for call_id, flow in call_map.items():

        for pkt in flow:

            from_val = str(pkt.get("from", ""))
            to_val = str(pkt.get("to", ""))

            if (
                (a_party in from_val and b_party in to_val) or
                (b_party in from_val and a_party in to_val)
            ):
                filtered[call_id] = flow
                break

    return filtered