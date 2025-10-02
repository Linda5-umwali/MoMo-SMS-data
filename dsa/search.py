import json
import os
import time
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_FILE = REPO_ROOT / "data" / "processed" / "sms_records.json"

# Load SMS records from JSON
def load_sms():
    with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Build dictionary for O(1) lookup
def build_dict(sms_list):
    return {sms["transaction_id"]: sms for sms in sms_list if sms["transaction_id"]}

# Linear Search
def linear_search(sms_list, transaction_id):
    for sms in sms_list:
        if sms["transaction_id"] == transaction_id:
            return sms
    return None

# Dictionary Lookup
def dict_lookup(sms_dict, transaction_id):
    return sms_dict.get(transaction_id, None)

def main():
    sms_list = load_sms()
    sms_dict = build_dict(sms_list)

    # Use first 20 records for testing
    test_ids = [sms["transaction_id"] for sms in sms_list[:20] if sms["transaction_id"]]

    linear_times = []
    dict_times = []

    for tid in test_ids:
        # Linear search timing
        start = time.time()
        linear_search(sms_list, tid)
        linear_times.append(time.time() - start)

        # Dictionary lookup timing
        start = time.time()
        dict_lookup(sms_dict, tid)
        dict_times.append(time.time() - start)

    avg_linear = sum(linear_times) / len(linear_times)
    avg_dict = sum(dict_times) / len(dict_times)

    print("=== DSA Comparison: Linear Search vs Dictionary Lookup ===")
    print(f"Average Linear Search Time: {avg_linear*1e6:.2f} μs")
    print(f"Average Dictionary Lookup Time: {avg_dict*1e6:.2f} μs")
    print(f"Dictionary lookup is approximately {avg_linear/avg_dict:.1f} times faster than linear search.\n")


if __name__ == "__main__":
    main()
