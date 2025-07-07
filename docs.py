import streamlit as st


def show_documentation():
    """
    Shows comprehensive documentation page within the application.
    """
    # Main Title
    st.title("🧬 Genetic Variant Interpretation Application — Detailed User Guide")
    
    # Table of Contents
    with st.expander("📚 Table of Contents", expanded=True):
        st.markdown("""
        1. [Overview](#overview)
        2. [Getting Started](#getting-started)
        3. [Getting and Using API Key](#api-key)
        4. [File Preparation and Formats](#file-preparation)
        5. [Analysis Process](#analysis-process)
        6. [Data Sources](#data-sources)
        7. [Interpreting Results](#interpreting-results)
        8. [PDF Report Generation](#pdf-report)
        9. [Statistics and Charts](#statistics)
        10. [Troubleshooting](#troubleshooting)
        11. [Frequently Asked Questions](#faq)
        12. [Technical Details (For Developers)](#technical-details)
        """)

    # 1. Overview
    st.header("1. 🌟 Overview", anchor="overview")
    st.markdown("""
    This application analyzes your genetic variants (DNA changes) by collecting:
    
    - **Clinical significance information** from ClinVar database
    - **Gene-disease associations** from ClinGen database
    - **Population frequencies** from gnomAD database
    - **Related scientific articles** from PubMed database
    - **Comprehensive clinical interpretations** with Google Gemini AI
    
    and provides you with a detailed report.
    
    ### 🎯 Who Is This For?
    - Genetic specialists and doctors
    - Researchers
    - Bioinformatics specialists
    - Individuals wanting to understand genetic test results
    
    ### ⚡ Key Features
    - Upload variant files in VCF/CSV format
    - Automatic database matching
    - AI-powered clinical interpretation
    - Professional PDF report generation
    - Interactive result visualization
    """)

    # 2. Getting Started
    st.header("2. 🚀 Getting Started", anchor="getting-started")
    st.markdown("""
    ### Requirements
    - A modern web browser (Chrome, Firefox, Safari, Edge)
    - Internet connection
    - Google Gemini API key (can be obtained for free)
    
    ### Getting Started
    
    1. **Access the web application**
       - The application link will be provided to you
       - Simply open it in your browser
    
    2. **Prepare your API key**
       - You can get it for free from Google AI Studio
       - Details in the next section
    
    3. **Prepare your variant file**
       - In VCF, VCF.GZ, or CSV format
       - Details in the "File Preparation" section
    
    ### ⚡ Quick Start
    1. Open the application
    2. Enter your API key
    3. Upload your file
    4. Click "Interpret" button
    5. Review results and download PDF report
    
    💡 **Note:** No installation required, completely web-based!
    """)

    # 3. API Key
    st.header("3. 🔑 Getting and Using API Key", anchor="api-key")
    st.markdown("""
    ### Getting Google Gemini API Key
    
    1. **Go to Google AI Studio:** [https://aistudio.google.com/](https://aistudio.google.com/)
    
    2. **Sign in with your Google account**
    
    3. **Click "Get API Key" button**
    
    4. **Create a new project or select existing project**
    
    5. **Copy your API key**
    
    ### Using in the Application
    
    1. Make sure you're on the **"Application"** tab in the left menu
    
    2. Paste your key in the **"Your Gemini API Key"** field
    
    3. After key validation, file upload area will become active
    
    ⚠️ **Security Note:** Don't share your API key with anyone. Free plan provides 60 requests per day.
    """)

    # 4. File Preparation
    st.header("4. 📁 File Preparation and Formats", anchor="file-preparation")
    st.markdown("""
    ### Supported Formats
    
    #### 1. VCF Format (.vcf or .vcf.gz)
    ```
    ##fileformat=VCFv4.2
    #CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO
    1       14370   rs6054257 G      A       29      PASS    .
    1       17330   .         T      A       3       q10     .
    ```
    
    #### 2. CSV Format (.csv)
    Must have at least these 4 columns:
    ```csv
    CHROM,POS,REF,ALT
    1,14370,G,A
    1,17330,T,A
    2,234567,C,T
    ```
    
    ### Sample Data Preparation
    
    **Converting from Excel to CSV:**
    1. Prepare your variant data in Excel
    2. File → Save As → Select CSV UTF-8
    3. Ensure column headers are correct
    
    **Compressing VCF file:**
    ```bash
    gzip variants.vcf
    # This will create variants.vcf.gz
    ```
    
    ### ⚠️ Important Notes
    - Chromosome values: 1-22, X, Y or chr1-chr22, chrX, chrY
    - Position values must be numeric
    - REF and ALT values must consist of A, C, G, T letters
    - Maximum file size: 200MB
    """)

    # 5. Analysis Process
    st.header("5. 🔬 Analysis Process", anchor="analysis-process")
    st.markdown("""
    ### Step-by-Step Analysis
    
    #### 1️⃣ File Upload
    - Click "Upload file" button
    - Select your VCF, VCF.GZ, or CSV file
    - File will be automatically read and validated
    
    #### 2️⃣ Variant Matching
    The system performs these operations:
    - Compares uploaded variants with ClinVar database
    - Matches CHROM, POS, REF, ALT values
    - Retrieves clinical information for matching variants
    
    #### 3️⃣ Data Enrichment
    For each matching variant:
    - **From ClinVar:** Clinical significance, disease association, gene name
    - **From ClinGen:** Gene-disease validity classification
    - **From gnomAD:** Population frequencies, allele counts
    - **From PubMed:** Related scientific article links
    
    #### 4️⃣ AI Interpretation
    Google Gemini evaluates each variant for:
    1. Pathogenicity probability
    2. Known disease associations
    3. Clinical significance interpretation
    4. Understandable summary
    
    #### 5️⃣ Result Display
    - Interactive table
    - Sortable columns
    - Detailed information display
    - CSV/PDF export
    """)

    # 6. Data Sources
    st.header("6. 📊 Data Sources", anchor="data-sources")
    st.markdown("""
    ### ClinVar
    - **What:** NCBI's genetic variant database
    - **Content:** 1+ million variants, clinical significance information
    - **Updates:** Monthly
    
    #### Retrieved Information:
    - `CLNSIG`: Clinical significance (Pathogenic, Benign, etc.)
    - `GENE`: Associated gene name
    - `DISEASE`: Associated diseases
    - `CLNREVSTAT`: Review status
    
    ### ClinGen
    - **What:** Clinical genome resource
    - **Content:** Gene-disease relationship validities
    - **Classifications:** Definitive, Strong, Moderate, Limited, No Evidence
    
    ### gnomAD
    - **What:** Genome aggregation database
    - **Content:** Genomic data from 141,456 individuals
    - **Data:**
      - Allele frequencies
      - Population distributions
      - Filter status
    
    ### PubMed
    - **What:** Biomedical literature database
    - **Content:** 35+ million articles
    - **Usage:** Links to variant-related publications
    """)

    # 7. Interpreting Results
    st.header("7. 📈 Interpreting Results", anchor="interpreting-results")
    st.markdown("""
    ### Clinical Significance Categories
    
    #### 🔴 Pathogenic
    - Proven to cause disease
    - Requires clinical follow-up
    - Family screening recommended
    
    #### 🟠 Likely Pathogenic
    - 90%+ probability of causing disease
    - Treated like pathogenic
    
    #### 🟡 Uncertain Significance
    - Insufficient evidence
    - Requires follow-up and re-evaluation
    
    #### 🟢 Likely Benign
    - 90%+ probability of being harmless
    
    #### ⚪ Benign
    - No disease risk
    - Normal variation
    
    ### Population Frequency Assessment
    
    | Frequency | Interpretation |
    |-----------|----------------|
    | < 0.0001 | Very rare |
    | 0.0001-0.001 | Rare |
    | 0.001-0.01 | Uncommon |
    | 0.01-0.05 | Common |
    | > 0.05 | Very common |
    
    ### Understanding AI Interpretations
    
    Gemini interpretations are organized into 4 main sections:
    1. **Pathogenic probability:** Disease-causing potential
    2. **Disease association:** Connection to known diseases
    3. **Clinical significance:** Medical importance
    4. **Summary:** Plain language explanation
    """)

    # 8. PDF Report
    st.header("8. 📄 PDF Report Generation", anchor="pdf-report")
    st.markdown("""
    ### PDF Report Content
    
    1. **Cover Page**
       - Title and date
       - Patient information
       - Summary statistics
    
    2. **Analysis Summary**
       - Clinical significance distribution (pie chart)
       - Chromosome distribution (bar chart)
       - Allele frequency histogram
       - Most common genes
    
    3. **Clinical Significance Analysis**
       - High-risk variants
       - Low-risk variants
       - Uncertain variants
    
    4. **Detailed Variant List**
       - Table of first 15-20 variants
       - Chromosome, position, genes
       - Clinical significance information
    
    5. **AI Interpretations**
       - Detailed explanation for each variant
       - Clinical recommendations
                
    6. **Conclusions and Recommendations**
       - Overall assessment
       - Follow-up recommendations
    
    ### PDF Generation Steps
    
    1. After analysis is complete, go to **"PDF Report"** tab
    2. Fill in patient information:
       - Patient ID (auto-generated)
       - Patient Name
       - Age
       - Test Date
    3. Click **"Generate PDF Report"** button
    4. Download the generated report with **"Download PDF Report"**
    
    """)

    # 9. Statistics
    st.header("9. 📊 Statistics and Charts", anchor="statistics")
    st.markdown("""
    ### Displayed Statistics
    
    #### Summary Metrics
    - **Total Variants:** Number of analyzed variants
    - **Pathogenic:** Disease-causing variants
    - **Benign:** Harmless variants
    - **Uncertain:** Uncertain variants
    
    #### Charts
    
    1. **Clinical Significance Distribution**
       - Pie chart
       - Percentage distribution
       - Color-coded categories
    
    2. **Chromosome Distribution**
       - Bar chart
       - Chromosomes with most variants
       - Numerical distribution
    
    3. **Allele Frequency Histogram**
       - Rare vs common variants
       - Population distribution
       - Log-scale view
    
    4. **Gene-based Distribution**
       - Most frequently affected genes
       - Variant counts
       - Top 10 gene list
    """)

    # 10. Troubleshooting
    st.header("10. 🛠️ Troubleshooting", anchor="troubleshooting")
    st.markdown("""
    ### Common Errors
    
    #### 1. "Invalid API key"
    - **Cause:** Wrong or missing API key
    - **Solution:** Get a new key from Google AI Studio
    
    #### 2. "File format not supported"
    - **Cause:** Wrong file extension or format
    - **Solution:** Save in VCF, VCF.GZ, or CSV format
    
    #### 3. "Required columns missing"
    - **Cause:** Missing CHROM, POS, REF, ALT columns
    - **Solution:** Check your file and add missing columns
    
    #### 4. "No matching variants found"
    - **Cause:** Variants not in ClinVar
    - **Solution:** 
      - Check reference genome version (GRCh37/38)
      - Check chromosome format (1 vs chr1)
    
    #### 5. "Cannot retrieve gnomAD data"
    - **Cause:** API connection error or variant not found
    - **Solution:** Check your internet connection
    
    #### 6. "Cannot generate PDF"
    - **Cause:** Memory shortage or too many variants
    - **Solution:** Try with fewer variants or select summary report
    
    ### Performance Improvement
    
    - **Slow analysis:** Reduce number of variants (max 100-200)
    - **Memory error:** Split large files into chunks
    - **API limit:** Free plan has 60 requests per day limit
    """)

    # 10. Technical Details (For Developers)
    st.header("10. 🔧 Technical Details (For Developers)", anchor="technical-details")
    st.markdown("""
    ### System Architecture
    
    #### Main Components
    1. **app.py** - Main Streamlit application
    2. **clinvar_parser.py** - ClinVar data processing
    3. **gemini_handler.py** - Google Gemini AI integration
    4. **gnomad_handler.py** - gnomAD API connection (GraphQL)
    5. **pubmed_handler.py** - PubMed data fetching
    6. **clingen_handler.py** - ClinGen data processing
    7. **pdf_report_generator.py** - PDF report generation
    8. **docs.py** - This documentation page
    
    #### Data Flow
    ```
    User File → VCF/CSV Parser → ClinVar Matching
                                    ↓
    PDF Report ← AI Interpretation ← Data Enrichment
                                    ↓
                            gnomAD + PubMed + ClinGen
    ```
    
    #### Technologies Used
    - **Frontend:** Streamlit
    - **Data Processing:** Pandas, NumPy
    - **Visualization:** Matplotlib
    - **PDF:** ReportLab
    - **AI:** Google Generative AI (Gemini 1.5 Flash)
    - **APIs:** GraphQL (gnomAD), REST (NCBI E-utilities)
    
    #### Developer Setup
    If you want to run the code locally:
    ```bash
    # Requirements
    pip install streamlit pandas numpy matplotlib reportlab 
    pip install google-generativeai requests streamlit-option-menu
    
    # Running
    streamlit run app.py
    ```
    
    #### Data Files
    - `sampled_100.parquet` - ClinVar sample data
    - `Clingen-Gene-Disease-Summary-2025-07-01.csv` - ClinGen data
    
    #### Security Measures
    - API keys stored in session state
    - Files processed in temporary memory
    - SSL/TLS API communication
    - Patient names not sent to external APIs
    
    #### Cache Mechanism
    - gnomAD and PubMed queries cached for 24 hours
    - Performance boost for repeated queries
    """)

    # 11. Frequently Asked Questions
    st.header("11. ❓ Frequently Asked Questions", anchor="faq")
    st.markdown("""
    **Q: Is it free?**
    A: The application is free, but Google Gemini API has free plan limits (60 requests per day).
    
    **Q: Does it require installation?**
    A: No! It's completely web-based. You can access and use it just from your browser.
    
    **Q: Which browsers does it support?**
    A: All modern browsers like Chrome, Firefox, Safari, Edge are supported.
    
    **Q: Which reference genome version does it use?**
    A: GRCh38 (hg38) is used by default.
    
    **Q: How many variants can I analyze?**
    A: Technically no limit, but 100-200 variants are recommended for performance.
    
    **Q: How reliable are the results?**
    A: Results are based on current databases but are not for definitive diagnosis. Always consult with an expert.
    
    **Q: Are my data safe?**
    A: Data is kept in memory only during analysis. Patient names are not sent to external APIs.
    
    **Q: Which diseases can be detected?**
    A: All genetic diseases recorded in ClinVar. Especially single-gene diseases.
    
    **Q: Can I use WGS/WES data?**
    A: Yes, but you need to filter variants first and convert to VCF/CSV format.
    
    **Q: Can I use it on mobile devices?**
    A: Yes, but it offers better experience on larger screens (tablets, computers).
    
    **Q: Does it work offline?**
    A: No, internet is required for database queries and AI interpretations.
    """)

    # Contact
    st.header("📧 Contact and Support")
    st.markdown("""
    ### Developer Information
    - **Email:** enesozyaramiss@gmail.com
    - **Project Updates:** Can be followed on GitHub
    
    ### Contributing
    - Open issues for bug reports
    - Feature suggestions are welcome
    - Send PRs for documentation improvements
    
    ### Acknowledgments
    This application was made possible thanks to the open source community and scientific databases.
    
    ---
    *Last updated: July 2025*
    """)

    # End of page
    st.stop()