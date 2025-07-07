import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfgen import canvas
from datetime import datetime
import io
import matplotlib.pyplot as plt
import numpy as np

class GeneticReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        # Title style - optimized spacing
        self.title_style = ParagraphStyle(
            'CustomTitle', 
            parent=self.styles['Title'],
            fontSize=20, 
            spaceAfter=20,  # Reduced
            spaceBefore=10, # Reduced
            textColor=HexColor('#2C3E50'), 
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=24
        )
        
        # Subtitle style - optimized spacing
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle', 
            parent=self.styles['Heading2'],
            fontSize=14, 
            spaceAfter=12,  # Reduced
            spaceBefore=15, # Reduced
            textColor=HexColor('#3498DB'), 
            fontName='Helvetica-Bold',
            leading=16
        )
        
        # Body text style - optimized
        self.body_style = ParagraphStyle(
            'CustomBody', 
            parent=self.styles['Normal'],
            fontSize=10, 
            spaceAfter=8,   # Reduced
            spaceBefore=3,  # Reduced
            textColor=black, 
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=12,
            leftIndent=0,
            rightIndent=0
        )
        
        # Highlight style
        self.highlight_style = ParagraphStyle(
            'Highlight', 
            parent=self.styles['Normal'],
            fontSize=11, 
            spaceAfter=8,   # Reduced
            spaceBefore=5,  # Reduced
            textColor=HexColor('#E74C3C'), 
            fontName='Helvetica-Bold',
            leading=13
        )
        
        # Comment style - for AI comments
        self.comment_style = ParagraphStyle(
            'Comment',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=8,   # Reduced
            spaceBefore=5,  # Reduced
            textColor=HexColor('#2C3E50'),
            fontName='Helvetica',
            leading=11,
            leftIndent=10,
            rightIndent=10,
            alignment=TA_JUSTIFY
        )

    def create_header_footer(self, canvas_obj, doc):
        canvas_obj.saveState()
        
        # Header
        header_y = A4[1] - 50
        canvas_obj.setFont('Helvetica-Bold', 12)  # Font size reduced
        canvas_obj.setFillColor(HexColor('#2C3E50'))
        canvas_obj.drawString(50, header_y, "🧬 Genetic Variant Analysis Report")
        
        # Header line
        canvas_obj.setStrokeColor(HexColor('#3498DB'))
        canvas_obj.setLineWidth(1)  # Line width reduced
        canvas_obj.line(50, header_y - 8, A4[0] - 50, header_y - 8)
        
        # Footer
        footer_y = 30  # Moved up slightly
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.setFillColor(HexColor('#7F8C8D'))
        canvas_obj.drawString(50, footer_y, f"Report Date: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        canvas_obj.drawRightString(A4[0] - 50, footer_y, f"Page {doc.page}")
        
        canvas_obj.restoreState()

    def create_summary_chart(self, results_df):
        plt.rcParams['font.family'] = ['DejaVu Sans']
        
        fig, axes = plt.subplots(2, 2, figsize=(10, 8))  # Size reduced
        axes = axes.flatten()
        fig.suptitle('Genetic Variant Analysis Summary', fontsize=14, fontweight='bold', y=0.95)
        
        # Clinical significance distribution
        if 'CLNSIG' in results_df.columns and not results_df['CLNSIG'].isna().all():
            cl_counts = results_df['CLNSIG'].value_counts()
            if not cl_counts.empty:
                axes[0].pie(cl_counts.values, labels=cl_counts.index, autopct='%1.1f%%', startangle=90)
                axes[0].set_title('Clinical Significance Distribution', fontweight='bold', pad=15)
            else:
                axes[0].text(0.5, 0.5, 'No data', ha='center', va='center', transform=axes[0].transAxes)
        else:
            axes[0].text(0.5, 0.5, 'CLNSIG data not found', ha='center', va='center', transform=axes[0].transAxes)
        
        # Chromosome distribution
        if 'CHROM' in results_df.columns:
            chr_counts = results_df['CHROM'].value_counts().head(10)
            if not chr_counts.empty:
                axes[1].bar(range(len(chr_counts)), chr_counts.values)
                axes[1].set_xticks(range(len(chr_counts)))
                axes[1].set_xticklabels(chr_counts.index.astype(str), rotation=45)
                axes[1].set_title('Chromosome Distribution', fontweight='bold', pad=15)
                axes[1].set_xlabel('Chromosome')
                axes[1].set_ylabel('Variant Count')
            else:
                axes[1].text(0.5, 0.5, 'No data', ha='center', va='center', transform=axes[1].transAxes)
        
        # Allele frequency distribution
        if 'PopMax_AF' in results_df.columns:
            af_data = pd.to_numeric(results_df['PopMax_AF'], errors='coerce').dropna()
            if not af_data.empty and len(af_data) > 1:
                axes[2].hist(af_data, bins=min(20, len(af_data)), alpha=0.7)
                axes[2].set_title('Allele Frequency Distribution', fontweight='bold', pad=15)
                axes[2].set_xlabel('PopMax AF')
                axes[2].set_ylabel('Variant Count')
            else:
                axes[2].text(0.5, 0.5, 'Insufficient AF data', ha='center', va='center', transform=axes[2].transAxes)
        else:
            axes[2].text(0.5, 0.5, 'No PopMax_AF data', ha='center', va='center', transform=axes[2].transAxes)
        
        # Gene-based distribution
        if 'GENE' in results_df.columns:
            gene_counts = results_df['GENE'].value_counts().head(10)
            if not gene_counts.empty:
                y_pos = range(len(gene_counts))
                axes[3].barh(y_pos, gene_counts.values)
                axes[3].set_yticks(y_pos)
                axes[3].set_yticklabels(gene_counts.index)
                axes[3].set_title('Most Frequent Genes', fontweight='bold', pad=15)
                axes[3].set_xlabel('Variant Count')
            else:
                axes[3].text(0.5, 0.5, 'No gene data', ha='center', va='center', transform=axes[3].transAxes)
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.92])
        
        buf = io.BytesIO()
        plt.savefig(buf, format='PNG', dpi=300, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        plt.close()
        
        return buf

    def generate_report(self, results_df, patient_info=None, output_filename="genetic_report.pdf", report_options=None):
        if report_options is None:
            report_options = {'template': 'Standard Report', 'include_charts': True, 'include_detailed_analysis': True}
        
        # Page settings - margins optimized
        doc = SimpleDocTemplate(
            output_filename, 
            pagesize=A4,
            rightMargin=50, 
            leftMargin=50,
            topMargin=70,   # Space for header
            bottomMargin=50
        )
        
        story = []
        
        # Main title
        story.append(Paragraph("Genetic Variant Analysis Report", self.title_style))
        story.append(Spacer(1, 15))  # Reduced
        
        # Patient information
        if patient_info:
            story.append(Paragraph("Patient Information", self.subtitle_style))
            
            table_data = [
                ["Patient ID:", str(patient_info.get('id', 'N/A'))],
                ["Patient Name:", str(patient_info.get('name', 'N/A'))],
                ["Age:", str(patient_info.get('age', 'N/A'))],
                ["Test Date:", str(patient_info.get('test_date', 'N/A'))],
                ["Report Date:", datetime.now().strftime('%d.%m.%Y %H:%M')],
                ["Total Variants:", str(len(results_df))]
            ]
            
            patient_table = Table(table_data, colWidths=[2.2*inch, 3.3*inch])
            patient_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F8F9FA')),
                ('TEXTCOLOR', (0, 0), (-1, -1), black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#DEE2E6')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            story.append(patient_table)
            story.append(Spacer(1, 20))  # Reduced
        
        # Summary chart
        if report_options.get('include_charts', True):
            story.append(Paragraph("Analysis Summary", self.subtitle_style))
            
            try:
                img_buf = self.create_summary_chart(results_df)
                img = Image(img_buf, width=6*inch, height=4*inch)  # Size reduced
                story.append(img)
                story.append(Spacer(1, 15))  # Reduced
            except Exception as e:
                error_msg = f"Chart could not be created: {str(e)}"
                story.append(Paragraph(error_msg, self.body_style))
                story.append(Spacer(1, 10))
        
        # Clinical significance analysis
        story.append(Paragraph("Clinical Significance Analysis", self.subtitle_style))
        
        if 'CLNSIG' in results_df.columns:
            # Pathogenic variants
            pathogenic_variants = results_df[results_df['CLNSIG'].str.contains('Pathogenic', na=False, case=False)]
            if not pathogenic_variants.empty:
                story.append(Paragraph(f"⚠️ High Risk Variants: {len(pathogenic_variants)} found", self.highlight_style))
                story.append(Paragraph(
                    "These variants are strongly associated with disease development and require clinical follow-up.", 
                    self.body_style
                ))
                story.append(Spacer(1, 8))
            
            # Benign variants
            benign_variants = results_df[results_df['CLNSIG'].str.contains('Benign', na=False, case=False)]
            if not benign_variants.empty:
                story.append(Paragraph(f"✅ Low Risk Variants: {len(benign_variants)} found", self.body_style))
                story.append(Spacer(1, 8))
            
            # Uncertain variants
            uncertain_variants = results_df[results_df['CLNSIG'].str.contains('Uncertain', na=False, case=False)]
            if not uncertain_variants.empty:
                story.append(Paragraph(f"❓ Variants of Uncertain Significance: {len(uncertain_variants)} found", self.body_style))
                story.append(Spacer(1, 15))
        else:
            story.append(Paragraph("Clinical significance data not found.", self.body_style))
            story.append(Spacer(1, 15))
        
        # Detailed variant list
        story.append(Paragraph("Detailed Variant List", self.subtitle_style))
        
        # Select columns for table
        display_columns = ['CHROM', 'POS', 'REF', 'ALT', 'GENE', 'CLNSIG']
        available_columns = [col for col in display_columns if col in results_df.columns]
        
        if available_columns:
            # Show maximum 15 variants
            display_limit = min(15, len(results_df))
            table_data = [available_columns]  # Header
            
            for _, row in results_df.head(display_limit).iterrows():
                row_data = []
                for col in available_columns:
                    value = str(row.get(col, 'N/A'))
                    # Truncate long values
                    if len(value) > 15:
                        value = value[:12] + "..."
                    row_data.append(value)
                table_data.append(row_data)
            
            # Calculate column widths
            col_widths = [inch * 0.75] * len(available_columns)
            if len(available_columns) <= 4:
                col_widths = [inch * 1.2] * len(available_columns)
            
            variant_table = Table(table_data, colWidths=col_widths, repeatRows=1)
            variant_table.setStyle(TableStyle([
                # Header style
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#3498DB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                
                # Data style
                ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F8F9FA')),
                ('TEXTCOLOR', (0, 1), (-1, -1), black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                
                # General
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#DEE2E6')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            
            story.append(variant_table)
            
            if len(results_df) > display_limit:
                story.append(Spacer(1, 10))
                story.append(Paragraph(
                    f"Note: Only the first {display_limit} variants are shown. Total of {len(results_df)} variants were analyzed.",
                    self.body_style
                ))
        else:
            story.append(Paragraph("No variant data available for display.", self.body_style))
        
        story.append(PageBreak())
        
        # AI comments - check for both possible column names
        ai_comment_column = None
        if 'Gemini_Interpretation' in results_df.columns:
            ai_comment_column = 'Gemini_Interpretation'
        elif 'Gemini_Comment' in results_df.columns:
            ai_comment_column = 'Gemini_Comment'
        elif 'AI_Comment' in results_df.columns:
            ai_comment_column = 'AI_Comment'
        elif 'Comment' in results_df.columns:
            ai_comment_column = 'Comment'
        
        if report_options.get('include_detailed_analysis', True) and ai_comment_column:
            story.append(Paragraph("AI Comments", self.subtitle_style))
            
            for idx, (_, row) in enumerate(results_df.iterrows(), 1):
                # Variant title
                variant_info = f"Variant {idx}: {row.get('CHROM', 'N/A')}:{row.get('POS', 'N/A')} {row.get('REF', 'N/A')}>{row.get('ALT', 'N/A')}"
                if 'GENE' in row and pd.notna(row['GENE']):
                    variant_info += f" ({row['GENE']})"
                
                story.append(Paragraph(variant_info, self.subtitle_style))
                
                # Comment text
                comment_text = str(row.get(ai_comment_column, 'Comment not found'))
                # Truncate very long comments
                if len(comment_text) > 2000:
                    comment_text = comment_text[:2000] + "... (Comment truncated)"
                
                story.append(Paragraph(comment_text, self.comment_style))
                story.append(Spacer(1, 12))
        
        # Add page break only if comments exist
        if report_options.get('include_detailed_analysis', True) and ai_comment_column:
            story.append(PageBreak())
        
        # Conclusion and recommendations
        story.append(Paragraph("Conclusion and Recommendations", self.subtitle_style))
        
        conclusion_text = f"""
        This report contains comprehensive analysis of {len(results_df)} genetic variants. 
        The analysis results are prepared based on current scientific literature and clinical databases.
        <br/><br/>
        <b>Important Notes:</b><br/>
        • This report is for informational purposes and does not make definitive diagnoses<br/>
        • For clinical decisions, specialist physician consultation is essential<br/>
        • Genetic counseling is recommended<br/>
        • This analysis is performed in light of current scientific data
        """
        
        story.append(Paragraph(conclusion_text, self.body_style))
        story.append(Spacer(1, 20))
        
        # Footer information
        footer_text = "This report was generated automatically. For questions, consult your genetic specialist."
        footer_style = ParagraphStyle(
            'Footer', 
            parent=self.styles['Normal'], 
            fontSize=8, 
            textColor=HexColor('#7F8C8D'),
            alignment=TA_CENTER,
            spaceAfter=0
        )
        story.append(Paragraph(footer_text, footer_style))
        
        # Create PDF
        doc.build(story, onFirstPage=self.create_header_footer, onLaterPages=self.create_header_footer)
        
        return output_filename

# Helper function for Streamlit
def create_pdf_report_for_streamlit(results_df, patient_info=None, report_options=None):
    """Optimized PDF report generator for Streamlit"""
    generator = GeneticReportGenerator()
    
    if report_options is None:
        report_options = {
            'template': 'Standard Report', 
            'include_charts': True, 
            'include_detailed_analysis': True
        }
    
    import tempfile
    import os
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
        temp_filename = tmp_file.name
    
    try:
        # Generate report
        if report_options['template'] == 'Standard Report':
            # Standard report with first 20 variants
            df_to_use = results_df.head(20)
        else:
            # Full report with all variants
            df_to_use = results_df
        
        generator.generate_report(
            df_to_use, 
            patient_info, 
            temp_filename, 
            report_options
        )
        
        # Read PDF data
        with open(temp_filename, 'rb') as f:
            pdf_data = f.read()
        
        return pdf_data
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)