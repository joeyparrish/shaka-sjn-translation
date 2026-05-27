def compute(source, source_json):
    source_keys = set(source_json.keys())
    total = len(source_keys)
    translated = sum(
        1 for t in source["translations"]
        if t.get("key") in source_keys and t.get("sjn", {}).get("tengwar")
    )
    pct = ((100 * translated) // total) if total else 0
    return {"translated": translated, "total": total, "pct": pct}
