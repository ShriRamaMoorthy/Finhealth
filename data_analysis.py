from collections import defaultdict
from typing import List, Dict, Any

def compute_aggregates(transactions:List[Dict]) -> Dict[str,float]:
    # compute top-level financial aggregates across the entire dataset
    # Returns : income, expense, savings totals+derived ratios

    income = sum(t["amount"] for t in transactions if t['amount']>0)
    savings = sum(abs(t["amount"]) for t in transactions if t['type']=='savings')
    expenses = sum(abs(t['amount']) for t in transactions if t['amount'] < 0 and t['type']!='savings')

    savings_rate = round((savings/income*100),2) if income else 0.0
    expense_ratio = round((expenses / income * 100),2) if income else 0.0

    months_of_data = _count_months(transactions)
    avg_monthly_expense = expenses / months_of_data if months_of_data else expenses
    emergency_months = round(savings / avg_monthly_expense, 2) if avg_monthly_expense else 0.0

    return {
        "income": round(income,2),
        "expenses": round(expenses,2),
        "savings": round(savings,2),
        "savings_rate": savings_rate,
        "expense_ratio": expense_ratio,
        "emergency_months": emergency_months,
        "months_of_data": months_of_data,
    }

def _count_months(transactions: List[Dict]) -> int:
    # Count distinct YYYY-MM periods present in the dataset
    months = {t['date'][:7] for t in transactions}
    return max(len(months),1)

# Category Breakdown
def compute_category_totals(transactions: List[Dict]):
    '''
    captures sum spending per category (excludes income and savings)
    Returns a list of {name,value} dicts sorted by values descending. 
    '''
    totals: Dict[str,float] = defaultdict(float)
    for t in transactions:
        if t['amount'] < 0 and t['type'] not in ('savings',):
            totals[t['type']] += abs(t['amount'])
    return sorted(
        [{'name':cat, 'value':round(val,2)} for cat,val in totals.items()],
        key=lambda x:x['value'],
        reverse=True,
    )



# Monthly Trends
def compute_monthly_trends(transactions: List[Dict]) -> List[Dict]:
    '''
    Aggregate transactions by YYYY-MM into income/expenses/savings buckets
    Returns list of monthly summary dicts, sorted chronologically
    '''
    monthly: Dict[str, Dict[str,float]] = defaultdict(lambda: {'income':0.0, 'expenses':0.0, 'savings':0.0})

    for t in transactions:
        month = t['date'][:7]
        if t['amount']>0:
            monthly['month']['income'] += t['amount']
        elif t['type']=='savings':
            monthly['month']['savings'] += abs(t['amount'])
        else:
            monthly[month]['expenses'] += abs(t['amount'])
    
    return[{
        'month':month,
        'income':round(data['income'],2),
        'expenses':round(data['expenses'],2),
        'savings':round(data['savings'],2)
    }
    for month,data in sorted(monthly.items())
    ]


# subscription analysis
def compute_subscriptions(transactions: List[Dict]) -> Dict[str,Any]:
    '''
    Identify all recurring subscription charges.
    Returns per-service breakdown + totals
    '''
    sub_map: Dict[str,Dict] = {}

    for t in transactions:
        if t['type']!='subscription':
            continue
        name=t['description']
        if name not in sub_map:
            sub_map[name] = {'name':name, 'monhtly':abs(t['amount']), 'count':0}
        sub_map[name]['count']+=1
    
    services = sorted(sub_map.values(), key=lambda x:x['monthly'], reverse=True)
    total_monthly = round(sum(s['monthly'] for s in services),2)
    total_annual = round(total_monthly*12,2)

    return{
        'services': services,
        'count':len(services),
        'total_monthly':total_monthly,
        'total_annual':total_annual
    }

# Anomaly Detection
def detect_anomalies(transactions: List[Dict]) -> List[Dict]:
    '''
    Detect unusually large spending transactions using a simple

    '''
    category_amounts: Dict[str,List[float]] = defaultdict(list)
    for t in transactions:
        if t['amount']<0:
            category_amounts[t['type']].append(abs(t['amount']))
    
    anomalies=[]
    for t in transactions:
        if t['amount']>=0:
            continue
        amounts=category_amounts[t['type']]
        if len(amounts) < 2:
            continue
        avg = sum(amounts) / len(amounts)
        if abs(t['amount']) > avg*1.8:
            anomalies.append({
                "date":t['date'],
                'description':t['description'],
                'amount':abs(t['amount']),
                'category':t['type'],
                'avg_for_cat':round(avg,2)
            })

    return anomalies