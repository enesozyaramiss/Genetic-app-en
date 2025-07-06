import os
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import gzip, io, time

from pdf_report_generator import create_pdf_report_for_streamlit
from clinvar_parser import enrich_clinvar_df, add_gnomad_links, fetch_gnomad_simple
from gemini_handler import generate_with_gemini
from clingen_handler import load_clingen_validity, get_clingen_classification
from pubmed_handler import get_pubmed_ids_from_clinvar, build_pubmed_links

# Page configuration
st.set_page_config(page_title="Genetic App", layout="wide")

# Define keys for session state
if 'analysis_completed' not in st.session_state:
    st.session_state.analysis_completed = False
if 'results_data' not in st.session_state:
    st.session_state.results_data = None
if 'pdf_created' not in st.session_state:
    st.session_state.pdf_created = False

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="📑 Menu",
        options=["Application", "Documentation"],
        icons=["house", "file-earmark-text"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0px 0px 20px 0px"},
            "icon": {"font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "--hover-color": "#f0f0f0"
            },
            "nav-link-selected": {
                "background-color": "#d9534f",
                "color": "white",
            },
        }
    )

if selected == "Documentation":
    from docs import show_documentation
    show_documentation()
else:
    # Cached functions
    @st.cache_data(ttl=24 * 3600, show_spinner=False)
    def get_pubmed_ids_cached(variation_id: str):
        return get_pubmed_ids_from_clinvar(variation_id)

    @st.cache_data(ttl=24 * 3600, show_spinner=False)
    def fetch_gnomad_cached(chrom: str, pos: str, ref: str, alt: str):
        return fetch_gnomad_simple(chrom, pos, ref, alt)

    # Data loading and preparation
    clinvar_df = enrich_clinvar_df(pd.read_parquet("sampled_100.parquet"))
    clinvar_df = add_gnomad_links(clinvar_df, genome_build="GRCh38")
    clingen_df = load_clingen_validity("Clingen-Gene-Disease-Summary-2025-07-01.csv")

    def parse_vcf_gz(uploaded_file):
        rows = []
        with gzip.open(io.BytesIO(uploaded_file.read()), 'rt') as f:
            for line in f:
                if line.startswith("#"): continue
                p = line.strip().split("\t")
                rows.append({"CHROM": p[0], "POS": int(p[1]), "REF": p[3], "ALT": p[4]})
        return pd.DataFrame(rows)

    def parse_vcf(uploaded_file):
        content = uploaded_file.getvalue().decode().splitlines()
        rows = []
        for line in content:
            if line.startswith("#"): continue
            p = line.strip().split("\t")
            rows.append({"CHROM": p[0], "POS": int(p[1]), "REF": p[3], "ALT": p[4]})
        return pd.DataFrame(rows)

    # Main Application
    st.title("🧬 Gemini-Powered Genetic Variant Interpretation")

    if st.session_state.analysis_completed and st.session_state.results_data is not None:
        results_df = pd.DataFrame(st.session_state.results_data)
        st.success("✅ Analysis completed!")

        if st.button("🔄 Start New Analysis", type="secondary"):
            st.session_state.analysis_completed = False
            st.session_state.results_data = None
            st.session_state.pdf_created = False
            st.rerun()

        tab1, tab2, tab3 = st.tabs(["📊 Results", "📄 PDF Report", "📈 Statistics"])

        # Results Tab
        with tab1:
            st.subheader("📊 Analysis Results")
            st.dataframe(results_df)
            csv_data = results_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv_data,
                file_name=f"genetic_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

        # PDF Report Tab
        with tab2:
            st.subheader("📄 Professional PDF Report")

            if st.session_state.pdf_created:
                st.success("✅ PDF report is ready!")
                st.download_button(
                    label="📥 Download PDF Report",
                    data=st.session_state['pdf_bytes'],
                    file_name=st.session_state['pdf_filename'],
                    mime="application/pdf"
                )

                with st.expander("📋 Report Details", expanded=True):
                    patient_info = st.session_state.get('pdf_patient_info', {})
                    report_options = st.session_state.get('pdf_report_options', {})
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Patient Information:**")
                        st.write(f"- ID: {patient_info.get('id', 'N/A')}")
                        st.write(f"- Name: {patient_info.get('name', 'N/A')}")
                        st.write(f"- Age: {patient_info.get('age', 'N/A')}")
                        st.write(f"- Test Date: {patient_info.get('test_date', 'N/A')}")
                    with col2:
                        st.write("**Report Settings:**")
                        st.write(f"- Type: {report_options.get('template', 'N/A')}")
                        st.write(f"- Language: {report_options.get('language', 'N/A')}")
                        st.write(f"- Charts: ✓")
                        st.write(f"- Detailed Analysis: ✓")
            else:
                with st.container():
                    st.info("📝 Fill out the form to create a PDF report.")
                with st.form("pdf_generation_form"):
                    st.markdown("#### 👤 Patient Information")
                    col1, col2 = st.columns(2)
                    with col1:
                        patient_id = st.text_input("Patient ID")
                        patient_name = st.text_input("Patient Name")
                    with col2:
                        patient_age = st.number_input("Age", min_value=0, max_value=150)
                        test_date = st.date_input("Test Date", value=pd.Timestamp.now().date())
                    submitted = st.form_submit_button("🎯 Generate PDF Report")
                    if submitted:
                        with st.spinner("🔄 Preparing PDF..."):
                            patient_info = {
                                'id': patient_id or f"RPT_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}" ,
                                'name': patient_name or "Not specified",
                                'age': str(patient_age) if patient_age > 0 else "Not specified",
                                'test_date': test_date.strftime('%d.%m.%Y')
                            }
                            report_options = {
                                'template': "Summary Report",
                                'language': "English",
                                'include_charts': True,
                                'include_detailed_analysis': True
                            }
                            pdf_bytes = create_pdf_report_for_streamlit(results_df, patient_info, report_options)
                            st.session_state['pdf_bytes'] = pdf_bytes
                            st.session_state['pdf_filename'] = f"genetic_report_{patient_info['id']}.pdf"
                            st.session_state.pdf_created = True
                            st.session_state['pdf_patient_info'] = patient_info
                            st.session_state['pdf_report_options'] = report_options
                        st.rerun()

        # Statistics Tab
        with tab3:
            st.subheader("📈 Analysis Statistics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Variants", len(results_df))
            with col2:
                pathogenic_count = len(results_df[results_df['CLNSIG'].str.contains('Pathogenic', na=False)])
                st.metric("Pathogenic", pathogenic_count)
            with col3:
                benign_count = len(results_df[results_df['CLNSIG'].str.contains('Benign', na=False)])
                st.metric("Benign", benign_count)
            with col4:
                uncertain_count = len(results_df[results_df['CLNSIG'].str.contains('Uncertain', na=False)])
                st.metric("Uncertain", uncertain_count)
            if 'CLNSIG' in results_df.columns:
                st.subheader("🔍 Clinical Significance Distribution")
                st.bar_chart(results_df['CLNSIG'].value_counts())
            if 'GENE' in results_df.columns:
                st.subheader("🧬 Most Frequently Observed Genes")
                st.bar_chart(results_df['GENE'].value_counts().head(10))

    else:
        # Initial analysis screen
        st.markdown("### ⚙️ Settings")
        api_key = st.text_input("Your Gemini API Key", type="password")
        if not api_key:
            st.warning("⚠️ API key not entered")
            st.info("💡 You can get a free key from Google AI Studio.")
            st.stop()
        uploaded = st.file_uploader("📁 Upload file (.vcf/.vcf.gz/.csv)", type=["vcf","vcf.gz","csv"])
        if uploaded:
            if uploaded.name.endswith(".vcf.gz"):
                df = parse_vcf_gz(uploaded)
            elif uploaded.name.endswith(".vcf"):
                df = parse_vcf(uploaded)
            else:
                df = pd.read_csv(uploaded)
            required_cols = {"CHROM","POS","REF","ALT"}
            if not required_cols.issubset(df.columns):
                st.error("❌ Upload error: required columns missing.")
                st.stop()
            st.success(f"✅ File uploaded: {len(df)} variants.")
            with st.expander("📋 Show Variants", expanded=False):
                st.dataframe(df.head(20))
            if st.button("🔎 Interpret with Gemini", type="primary"):
                with st.spinner("🧠 Generating interpretations..."):
                    for c in ["CHROM","POS","REF","ALT"]:
                        df[c] = df[c].astype(str)
                        clinvar_df[c] = clinvar_df[c].astype(str)
                    merged = pd.merge(df, clinvar_df, on=["CHROM","POS","REF","ALT"], how="left")
                    merged["ClinGen_Validity"] = merged["GENE"].apply(lambda g: get_clingen_classification(g, clingen_df))
                    matched = merged[~merged["ID"].isna()].copy()
                    if matched.empty:
                        st.warning("⚠️ No matching variants found.")
                        st.stop()
                    st.write(f"✅ {len(matched)} matches found.")
                    with st.expander("🔍 Show Matches", expanded=True):
                        st.dataframe(matched.head(30))
                    status = st.empty()
                    overall_pb = st.progress(0)
                    total = len(matched)
                    results = []
                    for idx, (i,row) in enumerate(matched.iterrows(),1):
                        status.markdown(f"### 🔍 Processing {idx}/{total}: {row['CHROM']}:{row['POS']} {row['REF']}>{row['ALT']}")
                        pm_response = get_pubmed_ids_cached(str(int(row["ID"])))
                        pmids = pm_response if not(isinstance(pm_response,dict) and "error" in pm_response) else []
                        gnomad_response = fetch_gnomad_cached(row["CHROM"],row["POS"],row["REF"],row["ALT"])
                        stats = gnomad_response if not(isinstance(gnomad_response,dict) and "error" in gnomad_response) else {}
                        prompt = f"""
You are a clinical geneticist. Based on the following variant and annotation data, provide a professional clinical interpretation.

🧬 Variant:
- Chr: {row['CHROM']}, Pos: {row['POS']}, {row['REF']}→{row['ALT']}

📑 ClinVar:
- Gene: {row.get('GENE','N/A')}, Sig: {row.get('CLNSIG','N/A')}, Dis: {row.get('DISEASE','N/A')}

🧪 ClinGen Validity: {row.get('ClinGen_Validity','N/A')}

📚 PubMed: {', '.join(pmids) if pmids else 'None'}

📊 gnomAD:
- Exome AC/AN: {stats.get('Exome_AC','N/A')}/{stats.get('Exome_AN','N/A')}
- PopMax AF: {stats.get('PopMax_AF','N/A')} (Pop: {stats.get('PopMax_Pop','N/A')})

🩺 Answer:
1. Likely pathogenicity?
2. Known disease?
3. Clinical relevance?
4. Plain-language summary (≤5 sents).
"""
                        try:
                            interpretation = generate_with_gemini(prompt, api_key=api_key)
                        except Exception as e:
                            interpretation = f"❌ Error: {e}"
                        pubmed_links = build_pubmed_links(pmids)
                        results.append({**row.to_dict(),"PubMed_Links":", ".join(pubmed_links),**stats,"Gemini_Interpretation":interpretation})
                        time.sleep(0.3)
                        overall_pb.progress(idx/total)
                    st.session_state.results_data = results
                    st.session_state.analysis_completed = True
                    st.rerun()