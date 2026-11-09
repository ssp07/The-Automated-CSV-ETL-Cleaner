import os
import sqlite3
import streamlit as st
import pandas as pd
import numpy as np

# ==========================================
# AUTOMATED ETL PIPELINE LOGIC MATRIX
# ==========================================
DB_FILE = "universal_clean_warehouse.db"

st.set_page_config(page_title="Autonomous ETL Engine", layout="wide")
st.title("⚙️ Autonomous Universal ETL Ingestion Engine")
st.markdown("### Project #3: Automated Schema Cleaning & Relational Target Loader")
st.markdown("---")

if not os.path.exists("dataset.csv"):
    st.error("⚠️ System Ingestion Error: Please place a target 'dataset.csv' file in the directory root.")
else:
    st.subheader("📥 Phase 1: Extract (Raw Messy Source Data)")
    df_raw = pd.read_csv("dataset.csv")
    st.dataframe(df_raw, use_container_width=True, hide_index=True)
    
    # Run Automated Transformations
    with st.spinner("🧠 Running auto-cleansing rules..."):
        # 1. Deduplication
        initial_rows = len(df_raw)
        df_clean = df_raw.drop_duplicates().copy()
        dupes_removed = initial_rows - len(df_clean)
        
        # 2. String Normalization (Lowercase, remove erratic padding whitespace)
        df_clean.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in df_clean.columns]
        
        # 3. Intelligent Null Imputation Strategy Mapping
        logs = []
        for col in df_clean.columns:
            if df_clean[col].dtype in [np.int64, np.float64]:
                null_count = df_clean[col].isnull().sum()
                if null_count > 0:
                    median_val = df_clean[col].median()
                    df_clean[col] = df_clean[col].fillna(median_val)
                    logs.append(f"Filled {null_count} empty cells in numeric column `{col}` with median value ({median_val})")
            else:
                df_clean[col] = df_clean[col].astype(str).str.strip()
                null_count = (df_clean[col].str.lower() == 'nan').sum() + df_clean[col].isnull().sum()
                df_clean[col] = df_clean[col].replace(['nan', 'NaN', ''], 'Unknown')
                if null_count > 0:
                    logs.append(f"Sanitized {null_count} empty/corrupted strings in column `{col}` with 'Unknown' tag baseline")

        # 4. Load Phase into target Relational Warehouse tables
        conn = sqlite3.connect(DB_FILE)
        df_clean.to_sql("cleaned_analytics_records", conn, if_exists="replace", index=False)
        conn.close()

    st.subheader("🛠️ Phase 2: Transform (Autonomous Cleansing Operational Logs)")
    st.info(f"**Deduplication Engine:** Scanned dataset rows and automatically purged **{dupes_removed} duplicated row anomalies**.")
    for log_item in logs:
        st.write(f"✔️ {log_item}")
        
    st.subheader("🚀 Phase 3: Load (Pristine Normalized Lakehouse Output Database)")
    st.success("Target loaded successfully into local SQLite table: `cleaned_analytics_records`")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Clean Structured Data Grid Layout**")
        st.dataframe(df_clean, use_container_width=True, hide_index=True)
    with col2:
        st.markdown("**System Numeric Data Distribution Metrics**")
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            # FIXED: Removed the .set_index column mismatch to prevent array length errors completely
            st.bar_chart(df_clean[numeric_cols[-1]], use_container_width=True)
        else:
            st.info("💡 Tabular string profiles optimized for system grid views.")

