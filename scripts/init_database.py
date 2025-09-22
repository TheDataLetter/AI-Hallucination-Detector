# Before we can catch AI hallucinations, we need to set up our source of truth database. 
# This script create a simple SQLite database with our sales data and AI reports. 

# Think of this as building the reference library that the AI should have consulted. 


import sqlite3
import pandas as pd

def init_db():
    # Create our database file
    # It's like setting up a new filing cabinet
    conn = sqlite3.connect('data/sales_data.db')
    cursor = conn.cursor()

    print("📁 Setting up our source of truth database...")

    # Create a table for our actual sales data
    # This is what the AI is reporting on
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        customer_segment TEXT,
        revenue REAL
    )
    ''')

    # Create a table for the AI's claims
    # We'll compare this against reality
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ai_reports (
        segment_name TEXT, 
        claimed_impact REAL
    )
    ''')

    # Load the real-world data from our CSV files
    sales_df = pd.read_csv('data/sales.csv')
    ai_reports_df = pd.read_csv('data/ai_reports.csv')

    # File the real data in our 'sales' drawer
    sales_df.to_sql('sales', conn, if_exists='replace', index=False)

    # File the AI's claims in our 'ai_reports' drawer
    ai_reports_df.to_sql('ai_reports', conn, if_exists='replace', index=False)

    print("✅ Database ready! We now have:")
    print("   - Real sales data loaded")
    print("   - AI's claims loaded")
    print("   - Everything in place for validation")

    conn.close()

if __name__ == "__main__":
    init_db()