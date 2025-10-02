import os
import json
import xml.etree.ElementTree as ET
import re
from datetime import datetime

RAW_FILE = "../data/raw/modified_sms_v2.xml"
PROCESSED_FILE = "../data/processed/sms_records.json"

def parse_sms_xml(raw_file=RAW_FILE, output_file=PROCESSED_FILE):
    try:
        tree = ET.parse(raw_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []

    sms_list = []

    for i, sms in enumerate(root.findall(".//sms"), start=1):
        record = {
            "id":i,
            "address": sms.get("address", ""),
            "date": sms.get("date", ""),
            "type": sms.get("type", ""),
            "body": sms.get("body", ""),
            "readable_date": sms.get("readable_date", ""),
            "contact_name": sms.get("contact_name", ""),
            "service_center": sms.get("service_center", ""),
            "transaction_id": None
        }

        #Convert timestamp to human readable if date is numeric
        if record["date"].isdigit():
            try:
                ts = int(record["date"]) / 1000
                record["readable_date"] = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S") #year-month-date-hour-mins-secs
            except Exception:
                pass # back to original timestamp

        # Extract Financial Transaction Id from body if present
        body_text = record["body"] or ""
        if "Financial Transaction Id:" in body_text:
            record["transaction_id"] = body_text.split("Financial Transaction Id:")[-1].strip().split()[0]

        sms_list.append(record)

    os.makedirs(os.path.dirname(PROCESSED_FILE), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sms_list, f, indent=4, ensure_ascii=False)

    print(f"Parsed {len(sms_list)}SMS records. Saved to {output_file}")
    return sms_list

if __name__ == "__main__":
    parse_sms_xml()
