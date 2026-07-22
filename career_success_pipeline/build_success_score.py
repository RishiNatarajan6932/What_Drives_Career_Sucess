"""Compute the Actual Success score for 2023 NSCG respondents.

Implements the methodology in CLAUDE.md:
    Actual Success = (1/3 * Salary_Percentile)
                    + (1/3 * Job_Satisfaction_Score)
                    + (1/3 * Upper_Management_Score)
"""
from pathlib import Path

import pandas as pd

RAW_DATA = Path(__file__).resolve().parents[1] / "pcg23Public" / "epcg23.csv"
OUTPUT_FILE = Path(__file__).resolve().parent / "output" / "nscg23_actual_success.csv"

SALARY_LOGICAL_SKIP = 9999998
JOBSATIS_TO_SCORE = {1: 1.00, 2: 0.67, 3: 0.33, 4: 0.00}
SUPWK_TO_SCORE = {"Y": 1.0, "1": 1.0, "N": 0.0, "2": 0.0}


def load_raw() -> pd.DataFrame:
    return pd.read_csv(RAW_DATA, low_memory=False)


def compute_actual_success(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["SALARY"] = pd.to_numeric(df["SALARY"], errors="coerce")

    employed = (
        (df["JOBSATIS"].astype(str) != "L")
        & (df["SUPWK"].astype(str) != "L")
        & (df["SALARY"] != SALARY_LOGICAL_SKIP)
        & (df["SALARY"] > 0)
    )
    df = df[employed].copy()

    df["SALARY_PERCENTILE"] = df["SALARY"].rank(pct=True)
    df["JOBSATIS_SCORE"] = pd.to_numeric(df["JOBSATIS"], errors="coerce").map(JOBSATIS_TO_SCORE)
    df["SUPWK_SCORE"] = df["SUPWK"].astype(str).map(SUPWK_TO_SCORE)

    df = df.dropna(subset=["SALARY_PERCENTILE", "JOBSATIS_SCORE", "SUPWK_SCORE"])

    df["ACTUAL_SUCCESS"] = (
        df["SALARY_PERCENTILE"] + df["JOBSATIS_SCORE"] + df["SUPWK_SCORE"]
    ) / 3

    return df


def main() -> None:
    df = load_raw()
    scored = compute_actual_success(df)
    
    # Strictly select ONLY your 5 target columns
    target_cols = [
        "SALARY", 
        "SALARY_PERCENTILE", 
        "JOBSATIS_SCORE", 
        "SUPWK_SCORE", 
        "ACTUAL_SUCCESS"
    ]
    
    output_df = scored[target_cols]
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"Wrote {len(output_df)} scored rows to {OUTPUT_FILE}")
    print("\n--- Preview of Output Table ---")
    print(output_df.head(10))


if __name__ == "__main__":
    main()