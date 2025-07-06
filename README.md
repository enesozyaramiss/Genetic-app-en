# 🧬 Genetic Variant Interpretation Application

Streamlit-based comprehensive genetic variant analysis and interpretation platform powered by Google Gemini AI.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Data Sources](#-data-sources)
- [API Integrations](#-api-integrations)
- [File Structure](#-file-structure)
- [Contributing](#-contributing)
- [License](#-license)

## 🌟 Overview

This application is a modern web platform developed for comprehensive analysis of genetic variants (DNA changes). It integrates multiple scientific databases and generates clinical-grade reports with AI-powered interpretations.

### 🎯 Target Audience

- **Genetic Specialists** - Clinical interpretation and patient assessment
- **Researchers** - Scientific studies and literature review
- **Bioinformatics Specialists** - Data analysis and pipeline integration
- **Medical Students** - Educational and learning purposes

## ✨ Features

### 🔬 Analysis Capabilities
- **Multi-format File Support**: Processing variant files in VCF, VCF.GZ, CSV formats
- **Automatic Data Matching**: CHROM:POS:REF:ALT based matching with ClinVar database
- **Comprehensive Annotation**: Information enrichment from 7 different data sources
- **AI Interpretation**: Professional clinical assessment with Google Gemini

### 📊 Data Enrichment
- **ClinVar**: Clinical significance, disease associations, gene information
- **ClinGen**: Gene-disease validity classifications
- **gnomAD**: Population frequencies, allele statistics
- **PubMed**: Related scientific article links

### 📄 Reporting System
- **Interactive Display**: Streamlit-based dynamic tables
- **Professional PDF Reports**: Patient information, charts, AI interpretations
- **CSV Export**: Raw data download options
- **Statistical Visualizations**: Pie and bar charts

### 🎨 User Experience
- **Responsive Design**: Desktop and tablet compatible interface
- **Real-time Progress**: Live progress tracking during analysis
- **Session Management**: Storing analysis results throughout the session
- **Error Management**: User-friendly error messages and solution suggestions

## 🚀 Installation

### Requirements

```bash
Python 3.8+
```

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/genetic-variant-interpreter.git
cd genetic-variant-interpreter
```

### 2. Install Required Packages

```bash
pip install -r requirements.txt
```

#### Requirements.txt Contents:
```txt
streamlit>=1.28.0
streamlit-option-menu>=0.3.6
pandas>=1.5.0
numpy>=1.21.0
matplotlib>=3.5.0
reportlab>=4.0.0
google-generativeai>=0.3.0
requests>=2.28.0
```

### 3. Prepare Data Files

Ensure the following files are in the project directory:
- `sampled_100.parquet` - ClinVar sample data
- `Clingen-Gene-Disease-Summary-2025-07-01.csv` - ClinGen validity data

### 4. Get Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click the "Get API Key" button
4. Copy your API key

### 5. Start the Application

```bash
streamlit run app.py
```

The application will run by default at `http://localhost:8501`.

## 📖 Usage

### Quick Start

1. **API Key Entry**
   ```
   After the application opens, enter your Google Gemini API key
   ```

2. **File Upload**
   ```
   Upload your variant file in VCF, VCF.GZ or CSV format
   ```

3. **Start Analysis**
   ```
   Click the "Interpret with Gemini" button
   ```

4. **Review Results**
   ```
   Use the Results, PDF Report and Statistics tabs
   ```

### Supported File Formats

#### VCF Format
```vcf
##fileformat=VCFv4.2
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO
1       14370   rs6054257 G      A       29      PASS    .
1       17330   .         T      A       3       q10     .
```

#### CSV Format
```csv
CHROM,POS,REF,ALT
1,14370,G,A
1,17330,T,A
2,234567,C,T
```

### Example Use Cases

#### 1. WGS/WES Variant Analysis
```bash
# Filter VCF file (coding region variants only)
bcftools view -R coding_regions.bed input.vcf > filtered.vcf

# Upload to application and analyze
```

#### 2. Targeted Panel Results
```bash
# Convert panel results to CSV format
# Ensure CHROM, POS, REF, ALT columns are present
```

#### 3. Research Variants
```bash
# Prepare variants from literature in CSV format
# Analyze individually or in batch
```

## 🗄️ Data Sources

### ClinVar
- **Source**: NCBI ClinVar Database
- **Content**: 1+ million genetic variants
- **Data**: Clinical significance (CLNSIG), Gene name (GENE), Disease (DISEASE)
- **Updates**: Monthly

### ClinGen
- **Source**: Clinical Genome Resource
- **Content**: Gene-disease relationship validities
- **Classifications**: Definitive, Strong, Moderate, Limited, No Evidence
- **Updates**: Quarterly

### gnomAD
- **Source**: Genome Aggregation Database
- **Content**: Genome data from 141,456 individuals
- **Data**: Allele frequencies, population distributions
- **Versions**: r2.1 (GRCh37), r4 (GRCh38)

### PubMed
- **Source**: NCBI PubMed Database
- **Content**: 35+ million biomedical articles
- **Access**: Via E-utilities API

## 🔌 API Integrations

### Google Gemini AI
```python
# Example usage
prompt = f"""
You are a clinical geneticist. Based on the following variant data:
- Variant: {chrom}:{pos} {ref}→{alt}
- ClinVar: {clnsig}, {gene}, {disease}
- gnomAD AF: {af}

Provide clinical interpretation...
"""
response = generate_with_gemini(prompt, api_key)
```

### gnomAD GraphQL
```python
# Example query
query = """
query ($variantId: String!) {
  variant(variantId: $variantId, dataset: gnomad_r4) {
    exome { ac an }
    genome { ac an }
  }
}
"""
```

### NCBI E-utilities
```python
# PubMed links
pmids = get_pubmed_ids_from_clinvar(variation_id)
links = build_pubmed_links(pmids)
```

## 📁 File Structure

```
genetic-variant-interpreter/
├── app.py                     # Main Streamlit application
├── clinvar_parser.py          # ClinVar data processing module
├── gemini_handler.py          # Google Gemini AI integration
├── gnomad_handler.py          # gnomAD API connection (optional)
├── pubmed_handler.py          # PubMed data fetching module
├── clingen_handler.py         # ClinGen data processing module
├── pdf_report_generator.py    # PDF report generation module
├── docs.py                    # Documentation page
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── LICENSE                    # License file
├── sampled_100.parquet       # ClinVar sample data
├── Clingen-Gene-Disease-Summary-2025-07-01.csv  # ClinGen data
└── assets/                    # Visual and documentation files
    ├── screenshots/
    └── examples/
```

### Main Modules

#### `app.py`
- Streamlit interface
- Session state management
- Main analysis loop
- Tab-based display

#### `clinvar_parser.py`
- INFO string parsing
- Variant matching
- gnomAD link generation
- GraphQL queries

#### `gemini_handler.py`
- Google Generative AI integration
- Prompt engineering
- Rate limiting
- Error handling

#### `pdf_report_generator.py`
- ReportLab-based PDF generation
- Chart integration
- Patient information management
- Template system

## 🛠️ Developer Guide

### Adding New Data Source

```python
# Create new handler file
# example: mydb_handler.py

def fetch_mydb_data(chrom, pos, ref, alt):
    """Fetch data from new database"""
    # API call
    # Data processing
    return result

# Integrate into app.py
from mydb_handler import fetch_mydb_data

# Use in main loop
mydb_data = fetch_mydb_data(row['CHROM'], row['POS'], 
                           row['REF'], row['ALT'])
```

### Custom Prompt Template

```python
# Inside gemini_handler.py
def create_custom_prompt(variant_data, clinical_context="general"):
    """Create prompt for custom clinical context"""
    
    if clinical_context == "oncology":
        prompt = f"""
        Oncology-focused interpretation for:
        {variant_data}
        
        Focus on:
        1. Cancer predisposition
        2. Therapeutic implications
        3. Prognostic value
        """
    
    return prompt
```

### Cache Optimization

```python
# Cache settings for large datasets
@st.cache_data(
    ttl=24*3600,  # 24 hour cache
    max_entries=1000,  # Maximum entry count
    show_spinner=False
)
def expensive_api_call(params):
    return api_response
```

## 🧪 Test Data

### Sample VCF File
```bash
# Sample variants you can use for testing
wget https://github.com/yourusername/genetic-variant-interpreter/raw/main/examples/test_variants.vcf
```

### Known Pathogenic Variants
```csv
CHROM,POS,REF,ALT,EXPECTED_RESULT
17,43094077,G,A,Pathogenic
13,32315474,G,T,Pathogenic
7,117199644,G,A,Likely_Pathogenic
```

## 🔒 Security and Privacy

- **API Keys**: Stored in session state, no persistent storage
- **Patient Data**: Kept in memory only during analysis
- **External APIs**: Patient names not sent to external services
- **GDPR Compliant**: Personal data processing policies

## 📊 Performance Metrics

- **File Size**: Maximum 200MB VCF file
- **Variant Count**: Optimal 100-200 variants/analysis
- **API Limits**: Gemini free plan - 60 requests/day
- **Memory Usage**: ~500MB typical, 2GB maximum

## 🐛 Known Issues and Solutions

### 1. API Rate Limiting
```python
# Solution: Exponential backoff
import time
import random

def api_call_with_retry(func, max_retries=3):
    for i in range(max_retries):
        try:
            return func()
        except RateLimitError:
            wait_time = (2 ** i) + random.uniform(0, 1)
            time.sleep(wait_time)
    raise Exception("Max retries exceeded")
```

### 2. Large File Processing
```python
# Solution: Chunk-based processing
def process_large_vcf(df, chunk_size=50):
    results = []
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        chunk_results = process_chunk(chunk)
        results.extend(chunk_results)
    return results
```

### 3. Memory Optimization
```python
# Solution: Lazy loading and cleanup
import gc

def cleanup_memory():
    gc.collect()
    
# Clean large DataFrames with del
del large_dataframe
cleanup_memory()
```

## 🔄 Updates and Roadmap

### v2.0.0 (Planned)
- [ ] Multi-threading support
- [ ] Database backend integration
- [ ] REST API endpoints
- [ ] User authentication system
- [ ] Batch processing capabilities

### v1.5.0 (Upcoming)
- [ ] HGVS notation support
- [ ] PolyPhen/SIFT score integration
- [ ] Custom annotation pipeline
- [ ] Excel export options

### v1.1.0 (Current)
- [x] PDF report system
- [x] Multiple data source integration
- [x] AI-powered interpretation
- [x] Interactive visualization

## 🤝 Contributing

### Code Contribution
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Bug Report
- Use template when opening issue
- Detail reproduction steps
- Include environment information
- Add screenshots

### Feature Request
- Explain use case
- Mention existing alternatives if any
- List technical requirements

## 📞 Support and Contact

- **Email**: enesozyaramiss@gmail.com
- **GitHub Issues**: [Issues page](https://github.com/enesozyaramiss/genetik-app/issues)
- **Documentation**: In-app "Documentation" tab

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

This project was made possible thanks to the following open source projects and databases:

- **Streamlit** - Web framework
- **Google Generative AI** - AI interpretation
- **ClinVar** - Genetic variant database
- **ClinGen** - Clinical genome resource
- **gnomAD** - Population genomic data
- **NCBI** - Bioinformatics tools
- **ReportLab** - PDF generation

---

**⚠️ Important Warning**: This application is for informational purposes and does not make definitive medical diagnoses. For clinical decisions, specialist physician consultation is essential.

*Last updated: July 2025*