# PRODUCTION PIPELINE SIMULATION: How we automate this in real companies
# How we automate detection in real companies
#
# This runs daily in production with retries, alerting,
# and all the safety nets we built.
# 
# Think of this as the autopilot version of our demo.

import time
import sqlite3
from src.mathematical_validation import validate_ai_math
from scripts.init_database import init_db

def run_complete_validation():
    # This function runs the same checks as our demo, 
    # but with production grade safety

    print("🔧 Running production validation pipeline...")

    # First check: Verify the AI's calculations
    ai_claim = {
        'quarter': '2024Q3',
        'metric': 'revenue',
        'growth_pct': 15.0
    }

    math_result = validate_ai_math("data/sales-data.csv", ai_claim)
    if math_result != "All checks passed":
        return f"Math error: {math_result}"

    # Second check: Verify the AI's segments exist
    init_db()
    conn = sqlite3.connect('data/sales_data.db')

    with open ('src/sql.validation.sql', 'r') as file:
        sql_query = file.read()

    cursor = conn.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()

    # If we find any hallucinations, we need to alert the team
    hallucinations = [row for row in results if row[1] == 'HALLUCINATION']
    if hallucinations:
        conn.close()
        return f"Found {len(hallucinations)} invented segments"
    
    conn.close()
    return "All checks passed"

def main():
    print("🏭 PRODUCTION PIPELINE SIMULATION")
    print("=================================")
    print("This mimics how Fortune 500 companies run these checks daily.")
    print("")
    print("Key safety features built in:")
    print("• 3 automatic retries between retries (avoids overwhelming systems)")
    print("• 15-minute delays between retries (avoids overwhelming systems)")
    print("• Email alerts for any failures (so humans can investigate)")
    print("")
    print("-" * 50)

    # Real production systems try multiple times before giving up
    # This handles temporary glitches like database timeouts
    for attempt in range(3):
        try:
            print(f"Attempt {attempt + 1} of 3...")
            result = run_complete_validation()

            if result == "All checks passed":
                print("✅ VALIDATION PASSED")
                print("✅ Report sent to leadership dashboard")
                return True
            else:
                # If we find issues, we raise an error to trigger retries
                raise ValueError(result)
        
        except Exception as e:
            print(f"❌ Validation failed: {e}")

            if attempt < 2:
                print("💤 Waiting 15 minutes before retry...")
                time.sleep(2)  # Shorter delay for demo purposes
                print("")
            else:
                print("🔥 All retries exhausted")
            
    # If we get here, all attempts failed and we need human intervention
    print("")
    print("🚨 CRITICAL: Sending alert email to data team")
    print("📧 Subject: AI Validation Failed - Human Review Required")
    print("💬 Message: The AI generated suspicious data. Please investigate.")

    return False

if __name__ == "__main__":
    success = main()

