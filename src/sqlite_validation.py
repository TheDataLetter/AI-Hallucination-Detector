import sqlite3

# Create a SQLite database in memory
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create the sales table
cursor.execute('''
CREATE TABLE sales (
    customer_segment TEXT,
    revenue INTEGER
)
''')

# Create the ai_reports table
cursor.execute('''
CREATE TABLE ai_reports (
    segment_name TEXT, 
    claimed_impact INTEGER
)
''')

# Insert sample data into sales table
sales_data = [
    ('North America', 100000),
    ('Asisa', 80000),
    ('Africa', 50000)
]

cursor.executemany('INSERT INTO sales VALUES (?, ?)', sales_data)

# Insert sample data into ai_reports table
ai_reports_data = [
    ('North America', 10),
    ('Europe', 15),
    ('Asia', 8)
]

cursor.executemany('INSERT INTO ai_reports VALUES (?, ?)', ai_reports_data)

query = '''
WITH valid_segments AS (
    SELECT
        customer_segment, 
        SUM(revenue) AS segment_revenue
    FROM sales
    GROUP BY customer_segment
    HAVING SUM(revenue) > 10000 -- Filters out insignificant segments
)

SELECT
    ai_reports.segment_name,
    CASE
        WHEN valid_segments.customer_segment IS NULL THEN 'HALLUCINATION'
        ELSE 'VALID'
    END AS status, 
    ai_reports.claimed_impact --Shows AI's claimed impact
FROM ai_reports
LEFT JOIN valid_segments
    ON ai_reports.segment_name = valid_segments.customer_segment
'''

cursor.execute(query)
results = cursor.fetchall()

# Print the results
print("SQL Validation Results:")
print("Segment Name\tStatus\t\tClaimed Impact")
print("-" * 40)
for row in results:
    segment, status, impact = row
    print(f"{segment}\t\t{status}\t{impact}")

# Close the connection
conn.close()