import pandas as pd
import re
import requests
import logging
import urllib.parse

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# --- ClinVar INFO Parsers ---
def extract_gene(info_str):
    if pd.isna(info_str): return None
    match = re.search(r'GENEINFO=([A-Z0-9\-]+)', info_str)
    return match.group(1).split(":")[0] if match else None

def extract_clnsig(info_str):
    if pd.isna(info_str): return None
    match = re.search(r'CLNSIG=([^;]+)', info_str)
    return match.group(1) if match else None

def extract_disease(info_str):
    if pd.isna(info_str): return None
    match = re.search(r'CLNDN=([^;]+)', info_str)
    return match.group(1).replace("_", " ") if match else None

def extract_rs(info_str):
    if pd.isna(info_str): return None
    match = re.search(r'RS=([0-9]+)', info_str)
    return match.group(1) if match else None

def extract_clnvc(info_str):
    if pd.isna(info_str): return None
    match = re.search(r'CLNVC=([^;]+)', info_str)
    return match.group(1) if match else None

def extract_clnhgvs(info_str):
    if pd.isna(info_str): return None
    match = re.search(r'CLNHGVS=([^;]+)', info_str)
    return match.group(1) if match else None

def extract_clnrevstat(info_str):
    if pd.isna(info_str): return None
    match = re.search(r'CLNREVSTAT=([^;]+)', info_str)
    return match.group(1).replace("_", " ") if match else None


# --- ClinVar Data Enrichment ---
def enrich_clinvar_df(df):
    df["GENE"] = df["INFO"].apply(extract_gene)
    df["CLNSIG"] = df["INFO"].apply(extract_clnsig)
    df["DISEASE"] = df["INFO"].apply(extract_disease)
    df["RS"] = df["INFO"].apply(extract_rs)
    df["CLNVC"] = df["INFO"].apply(extract_clnvc)
    df["CLNHGVS"] = df["INFO"].apply(extract_clnhgvs)
    df["CLNREVSTAT"] = df["INFO"].apply(extract_clnrevstat)
    return df


# --- gnomAD Link Generator ---
def add_gnomad_links(df, genome_build="GRCh37"):
    def build_url(row):
        chrom = str(row['CHROM']).replace("chr", "").strip()
        pos = int(row['POS'])
        ref = row['REF'].strip()
        alt = row['ALT'].strip()
        if not chrom or not ref or not alt:
            return None
        ds = "gnomad_r2_1" if genome_build == "GRCh37" else "gnomad_r4"
        return f"https://gnomad.broadinstitute.org/variant/{chrom}-{pos}-{urllib.parse.quote(ref)}-{urllib.parse.quote(alt)}?dataset={ds}"

    df["gnomAD_Link"] = df.apply(build_url, axis=1)
    return df


# --- gnomAD GraphQL API Handler ---
def fetch_gnomad_simple(chrom, pos, ref, alt, genome_build="GRCh38"):
    """
    Fetches exome AC/AN and popmax AF via GraphQL using CHROM, POS, REF, ALT information.
    Returns: {
      "Exome_AC": int,
      "Exome_AN": int,
      "PopMax_AF": float,
      "PopMax_Pop": str
    } or {'error': str} if error/missing data
    """
    url = "https://gnomad.broadinstitute.org/api"
    query = """
    query ($variantId: String!) {
      variant(variantId: $variantId, dataset: gnomad_r4) {
        exome {
          ac
          an
          faf95 { popmax popmax_population }
        }
      }
    }
    """
    vid = f"{chrom}-{pos}-{ref}-{alt}"

    try:
        resp = requests.post(url, json={"query": query, "variables": {"variantId": vid}}, timeout=20)
        resp.raise_for_status()
        data = resp.json().get("data", {}).get("variant")

        if data is None:
            logger.warning(f"No data returned for gnomAD variant {vid}")
            return {'error': 'No data returned'}

        ex = data.get("exome", {})
        faf = ex.get("faf95") or {}

        return {
            "Exome_AC": ex.get("ac"),
            "Exome_AN": ex.get("an"),
            "PopMax_AF": faf.get("popmax"),
            "PopMax_Pop": faf.get("popmax_population"),
        }

    except requests.exceptions.RequestException as req_err:
        logger.error(f"HTTP error fetching gnomAD stats for {vid}: {req_err}")
        return {'error': f"HTTP error: {req_err}"}

    except ValueError as val_err:
        logger.error(f"JSON decode error for gnomAD response {vid}: {val_err}")
        return {'error': f"JSON decode error: {val_err}"}

    except Exception as e:
        logger.error(f"Unexpected error in gnomAD handler for {vid}: {e}")
        return {'error': f"Unexpected error: {e}"}