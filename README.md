# TCGA Breast Cancer Cohort: Genomic Stratification and Multi-Omic Prognostic Analysis

**Author:** Prosper Wiredu Ackah

## Project Overview
This project integrates clinical oncology data with mRNA sequencing results from The Cancer Genome Atlas (TCGA) to identify genomic signatures that serve as reliable proxies for patient risk. Focusing on a cohort of 1,084 unique Breast Invasive Carcinoma (BRCA) patients, this study utilizes statistical tiering to predict survival velocity and mortality probability.

## Tech Stack
* **Data Engineering:** Python (Pandas, NumPy)
* **Exploratory Analysis:** SQL (BigQuery)
* **Data Visualization:** Tableau
* **Domain Knowledge:** Bioinformatics, Oncology, Genomics

---

## 1. The Clinical Challenge (Ask)
The primary objective is to analyze the relationship between biomarker expression and long-term survival to inform personalized treatment strategies. The study addresses four core questions:
1. How can patients be accurately stratified using biomarkers like **ESR1** and **ERBB2**?
2. Do distinct molecular subtypes exhibit statistically different overall survival (OS) or mortality rates?
3. Can SQL-based quartile tiering of tumor suppressor genes (e.g., **TP53**) reveal prognostic trends?
4. How can clinical stakeholders visualize this variance to better assess patient risk?

## 2. Data Preparation (Prepare)
The data for this project was sourced from the **TCGA Pan-Cancer Atlas 2018** via cBioPortal, representing a high-authority open-access repository for genomic research.

* **Data Sources:** Two primary datasets were utilized—`data_clinical_patient.txt` (structured metadata) and `data_mrna_seq_v2_rsem.txt` (continuous genomic expression values).
* **Data Privacy:** The dataset consists of de-identified, open-access patient records, ensuring compliance with data privacy standards while maintaining clinical utility.
* **Integrity & Verification:** Preliminary data inspection confirmed a cohort of 1,084 patients and 20,531 raw transcripts. Initial verification involved checking for data types (Strings vs. Floats) and ensuring the uniqueness of patient identifiers.

## 3. Data Pipeline & ETL (Process)
A programmatic ETL pipeline was built in Python to resolve dimensionality and variance issues within the 16,564 high-quality unique genes identified:



* **Targeted Extraction:** The pipeline utilized data chunking to filter strictly for high-impact biomarkers (ESR1, ERBB2, and TP53) from massive mRNA sequencing files.
* **Integrity Check:** Standardized `PATIENT_ID` keys (e.g., TCGA-3C-AAAU) with genomic sample IDs, performing an Inner Join to ensure 100% data alignment for the cohort.
* **Normalization:** Applied a `Log2(x + 1)` transformation via NumPy to normalize high-variance RSEM counts (ranging from zero to thousands) for accurate visual clustering.
* **Feature Engineering:** Developed custom Python logic and SQL `CASE` expressions to create "Molecular Subtype Proxies" (e.g., ER+/HER2-), reflecting standard clinical classifications.

## 4. Exploratory Analysis (Analyze)
Before visual rendering, SQL Window Functions (`NTILE`) were utilized in BigQuery to isolate extreme quartiles (Top 25% vs. Bottom 25%) and identify hidden prognostic trends:



* **The TP53 "Guardian" Effect:** High TP53 expression demonstrated a protective prognostic trend, with a mean survival of 43.67 months compared to 39.79 months in the low expression quartile (a ~10% extension).
* **The ERBB2 (HER2) Survival Impact:** High ERBB2 expression (Top 25%) correlated with a ~4-month decrease in mean survival (37.96 months) compared to the low expression group (42.05 months).
* **Univariate Sensitivity:** Initial SQL analysis of ESR1 alone suggested a survival deficit for high-expression patients; however, multivariate stratification revealed that the deficit was specifically driven by the aggressive HER2+ (ERBB2) subset.

## 5. Visual Insights & Clinical Findings (Share)
The interactive Tableau dashboard utilizes Level of Detail (LOD) concepts to establish mean survival benchmarks while maintaining data transparency:



* **Genomic Stratification:** A scatter plot of Log2_ESR1 vs. Log2_ERBB2 identifies distinct clusters, proving that mRNA sequencing can effectively categorize biological subtypes.
* **The "Average" Illusion:** Box plots were utilized to reveal survival distribution within the "Double Negative" cohort, which is often masked by simple mean calculations. These revealed extreme outliers and highly unpredictable patient outcomes.
* **Mortality Rate Discrepancies:** Stacked bar charts highlight that survival *length* (months) does not always correlate with survival *probability* (Living vs. Deceased).

## 6. Strategic Recommendations (Act)
* **Prioritize Multi-Gene Screening:** Dashboards should prioritize combined ERBB2/ESR1 status over single-gene metrics, as "Double Positive" status significantly altered survival benchmarks.
* **Deploy Variance-Based Risk Assessment:** Clinical systems must include distribution metrics (Box Plots) rather than relying solely on average survival times to better assess risk volatility.
* **Focus on High-Risk Tiers for Monitoring:** Patients identified in the Low TP53 / High ERBB2 risk tier should be prioritized for more aggressive follow-up cadences.
* **Standardize Log2 Normalization:** Future pipelines should automatically apply the `Log2(x + 1)` transformation to ensure new patient genomic data maps correctly onto existing visual clusters.

## 7. Limitations & Caveats
* **Biomarker Scope:** This analysis relies on a "proxy" subtype based on only two genes; true clinical classification often includes Progesterone Receptor (PR) status and Ki-67 indexes.
* **mRNA vs. Protein Expression:** Data measures mRNA transcription (RSEM), which is not identical to physical protein expression measured via Immunohistochemistry (IHC) staining.
* **Retrospective Bias:** The dataset represents a historical cohort where survival may be influenced by unrecorded, non-standardized treatment regimens (e.g., chemotherapy or targeted therapies like Herceptin).

---
### Interactive Dashboard: 
https://public.tableau.com/app/profile/prosper.ackah/viz/TCGABreastCancerCohortGenomicStratificationandSurvivalAnalysis/Dashboard1
