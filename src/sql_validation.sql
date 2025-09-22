-- Layer 2: Source Verification (Postgres/Redshift/BigQuery compatible)
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
    ai_reports.claimed_impact -- Shows AI's claimed impact
FROM ai_reports
LEFT JOIN valid_segments
    ON ai_reports.segment_name = valid_Segments.customer_segment