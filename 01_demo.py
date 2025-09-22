# MAIN DEMO: See the AI Hallucination Detector in action
#
# We'll run both validation layers and watch as they catch 
# the AI's creative accounting and invented segments.
#
# Run this file first to see the system work end to end.

from src.mathematical_validation import validate_ai_math
from scripts.init_database import init_db
import sqlite3

def main():
    print("🚨 AI HALLUCINATION DETECTOR")
    print("============================")
    print("This demo recreates the system that caught a $2M forecasting error.")
    print("We'll check the AI's math and whether its segments actually exist.\n")

    # Step 1: Set up our reference database
    print("1. 📊 Loading our reference data...")
    init_db()
    print("   ✅ Ground truth data loaded\n")

    # Step 2: Check the AI's calculations
    print("2. 🧮 Checking the AI's math...")

    # This is the exact claim that made me suspicious in the real project
    ai_claim = {
        'quarter': '2024Q3',
        'metric': 'revenue',
        'growth_pct': 15.0 # The AI claimed 15% growth. Let's check the numbers
    }

    result = validate_ai_math("data/sales-data.csv", ai_claim)

    if result != "All checks passed":
        print(f"    ❌ CAUGHT: {result}")
        print("     The AI's growth calculation doesn't match reality.\n")
    else:
        print("     ✅ Math checks out. The numbers add up\n")
    
    # Step 3: Verify the AI didn't invent segments
    print("3. 🔍 Checking if the AI's segments actually exist...")
    conn = sqlite3.connect('data/sales_data.db')
    cursor = conn.cursor()

    # This SQL query is the heart of our source verification
    with open('src/sql_validation.sql', 'r') as file:
        sql_query = file.read()
    
    cursor.execute(sql_query)
    results = cursor.fetchall()

    # Show readers exactly what we found
    print("   Segment validation results:")
    print("   " + "-" * 40)

    for row in results:
        segment, status, impact = row
        if status == 'HALLUCINATION':
            print(f"    ❌ {segment}: HALLUCINATION (claimed {impact}% impact)")
            print(f"       This segment doesn't exist in our sales data!")
        else: 
            print(f"    ✅ {segment}: Valid (claimed {impact}% impact)")
    
    conn.close()

    print("\n" + "="*50)
    print("🎯 DEMO COMPLETE")
    print("This is exactly how we caught the AI inventing European sales data.")
    print("The system flagged both calculation errors and fabricated segments.")

if __name__ == "__main__":
    main()
