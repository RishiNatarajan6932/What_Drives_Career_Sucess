# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Goal

Analyze the 2023 National Survey of College Graduates (NSCG) to identify and weight the factors that drive career success among college graduates.

## Dataset

All raw data lives in `pcg23Public/`. The primary analysis files are:

| File | Description |
|---|---|
| `epcg23.csv` | 2023 NSCG data in CSV format (144 MB) — most convenient for Python/R analysis |
| `EPCG23.DAT` | ASCII fixed-width format (used with `LAYOUTPCG23.TXT` as layout spec) |
| `epcg23.sas7bdat` | Native SAS format |

**Codebooks and documentation:**
- `Ppcg23.html` / `Ppcg23.pdf` — variable codebook (consult this first when looking up variable meanings)
- `Dpcg23.xlsx` — crosswalk between source names and SAS variable names
- `LAYOUTPCG23.TXT` — column layout for the ASCII `.DAT` file
- `2023-NSCG-21_annotated_7Aug25.pdf` — original questionnaire with variable names annotated
- `2023NSCG_RecodeDocumentation_4Feb25.pdf` — recode documentation for derived variables
- `TOGA_crosswalk_NSCG23_20250116.xlsx` — geography code crosswalk (location variables use `_TOGA` suffix)

**SAS programs (reference only):**
- `Fpcg23.sas` — FORMAT assignment statements
- `Lpcg23.sas` — LABEL assignment statements
- `Ppcg23.sas` — PROC FORMAT statements

## Key Dataset Notes

- Geography variables changed in 2023 relative to past cycles — location fields now use the `_TOGA` suffix (e.g., `EMST_TOGA` for employer location, `RESPLO3_TOGA` for respondent location).
- Occupation code 611150 is new in 2023 for clinical/health-services psychologists; code 432360 now covers only research/applied psychologists.
- September 2025 errata corrected occupation and field-of-study labels in SAS formats and codebooks — use the September 2025 versions.

## Tech Stack
- Python & SQL (Pandas, Scikit-Learn, or DuckDB as needed for execution)





# Process & Methodology: Modeling Career Success (ACTUAL VALUE (Y))

## Definition of Actual Success
Actual Success = (1/3 * Salary_Percentile) + (1/3 * Job_Satisfaction_Score) + (1/3 * Upper_Management_Score)

### Component Definitions & Column Mapping

1. Salary (`SALARY` Column):
   - Filter for SALARY > 0.
   - Convert raw salary into a Percentile Rank from 0.00 to 1.00.
   - The median salary automatically sits at 0.50.

2. Job Satisfaction (`JOBSATIS` Column):
   - Drop rows with 'L' (Logical Skip / Unemployed).
   - Convert values to a 0.00 to 1.00 scale:
     - Code 4 (Very Dissatisfied) -> 0.00
     - Code 3 (Somewhat Dissatisfied) -> 0.33 (1/3)
     - Code 2 (Somewhat Satisfied) -> 0.67 (2/3)
     - Code 1 (Very Satisfied) -> 1.00 (3/3)

3. Upper Management Job (`SUPWK` Column):
   - Drop rows with 'L' (Logical Skip / Unemployed).
   - Binary indicator:
     - 'Y' or '1' -> 1.00
     - 'N' or '2' -> 0.00


## Process for Predicted Value (Y-hat):
