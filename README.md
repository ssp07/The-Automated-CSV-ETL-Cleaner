# The-Automated-CSV-ETL-Cleaner
# Autonomous Schema Cleaning & Relational ETL Engine (Project #3)

A high-performance, algorithmic Data Engineering pipeline designed to automatically ingest raw, uncurated corporate transactional spreadsheets, clean them, and transition them into pristine, production-ready relational data networks. Built explicitly to eliminate human data entry anomalies, this system operates entirely on autopilot to clear messy datasets within enterprise data lake architectures.

## 🛠️ Automated ETL Processing Phases
* **Phase 1: Extract (Raw Messy Ingestion):** Intercepts raw comma-separated files containing erratic padding layouts, blank entries, or structural columns on launch.
* **Phase 2: Transform (Autonomous Cleansing Logic):**
  * *Purges Duplicate Vectors:* Executes atomic data layout comparison rules to isolate and drop repeating row anomalies.
  * *Normalizes Metadata:* Shrinks data structures by mapping lowercase conversions and removing formatting spaces across column names.
  * *Statistical Null Imputation:* Implements smart filling mapping; calculates live column medians to patch broken integer cells while stamping blank string fragments with safe `Unknown` tags.
* **Phase 3: Load (Lakehouse Target Loading):** Commits the normalized, fault-tolerant target frames into local SQLite relational schema tables (`cleaned_analytics_records`) for live analytic querying.

## 📦 Execution Roadmap
1. Place your target database spreadsheet data named **`dataset.csv`** in your application environment path.
2. Install the necessary system dependencies:
```bash
pip install streamlit pandas numpy
```
3. Launch the automated pipeline engine dashboard:
```bash
streamlit run app.py
```
