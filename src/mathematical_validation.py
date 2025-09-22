import pandas as pd

def validate_ai_math(data_path, ai_claim):
    # Validates AI calims against actual data in <15 lines.
    # Catches:
    # 1. Incorrect growth calculations
    # 2. Period mismatches
    # 3. Fabricated metrics

    df = pd.read_csv(data_path)
    df['quarter'] = pd.to_datetime(df['date']).dt.to_period('Q')

    # 1. Check period exists
    if ai_claim['quarter'] not in df['quarter'].unique():
        return f"Period mmismatch: No data for {ai_claim['quarter']}"
    
    # 2. Check metric exists
    if ai_claim['metric'] not in df.columns:
        return f"Fabricated metric: '{ai_claim['metric']}' not found"
    
    # 3. Validate growth rate
    current_q = pd.Period(ai_claim['quarter'])
    previous_q = current_q - 1

    current_data = df[df['quarter'] == current_q]
    previous_data = df[df['quarter'] == previous_q]

    if previous_data.empty:
        return f"No data for previous quarter {previous_q}"
    
    current_sum = current_data[ai_claim['metric']].sum()
    previous_sum = previous_data[ai_claim['metric']].sum()

    if previous_sum == 0:
        return "Cannot calculate growth from zero base"
    
    actual_growth = (current_sum - previous_sum) / previous_sum * 100

    if abs(actual_growth - ai_claim['growth_pct']) > 2:
        return f"Growth error: AI claimed {ai_claim['growth_pct']}%, actual was {actual_growth:.1f}%"
    
    return "All checks passed"

# Example usage:
# ai_claim = {
#    'quarter': '2024Q3',    # Try changing to '2024Q4' to test period mismatch
#    'metric': 'revenue',    # Try changing to 'profit' to test fabricated metric
#    'growth_pct': 15.0      # Try changing to see growth errors
# }
# print(validate_ai_math("data/sales-data.csv", ai_claim))