# BASIC TESTS: How we make sure our validation logic works correctly
#
# These tests verify that our system actually catches hallucinations.
# We run these automatically to prevent bugs from creeping in.
# 
# Think of this as the quality control for our quality control system.

import unittest
import sqlite3
from src.mathematical_validation import validate_ai_math
from scripts.init_database import init_db

class TestHallucinationDetection(unittest.TestCase):
    # Tests that prove our system catches AI hallucinations

    def test_catches_fake_segments(self):
        # Does our SQL validation catch segments that don't exist?
        init_db()
        conn = sqlite3.connect('data/sales_data.db')
        cursor = conn.cursor()

        with open('src/sql_validation.sql', 'r') as file:
            sql_query = file.read()
        
        cursor.execute(sql_query)
        results = cursor.fetchall()

        # Look for Europe, which the AI invented
        europe_found = any(row[0] == 'Europe' and row[1] == 'HALLUCINATION' for row in results)

        self.assertTrue(europe_found, "Should have caught 'Europe' as a hallucination")
        conn.close()

        print("✅ Test passed: Successfully caught invented 'Europe' segment")
    
    def test_validates_growth_calculations(self):
        # Does our math validation catch calculation errors?
        # Test with a claim that's way off
        ai_claim = {
            'quarter': '2024Q3',
            'metric': 'revenue',
            'growth_pct': 50.0 # Wildly inaccurate
        }

        result = validate_ai_math("data/sales-data.csv", ai_claim)

        # Should not pass validation
        self.assertNotEqual(result, "All checks passed")
        print("✅ Test passed: Successfully caught inaccurate growth calculation")

if __name__ == '__main__':
    print("Running AI Hallucination Detector tests...")
    unittest.main()