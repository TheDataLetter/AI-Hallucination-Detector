AI Hallucination Detector

This repository contains the code for the article My AI gave me fake data. Here’s how to catch it if it happens to you.

It implements a multi-layer validation system to catch AI hallucinations in data analysis, including incorrect calculations and entirely fabricated metrics.

Quick Start

1. Install dependencies:

pip install -r requirements.txt

2. See a hallucination get caught:

python demo.py

This will run the full demo, showing mathematical and SQL-based checks.

3. Launch the contextual audit dashboard:

streamlit run dashboard/app.py

4. Run the production pipeline simulation:

python airflow_simulation.py

5. Run the test suite:

python -m tests.test_basic_validation

## Project Structure

ai-hallucination-detector/

├── 01_demo.py # Main demonstration script

├── 02_airflow_simulation.py # Production pipeline simulator

├── LICENSE # MIT License

├── README.md # Project documentation

├── requirements.txt # Python dependencies

├── data/ # Sample datasets

├── scripts/ # Database initialization utility

├── src/ # Core validation logic

├── tests/ # Unit tests

├── dashboard/ # Streamlit app for visual validation

└── airflow/ # Airflow DAG for automation

What This Demonstrates

• Mathematical Validation: Catches calculation errors and misrepresentations
• Source Verification: Identifies invented dimensions and segments
• Contextual Auditing: Aligns insights with business reality through visual dashboards
• Automated Validation: Production-ready pipeline with retry logic and alerting

System Overview

The detector runs four layers of validation, as described in the article:

1. Mathematical Validation (src/mathematical_validation.py): Catches calculation errors and misrepresentations
2. Source Verification (src/sql_validation.sql): Identifies invented dimensions and segments
3. Contextual Auditing (dashboard/app.py): Aligns insights with business reality through visual dashboards
4. Automated Validation (airflow_simulation.py): Production pipeline with retry logic and alerting

Requirements

• Python 3.6+
• pandas
• streamlit
• plotly

License

This project is licensed under the MIT License - see the LICENSE file for details.

About

This code accompanies the article showing how to build robust validation systems for AI-generated business insights. The system caught a $2M forecasting error in production by detecting invented segments and calculation errors.

