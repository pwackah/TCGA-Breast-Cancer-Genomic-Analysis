/* TCGA BRCA Survival Analysis Queries
Project: Genomic Stratification and Multi-Omic Prognostic Analysis
Database: Google BigQuery (Pan-Cancer Atlas 2018)
*/

-- Query 1: Overall Survival Analysis by Molecular Subtype Proxy
-- Purpose: Evaluate survival metrics across engineered biological clusters to identify high-risk groups.
SELECT 
    Molecular_Subtype_Proxy,
    COUNT(*) AS Patient_Count,
    ROUND(AVG(CAST(OS_MONTHS AS FLOAT64)), 2) AS Avg_Survival_Months,
    ROUND(MIN(CAST(OS_MONTHS AS FLOAT64)), 2) AS Min_Survival,
    ROUND(MAX(CAST(OS_MONTHS AS FLOAT64)), 2) AS Max_Survival
FROM 
    `pan-breast-cancer-atlas-2018.tcga_pan_breast_cancer_atlas_2018.BRCA_Final_Analysis_Data`
GROUP BY 
    Molecular_Subtype_Proxy
ORDER BY 
    Avg_Survival_Months DESC;

-- Query 2: TP53 Expression Tier Analysis (The Guardian Effect)
-- Purpose: Stratify cohort into quartiles to identify survival velocity in extreme phenotypes.
WITH TP53_Quartiles AS (
    SELECT 
        PATIENT_ID,
        OS_MONTHS,
        TP53,
        -- NTILE(4) breaks the cohort into 4 equal groups (1 = Lowest, 4 = Highest expression)
        NTILE(4) OVER(ORDER BY TP53 ASC) as Expression_Tier 
    FROM 
        `pan-breast-cancer-atlas-2018.tcga_pan_breast_cancer_atlas_2018.BRCA_Final_Analysis_Data`
    WHERE 
        TP53 IS NOT NULL 
        AND OS_MONTHS IS NOT NULL
)

SELECT 
    CASE 
        WHEN Expression_Tier = 1 THEN 'Low TP53 (Bottom 25%)'
        WHEN Expression_Tier IN (2, 3) THEN 'Normal (Middle 50%)'
        WHEN Expression_Tier = 4 THEN 'High TP53 (Top 25%)'
    END AS TP53_Status,
    ROUND(AVG(OS_MONTHS), 2) AS Mean_Survival_Months,
    COUNT(PATIENT_ID) AS Patient_Count
FROM 
    TP53_Quartiles
GROUP BY 
    TP53_Status
ORDER BY 
    Mean_Survival_Months DESC;
