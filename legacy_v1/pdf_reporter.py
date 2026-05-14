from fpdf import FPDF
import datetime

class SentinelReport(FPDF):
    def header(self):
        # Custom Logo and Title
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'SENTINEL GRC: Continuous Compliance Audit', border=False, ln=1, align='C')
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 10, f'Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', border=False, ln=1, align='C')
        self.line(10, 30, 200, 30)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf(findings, filename="Sentinel_Compliance_Report.pdf"):
    pdf = SentinelReport()
    pdf.add_page()
    
    for finding in findings:
        pdf.set_font('helvetica', 'B', 12)
        pdf.set_text_color(220, 53, 69) # Red for violations
        pdf.cell(0, 10, f"[VIOLATION] Trigger: {finding.get('technical_trigger', 'Unknown')}", ln=1)
        
        pdf.set_text_color(0, 0, 0) # Black for text
        pdf.set_font('helvetica', '', 10)
        pdf.multi_cell(0, 8, f"Location: {finding.get('location', 'Unknown')}")
        
        for link in finding.get('regulatory_links', []):
            pdf.set_font('helvetica', 'B', 10)
            pdf.cell(0, 8, f"Regulation: {link['regulation']} | {link['article']}", ln=1)
            pdf.set_font('helvetica', '', 10)
            pdf.multi_cell(0, 8, f"Explanation: {link['explanation']}")
            pdf.multi_cell(0, 8, f"Remediation: {finding.get('standard_remediation', 'N/A')}")
            
        pdf.ln(5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)

    pdf.output(filename)
    print(f"📄 PDF Report successfully generated: {filename}")
