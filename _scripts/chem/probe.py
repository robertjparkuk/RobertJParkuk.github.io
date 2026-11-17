# Temporary probe: what do the official list pages return to a GitHub runner?
import re, urllib.request, sys
H={"User-Agent":"Mozilla/5.0 (compatible; robertjpark.co.uk list builder)"}
for u in ["https://www.hse.gov.uk/reach/candidate-list.htm",
          "https://echa.europa.eu/candidate-list-table",
          "https://echa.europa.eu/candidate-list-table?p_p_id=disslists_WAR_disslistsportlet&_disslists_WAR_disslistsportlet_delta=500"]:
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=60); b=r.read().decode("utf-8","ignore")
        print("==",u,r.status,len(b))
        print("tables:",b.count("<table"),"rows:",b.count("<tr"),"CAS-like:",len(set(re.findall(r"\b\d{2,7}-\d{2}-\d\b",b))))
        for m in sorted(set(re.findall(r'href="([^"]+)"',b))):
            if re.search(r"xls|csv|export|download|candidate",m,re.I): print("  link:",m[:300])
        i=b.find("<table"); print(b[i:i+1500] if i>=0 else b[:800])
    except Exception as e: print("==",u,"ERR",e)
