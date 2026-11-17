#!/usr/bin/env python3
"""Build the chemical lists used by the Safety Data Sheet Checker.

- UK REACH Candidate List: downloaded from HSE each run.
- EU REACH Candidate List: ECHA blocks automated downloads, so save ECHA's Excel
  export by hand as data/chem/sources/echa-candidate-list.xlsx (see README in
  that folder). If the file is missing, the last svhc-eu.json is kept.
- CBAM chemicals, F-gases and known PFAS: short fixed lists below, with sources.

Writes data/chem/svhc-uk.json, svhc-eu.json and lists.json.
"""
import datetime as dt, io, json, re, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/chem"
HSE_URL = "https://www.hse.gov.uk/reach/assets/docs/candidate-list.xlsx"
HSE_PAGE = "https://www.hse.gov.uk/reach/candidate-list.htm"
ECHA_FILE = OUT / "sources/echa-candidate-list.xlsx"
ECHA_PAGE = "https://echa.europa.eu/candidate-list-table"
UA = {"User-Agent": "Mozilla/5.0 (compatible; robertjpark.co.uk list builder)"}
CAS = re.compile(r"\b\d{2,7}-\d{2}-\d\b")
EC = re.compile(r"\b\d{3}-\d{3}-\d\b")

def iso(v):
    if isinstance(v, (dt.date, dt.datetime)):
        return v.strftime("%Y-%m-%d")
    s = str(v or "").strip()
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    if m:
        return f"{m[3]}-{int(m[2]):02d}-{int(m[1]):02d}"
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)
    return m[0] if m else ""

def parse(xlsx_bytes):
    """Find the sheet and header row with CAS and EC columns; return entries."""
    import openpyxl
    wb = openpyxl.load_workbook(io.BytesIO(xlsx_bytes), read_only=True, data_only=True)
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        for h, row in enumerate(rows[:20]):
            cells = [str(c or "").lower() for c in row]
            if any("cas" in c for c in cells) and any(c.startswith("ec") for c in cells):
                col = lambda *keys: next((i for i, c in enumerate(cells) if any(k in c for k in keys)), None)
                cn, cd, ce, cc = col("substance name", "name"), col("description"), col("ec"), col("cas")
                cr, ct = col("reason"), col("date of inclusion", "date")
                out = []
                for r in rows[h + 1:]:
                    name = str(r[cn] or "").strip() if cn is not None else ""
                    if not name:
                        continue
                    out.append({
                        "name": re.sub(r"\s+", " ", name),
                        "description": re.sub(r"\s+", " ", str(r[cd] or "").strip()) if cd is not None else "",
                        "ec": EC.findall(str(r[ce] or "")) if ce is not None else [],
                        "cas": CAS.findall(str(r[cc] or "")) if cc is not None else [],
                        "reason": re.sub(r"\s*#\s*", "; ", re.sub(r"\s+", " ", str(r[cr] or "").strip())) if cr is not None else "",
                        "date": iso(r[ct]) if ct is not None else ""})
                if out:
                    return out
    raise ValueError("No sheet with CAS and EC columns found")

def write(name, entries, source, page):
    dates = [e["date"] for e in entries if e["date"]]
    doc = {"source": source, "page": page, "built": dt.date.today().isoformat(),
           "entries": len(entries), "latest_inclusion": max(dates) if dates else "", "items": entries}
    (OUT / name).write_text(json.dumps(doc, ensure_ascii=False, indent=0), encoding="utf-8")
    return {k: doc[k] for k in ("source", "page", "built", "entries", "latest_inclusion")}

# Fixed lists. CBAM: CN headings from the site's own lookup (cbam-desk/is-it-a-cbam-good.md).
CBAM = [
    {"cas": "1333-74-0", "name": "Hydrogen", "cn": "2804 10"},
    {"cas": "7697-37-2", "name": "Nitric acid", "cn": "2808"},
    {"cas": "7664-41-7", "name": "Ammonia", "cn": "2814"},
    {"cas": "1336-21-6", "name": "Ammonia solution (ammonium hydroxide)", "cn": "2814"},
    {"cas": "7757-79-1", "name": "Potassium nitrate", "cn": "2834 21"},
    {"cas": "6484-52-2", "name": "Ammonium nitrate", "cn": "3102"},
    {"cas": "57-13-6", "name": "Urea", "cn": "3102"},
    {"cas": "7783-20-2", "name": "Ammonium sulphate", "cn": "3102"}]
# Fluorinated gases: EU F-gas Regulation (EU) 2024/573 applies in NI; GB keeps assimilated Reg 517/2014.
FGAS = [
    ("75-46-7", "HFC-23"), ("75-10-5", "HFC-32 (R32)"), ("354-33-6", "HFC-125"), ("811-97-2", "HFC-134a (R134a)"),
    ("420-46-2", "HFC-143a"), ("75-37-6", "HFC-152a"), ("431-89-0", "HFC-227ea"), ("460-73-1", "HFC-245fa"),
    ("406-58-6", "HFC-365mfc"), ("754-12-1", "HFO-1234yf"), ("29118-24-9", "HFO-1234ze(E)"),
    ("2551-62-4", "Sulphur hexafluoride (SF6)"), ("7783-54-2", "Nitrogen trifluoride (NF3)")]
# Well-known PFAS by CAS. Anything else is flagged by name or by the reader's structural check.
PFAS = [
    ("335-67-1", "PFOA"), ("1763-23-1", "PFOS"), ("307-24-4", "PFHxA"), ("355-46-4", "PFHxS"),
    ("375-95-1", "PFNA"), ("13252-13-6", "HFPO-DA (GenX)"), ("647-42-7", "6:2 fluorotelomer alcohol"),
    ("9002-84-0", "PTFE"), ("24937-79-9", "PVDF"), ("25067-11-2", "FEP"), ("26655-00-5", "PFA"), ("9011-17-0", "FKM fluoroelastomer")]

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    meta_path = OUT / "lists.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    with urllib.request.urlopen(urllib.request.Request(HSE_URL, headers=UA), timeout=60) as r:
        uk = parse(r.read())
    meta["uk"] = write("svhc-uk.json", uk, "HSE, UK REACH Candidate List (Excel)", HSE_PAGE)
    print(f"UK: {len(uk)} rows, latest {meta['uk']['latest_inclusion']}")
    if ECHA_FILE.exists():
        eu = parse(ECHA_FILE.read_bytes())
        meta["eu"] = write("svhc-eu.json", eu, "ECHA, Candidate List table (Excel export)", ECHA_PAGE)
        print(f"EU: {len(eu)} rows, latest {meta['eu']['latest_inclusion']}")
    else:
        print("EU: no ECHA file in data/chem/sources; keeping the last EU list" if "eu" in meta else "EU: no ECHA file yet")
    meta["cbam"] = CBAM
    meta["fgas"] = [{"cas": c, "name": n} for c, n in FGAS]
    meta["pfas"] = [{"cas": c, "name": n} for c, n in PFAS]
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")

if __name__ == "__main__":
    main()
