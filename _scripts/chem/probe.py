import re, urllib.request, io
H={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
   "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language":"en-GB,en;q=0.9"}
def get(u):
    r=urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=60); return r.status,r.headers.get("content-type"),r.read()
try:
    s,ct,b=get("https://www.hse.gov.uk/reach/assets/docs/candidate-list.xlsx"); print("HSE xlsx",s,ct,len(b))
    import openpyxl; wb=openpyxl.load_workbook(io.BytesIO(b),read_only=True)
    for ws in wb.worksheets:
        print("sheet",ws.title)
        for i,row in enumerate(ws.iter_rows(values_only=True)):
            if i<8 or i in (100,200): print("  ",i,row[:8])
        print("  rows",i+1)
except Exception as e: print("HSE ERR",e)
for u in ["https://echa.europa.eu/candidate-list-table",
          "https://chem.echa.europa.eu/",
          "https://chem.echa.europa.eu/api-substance/v1/substance?searchText=110-54-3",
          "https://echa.europa.eu/documents/10162/17222/candidate_list_table_en.xlsx",
          "https://data.europa.eu/api/hub/search/search?q=candidate%20list%20substances%20of%20very%20high%20concern&limit=5"]:
    try:
        s,ct,b=get(u); t=b.decode("utf-8","ignore"); print("==",u,s,ct,len(b)); print(t[:600].replace("\n"," "))
        for m in sorted(set(re.findall(r'"(https?://[^"]+(?:xlsx|csv|json)[^"]*)"',t)))[:15]: print("  link:",m)
    except Exception as e: print("==",u,"ERR",e)
