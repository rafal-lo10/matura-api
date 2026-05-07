import pdfplumber
import json
import re

pdf = pdfplumber.open("matura.pdf")
events = []

pattern = re.compile(r"(\d{1,2})\s+([A-Za-ząćęłńóśźż]+)\s+(\d{4})")

months = {
    "stycznia": "01", "lutego": "02", "marca": "03", "kwietnia": "04",
    "maja": "05", "czerwca": "06", "lipca": "07", "sierpnia": "08",
    "września": "09", "października": "10", "listopada": "11", "grudnia": "12"
}

for page in pdf.pages:
    text = page.extract_text()
    if not text:
        continue

    for line in text.split("\n"):
        m = pattern.search(line)
        if m:
            day, month_name, year = m.groups()
            month = months.get(month_name.lower())
            if month:
                date = f"{year}-{month}-{int(day):02d}"
                events.append({
                    "date": date,
                    "title": line.strip(),
                    "type": "M"
                })

print(json.dumps(events, ensure_ascii=False, indent=2))
