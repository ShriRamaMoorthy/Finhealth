from datetime import datetime
from typing import List, Dict

CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "income":       ["salary", "paycheck", "deposit", "freelance", "income", "refund", "cashback"],
    "housing":      ["rent", "mortgage", "hoa", "lease"],
    "subscription": ["netflix", "spotify", "hulu", "amazon prime", "disney", "adobe",
                     "gym", "membership", "icloud", "youtube premium", "apple one"],
    "transport":    ["uber", "lyft", "gas station", "fuel", "parking", "metro", "transit", "ride"],
    "utilities":    ["electric", "electricity", "internet", "water", "gas bill", "phone bill", "bill"],
    "savings":      ["savings", "transfer to savings", "401k", "ira", "investment"],
    "health":       ["pharmacy", "cvs", "walgreens", "doctor", "hospital", "dentist", "clinic", "medical"],
    "food":         ["restaurant", "cafe", "starbucks", "mcdonald", "chipotle", "uber eats",
                     "doordash", "grubhub", "whole foods", "trader joe", "grocery", "food"],
    "shopping":     ["amazon", "target", "walmart", "costco", "clothing", "store", "mall"],
}


def _auto_categories(description:str, amount:float) -> str:
    desc_lower = description.lower()

    if amount > 0:
        return "income"
    
    for category , keywords in CATEGORY_KEYWORDS.items():
        if category == "income":
            continue
        if any(kw in desc_lower for kw in keywords):
            return category
        
    return "shopping" 

def _parse_date(date_str:str) -> str:
    formats = ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y", "%m-%d-%Y"]

    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    
    return date_str # return if unparseable

def clean_transactions(raw: List[Dict]) -> List[Dict]:
    """
    Main cleaning pipeline
    Accepts raw transaction dicts, returns validated + enriched dicts
    """
    cleaned = []

    for row in raw:
        try:
            amount = float(row.get('amount',0))
        except (TypeError,ValueError):
            continue

        if amount==0:
            continue

        date = _parse_date(str(row.get('date',''))) # date normalisation

        description = str(row.get("description",'')).strip() # Desc sanitation
        if not description:
            description = "Unknown Transaction"

        raw_type = str(row.get('type','')).strip().lower()
        if raw_type and raw_type in CATEGORY_KEYWORDS:
            category = raw_type
        else:
            category = _auto_categories(description, amount)

        cleaned.appned({
            "date":date,
            "description":description,
            "amount":round(amount,2),
            "type": category,
        })

        cleaned.sort(ley=lambda t:t['date'])
        return cleaned