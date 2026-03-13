import csv
import io
from datetime import datetime
from typing import List, Dict

# Mock data
MOCK_TRANSACTIONS_RAW = [
    {"date": "2024-01-03", "description": "Salary Deposit",    "amount":  4500.00, "type": "income"},
    {"date": "2024-01-05", "description": "Rent Payment",      "amount": -1400.00, "type": "housing"},
    {"date": "2024-01-06", "description": "Whole Foods",       "amount":   -87.00, "type": "food"},
    {"date": "2024-01-08", "description": "Netflix",           "amount":   -15.99, "type": "subscription"},
    {"date": "2024-01-08", "description": "Spotify",           "amount":    -9.99, "type": "subscription"},
    {"date": "2024-01-09", "description": "Uber Eats",         "amount":   -34.50, "type": "food"},
    {"date": "2024-01-10", "description": "Amazon Prime",      "amount":   -14.99, "type": "subscription"},
    {"date": "2024-01-11", "description": "Gas Station",       "amount":   -52.00, "type": "transport"},
    {"date": "2024-01-12", "description": "Gym Membership",    "amount":   -49.00, "type": "subscription"},
    {"date": "2024-01-14", "description": "Restaurant Dinner", "amount":   -78.00, "type": "food"},
    {"date": "2024-01-15", "description": "Savings Transfer",  "amount":  -500.00, "type": "savings"},
    {"date": "2024-01-17", "description": "Electric Bill",     "amount":   -95.00, "type": "utilities"},
    {"date": "2024-01-18", "description": "Starbucks",         "amount":    -6.50, "type": "food"},
    {"date": "2024-01-19", "description": "Adobe Creative",    "amount":   -54.99, "type": "subscription"},
    {"date": "2024-01-20", "description": "CVS Pharmacy",      "amount":   -23.00, "type": "health"},
    {"date": "2024-01-22", "description": "Target",            "amount":  -112.00, "type": "shopping"},
    {"date": "2024-01-23", "description": "Internet Bill",     "amount":   -79.00, "type": "utilities"},
    {"date": "2024-01-25", "description": "Freelance Income",  "amount":   800.00, "type": "income"},
    {"date": "2024-01-26", "description": "Uber Ride",         "amount":   -18.00, "type": "transport"},
    {"date": "2024-01-28", "description": "Hulu",              "amount":   -17.99, "type": "subscription"},
    {"date": "2024-02-03", "description": "Salary Deposit",    "amount":  4500.00, "type": "income"},
    {"date": "2024-02-05", "description": "Rent Payment",      "amount": -1400.00, "type": "housing"},
    {"date": "2024-02-07", "description": "Trader Joe's",      "amount":   -93.00, "type": "food"},
    {"date": "2024-02-08", "description": "Netflix",           "amount":   -15.99, "type": "subscription"},
    {"date": "2024-02-08", "description": "Spotify",           "amount":    -9.99, "type": "subscription"},
    {"date": "2024-02-10", "description": "Amazon Prime",      "amount":   -14.99, "type": "subscription"},
    {"date": "2024-02-11", "description": "Gas Station",       "amount":   -48.00, "type": "transport"},
    {"date": "2024-02-12", "description": "Gym Membership",    "amount":   -49.00, "type": "subscription"},
    {"date": "2024-02-14", "description": "Valentine's Dinner","amount":  -145.00, "type": "food"},
    {"date": "2024-02-15", "description": "Savings Transfer",  "amount":  -500.00, "type": "savings"},
    {"date": "2024-02-17", "description": "Electric Bill",     "amount":  -102.00, "type": "utilities"},
    {"date": "2024-02-19", "description": "Adobe Creative",    "amount":   -54.99, "type": "subscription"},
    {"date": "2024-02-21", "description": "Clothing Store",    "amount":  -189.00, "type": "shopping"},
    {"date": "2024-02-23", "description": "Internet Bill",     "amount":   -79.00, "type": "utilities"},
    {"date": "2024-02-25", "description": "Doctor Visit",      "amount":   -40.00, "type": "health"},
    {"date": "2024-02-26", "description": "Hulu",              "amount":   -17.99, "type": "subscription"},
    {"date": "2024-02-28", "description": "Uber Eats",         "amount":   -28.00, "type": "food"},
    {"date": "2024-03-03", "description": "Salary Deposit",    "amount":  4500.00, "type": "income"},
    {"date": "2024-03-05", "description": "Rent Payment",      "amount": -1400.00, "type": "housing"},
    {"date": "2024-03-06", "description": "Whole Foods",       "amount":  -104.00, "type": "food"},
    {"date": "2024-03-08", "description": "Netflix",           "amount":   -15.99, "type": "subscription"},
    {"date": "2024-03-08", "description": "Spotify",           "amount":    -9.99, "type": "subscription"},
    {"date": "2024-03-09", "description": "Amazon Prime",      "amount":   -14.99, "type": "subscription"},
    {"date": "2024-03-10", "description": "Gas Station",       "amount":   -61.00, "type": "transport"},
    {"date": "2024-03-11", "description": "Gym Membership",    "amount":   -49.00, "type": "subscription"},
    {"date": "2024-03-12", "description": "Disney+",           "amount":   -13.99, "type": "subscription"},
    {"date": "2024-03-14", "description": "Restaurant",        "amount":   -67.00, "type": "food"},
    {"date": "2024-03-15", "description": "Savings Transfer",  "amount":  -600.00, "type": "savings"},
    {"date": "2024-03-17", "description": "Electric Bill",     "amount":   -88.00, "type": "utilities"},
    {"date": "2024-03-18", "description": "Starbucks",         "amount":    -7.50, "type": "food"},
    {"date": "2024-03-19", "description": "Adobe Creative",    "amount":   -54.99, "type": "subscription"},
    {"date": "2024-03-22", "description": "Amazon Shopping",   "amount":  -234.00, "type": "shopping"},
    {"date": "2024-03-23", "description": "Internet Bill",     "amount":   -79.00, "type": "utilities"},
    {"date": "2024-03-25", "description": "Freelance Income",  "amount":  1200.00, "type": "income"},
    {"date": "2024-03-26", "description": "Hulu",              "amount":   -17.99, "type": "subscription"},
    {"date": "2024-03-28", "description": "Pharmacy",          "amount":   -31.00, "type": "health"},
]


# Ingestion Functions
def load_mock_data()->list[Dict]:
    return [dict(t) for t in MOCK_TRANSACTIONS_RAW]

def load_from_csv_string(csv_text: str) -> List[Dict]:
    '''
    Parse a CSV string into raw transaction dicts.
    Expected Columns: date , description, amount
    Optional column: type / category
    '''

    reader = csv.DictReader(io.StringIO(csv_text.strip()))
    rows = []

    for row in reader:
        normalised = {k.strip().lower(): v.strip() for k, v in row.items()}
        try:
            amount =float(normalised.get('amount') or normalised.get('value') or 0)
        except ValueError:
            continue

        rows.append({
            "date":normalised.get('date','2024-01-01'),
            "description": normalised.get("description") or normalised.get("merchant") or normalised.get('name') or "Unknown",
            "amount": amount,
            "type" : normalised.get('type') or normalised.get('category') or "",
        })

    return rows



def load_from_csv_file(filepath:str)->List[Dict]:
    with open(filepath,'r',encoding='utf-8') as f:
        return load_from_csv_string(f.read())
    
