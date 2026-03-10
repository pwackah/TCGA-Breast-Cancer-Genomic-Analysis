# scripts/data_processing.py
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def run_tcga_etl(clinical_path, genomic_path):
    """
    ETL Pipeline for TCGA Breast Cancer Analysis.
    Performs data ingestion, biomarker extraction, normalization, and feature engineering.
    """
    
    # 1. Load Clinical Data (Skip metadata headers)
    df_clinical = pd.read_csv(clinical_path, sep='\t', header=4).drop(0)

    # 2. Extract Targeted Biomarkers (Memory-efficient chunking)
    target_genes = ['ESR1', 'ERBB2', 'TP53']
    genomic_chunks = pd.read_csv(genomic_path, sep='\t', chunksize=5000)
    df_genomic = pd.concat([chunk[chunk['Hugo_Symbol'].isin(target_genes)] for chunk in genomic_chunks])

    # 3. Pivot & Align Sample IDs (Standardize to TCGA-XX-XXXX)
    df_pivot = df_genomic.set_index('Hugo_Symbol').drop(columns=['Entrez_Gene_Id']).T
    df_pivot.index.name = 'SAMPLE_ID'
    df_pivot = df_pivot.reset_index()
    df_pivot['PATIENT_ID'] = df_pivot['SAMPLE_ID'].str[:12]

    # 4. Merge Datasets (Inner join for clinical-genomic alignment)
    master_df = pd.merge(df_clinical, df_pivot, on='PATIENT_ID', how='inner')

    # 5. Log2 Normalization (Stabilize variance for RSEM counts)
    for gene in target_genes:
        master_df[gene] = pd.to_numeric(master_df[gene], errors='coerce').fillna(0)
        master_df[f'Log2_{gene}'] = np.log2(master_df[gene] + 1)

    # 6. Feature Engineering: Molecular Subtype Proxy
    master_df['Molecular_Subtype_Proxy'] = np.where(
        (master_df['Log2_ESR1'] > 12) & (master_df['Log2_ERBB2'] > 12), 'Double Positive',
        np.where(master_df['Log2_ERBB2'] > 12, 'HER2+',
        np.where(master_df['Log2_ESR1'] > 12, 'ER+', 'Double Negative'))
    )

    return master_df

if __name__ == "__main__":
    # Note: Filenames should match your local TCGA data source
    processed_data = run_tcga_etl('data_clinical_patient.txt', 'data_mrna_seq_v2_rsem.txt')
    processed_data.to_csv('BRCA_Final_Analysis_Data.csv', index=False)
    print(f"Success: Processed {len(processed_data)} patient records.")
    
