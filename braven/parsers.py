def parse_summary_block(lines):
    return {
        ln.split(":", 1)[0].strip(): ln.split(":", 1)[1].strip()
        for ln in lines
        if ":" in ln
    }
