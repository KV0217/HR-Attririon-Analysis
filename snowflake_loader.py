"""
Snowflake Data Warehouse Loader — HR Attrition Analysis
=======================================================
Loads the IBM HR dataset into Snowflake, runs advanced SQL risk
analysis using CTEs, Window Functions and NTILE ranking, and
exports flagged at-risk employees for downstream ML scoring.

Setup:
    pip install snowflake-connector-python pandas python-dotenv

    Create a .env file with:
        SNOWFLAKE_ACCOUNT=<your-account-identifier>
        SNOWFLAKE_USER=<your-username>
        SNOWFLAKE_PASSWORD=<your-password>
        SNOWFLAKE_WAREHOUSE=COMPUTE_WH
        SNOWFLAKE_DATABASE=HR_ANALYTICS
        SNOWFLAKE_SCHEMA=ATTRITION

Usage:
    python snowflake_loader.py
"""

import os
import logging
from pathlib import Path

import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)
logger = logging.getLogger(__name__)

# ── Connection Config ─────────────────────────────────────────────────────────
SNOWFLAKE_CONFIG = {
    "account":   os.getenv("SNOWFLAKE_ACCOUNT"),
    "user":      os.getenv("SNOWFLAKE_USER"),
    "password":  os.getenv("SNOWFLAKE_PASSWORD"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
    "database":  os.getenv("SNOWFLAKE_DATABASE",  "HR_ANALYTICS"),
    "schema":    os.getenv("SNOWFLAKE_SCHEMA",     "ATTRITION"),
}

# ── DDL: Create database, schema, table ──────────────────────────────────────
DDL_SETUP = [
    "CREATE DATABASE IF NOT EXISTS HR_ANALYTICS",
    "CREATE SCHEMA IF NOT EXISTS HR_ANALYTICS.ATTRITION",
    """
    CREATE TABLE IF NOT EXISTS HR_ANALYTICS.ATTRITION.EMPLOYEE_DATA (
        EMPLOYEE_ID                  INTEGER,
        AGE                          INTEGER,
        ATTRITION                    VARCHAR(3),
        BUSINESS_TRAVEL              VARCHAR(50),
        DAILY_RATE                   INTEGER,
        DEPARTMENT                   VARCHAR(50),
        DISTANCE_FROM_HOME           INTEGER,
        EDUCATION                    INTEGER,
        EDUCATION_FIELD              VARCHAR(50),
        ENVIRONMENT_SATISFACTION     INTEGER,
        GENDER                       VARCHAR(10),
        HOURLY_RATE                  INTEGER,
        JOB_INVOLVEMENT              INTEGER,
        JOB_LEVEL                    INTEGER,
        JOB_ROLE                     VARCHAR(50),
        JOB_SATISFACTION             INTEGER,
        MARITAL_STATUS               VARCHAR(20),
        MONTHLY_INCOME               INTEGER,
        MONTHLY_RATE                 INTEGER,
        NUM_COMPANIES_WORKED         INTEGER,
        OVER_TIME                    VARCHAR(3),
        PERCENT_SALARY_HIKE          INTEGER,
        PERFORMANCE_RATING           INTEGER,
        RELATIONSHIP_SATISFACTION    INTEGER,
        STANDARD_HOURS               INTEGER,
        STOCK_OPTION_LEVEL           INTEGER,
        TOTAL_WORKING_YEARS          INTEGER,
        TRAINING_TIMES_LAST_YEAR     INTEGER,
        WORK_LIFE_BALANCE            INTEGER,
        YEARS_AT_COMPANY             INTEGER,
        YEARS_IN_CURRENT_ROLE        INTEGER,
        YEARS_SINCE_LAST_PROMOTION   INTEGER,
        YEARS_WITH_CURR_MANAGER      INTEGER,
        LOADED_AT                    TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
    )
    """,
]

# ── Advanced SQL Risk Analysis ────────────────────────────────────────────────
RISK_ANALYSIS_SQL = """
WITH risk_scoring AS (
    SELECT
        EMPLOYEE_ID,
        DEPARTMENT,
        JOB_ROLE,
        MONTHLY_INCOME,
        OVER_TIME,
        YEARS_SINCE_LAST_PROMOTION,
        JOB_SATISFACTION,
        WORK_LIFE_BALANCE,
        ATTRITION,
        (
            CASE WHEN OVER_TIME = 'Yes'                    THEN 3 ELSE 0 END
          + CASE WHEN YEARS_SINCE_LAST_PROMOTION > 4       THEN 2 ELSE 0 END
          + CASE WHEN JOB_SATISFACTION <= 2                THEN 2 ELSE 0 END
          + CASE WHEN WORK_LIFE_BALANCE = 1                THEN 2 ELSE 0 END
          + CASE WHEN YEARS_SINCE_LAST_PROMOTION > 7       THEN 1 ELSE 0 END
        ) AS RISK_SCORE
    FROM HR_ANALYTICS.ATTRITION.EMPLOYEE_DATA
),

dept_attrition AS (
    SELECT
        DEPARTMENT,
        JOB_ROLE,
        COUNT(*) AS TOTAL_EMPLOYEES,
        SUM(CASE WHEN ATTRITION = 'Yes' THEN 1 ELSE 0 END) AS ATTRITED,
        ROUND(
            100.0 * SUM(CASE WHEN ATTRITION = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2
        ) AS ATTRITION_RATE_PCT
    FROM HR_ANALYTICS.ATTRITION.EMPLOYEE_DATA
    GROUP BY DEPARTMENT, JOB_ROLE
),

cost_of_attrition AS (
    SELECT
        DEPARTMENT,
        COUNT(*) AS TOTAL_HEADCOUNT,
        SUM(CASE WHEN ATTRITION = 'Yes' THEN 1 ELSE 0 END) AS ATTRITED_COUNT,
        ROUND(AVG(MONTHLY_INCOME) * 12, 0)                 AS AVG_ANNUAL_SALARY,
        -- 150% salary replacement model
        ROUND(
            SUM(CASE WHEN ATTRITION = 'Yes' THEN MONTHLY_INCOME * 12 * 1.5 ELSE 0 END), 0
        ) AS TOTAL_REPLACEMENT_COST_USD
    FROM HR_ANALYTICS.ATTRITION.EMPLOYEE_DATA
    GROUP BY DEPARTMENT
),

ranked AS (
    SELECT
        r.EMPLOYEE_ID,
        r.DEPARTMENT,
        r.JOB_ROLE,
        r.MONTHLY_INCOME,
        r.OVER_TIME,
        r.YEARS_SINCE_LAST_PROMOTION,
        r.JOB_SATISFACTION,
        r.WORK_LIFE_BALANCE,
        r.ATTRITION,
        r.RISK_SCORE,
        NTILE(4) OVER (ORDER BY r.RISK_SCORE DESC)                     AS RISK_QUARTILE,
        ROW_NUMBER() OVER (PARTITION BY r.DEPARTMENT ORDER BY r.RISK_SCORE DESC)
                                                                        AS DEPT_RISK_RANK,
        c.TOTAL_REPLACEMENT_COST_USD,
        d.ATTRITION_RATE_PCT                                            AS DEPT_ATTRITION_RATE_PCT
    FROM risk_scoring r
    JOIN cost_of_attrition c USING (DEPARTMENT)
    JOIN dept_attrition     d USING (DEPARTMENT, JOB_ROLE)
)

SELECT *
FROM   ranked
WHERE  RISK_QUARTILE = 1          -- top 25% highest-risk employees
ORDER  BY RISK_SCORE DESC, MONTHLY_INCOME DESC;
"""

OVERTIME_MATRIX_SQL = """
-- Overtime × JobLevel attrition matrix (replicates the notebook heatmap in SQL)
SELECT
    JOB_LEVEL,
    OVER_TIME,
    COUNT(*)                                                               AS TOTAL,
    SUM(CASE WHEN ATTRITION = 'Yes' THEN 1 ELSE 0 END)                    AS ATTRITED,
    ROUND(
        100.0 * SUM(CASE WHEN ATTRITION = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2
    )                                                                      AS ATTRITION_RATE_PCT
FROM HR_ANALYTICS.ATTRITION.EMPLOYEE_DATA
GROUP BY JOB_LEVEL, OVER_TIME
ORDER BY JOB_LEVEL, OVER_TIME;
"""


# ── Core Functions ────────────────────────────────────────────────────────────

def get_connection() -> snowflake.connector.SnowflakeConnection:
    logger.info("Connecting to Snowflake …")
    conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
    logger.info(f"Connected  →  account: {SNOWFLAKE_CONFIG['account']}")
    return conn


def setup_warehouse(conn: snowflake.connector.SnowflakeConnection) -> None:
    """Create the HR_ANALYTICS database, ATTRITION schema, and EMPLOYEE_DATA table."""
    logger.info("Setting up Snowflake schema …")
    cur = conn.cursor()
    for stmt in DDL_SETUP:
        cur.execute(stmt.strip())
    cur.close()
    logger.info("Schema ready.")


def load_hr_data(
    conn: snowflake.connector.SnowflakeConnection,
    csv_path: str = "data/WA_Fn-UseC_-HR-Employee-Attrition.csv",
) -> pd.DataFrame:
    """Read the IBM HR CSV and bulk-load it into Snowflake via write_pandas."""
    logger.info(f"Reading dataset from {csv_path} …")
    df = pd.read_csv(csv_path)

    # Snowflake expects uppercase column names
    df.columns = [c.upper().replace(" ", "_") for c in df.columns]
    df.insert(0, "EMPLOYEE_ID", range(1, len(df) + 1))

    # Drop columns Snowflake rejects (constant value in IBM dataset)
    df.drop(columns=["OVER_18", "STANDARD_HOURS"], errors="ignore", inplace=True)

    cur = conn.cursor()
    cur.execute("USE DATABASE HR_ANALYTICS")
    cur.execute("USE SCHEMA ATTRITION")
    cur.close()

    success, nchunks, nrows, _ = write_pandas(
        conn, df, "EMPLOYEE_DATA", auto_create_table=False, overwrite=True
    )
    logger.info(f"Loaded {nrows} rows  |  {nchunks} chunk(s)  |  success={success}")
    return df


def run_query(conn: snowflake.connector.SnowflakeConnection, sql: str) -> pd.DataFrame:
    cur = conn.cursor()
    cur.execute(sql)
    df = cur.fetch_pandas_all()
    cur.close()
    return df


def export_results(df: pd.DataFrame, output_path: str = "outputs/snowflake_risk_report.csv") -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Report saved → {output_path}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    conn = get_connection()
    try:
        setup_warehouse(conn)
        load_hr_data(conn)

        logger.info("Running risk analysis SQL …")
        risk_df = run_query(conn, RISK_ANALYSIS_SQL)
        export_results(risk_df, "outputs/snowflake_risk_report.csv")

        logger.info("Running overtime matrix SQL …")
        overtime_df = run_query(conn, OVERTIME_MATRIX_SQL)
        export_results(overtime_df, "outputs/snowflake_overtime_matrix.csv")

        print("\n══════════════════════════════════════════")
        print("  TOP 10 HIGH-RISK EMPLOYEES (Snowflake)")
        print("══════════════════════════════════════════")
        print(risk_df.head(10).to_string(index=False))

        print("\n══════════════════════════")
        print("  OVERTIME × JOB LEVEL")
        print("══════════════════════════")
        print(overtime_df.to_string(index=False))

    finally:
        conn.close()
        logger.info("Snowflake connection closed.")


if __name__ == "__main__":
    main()
