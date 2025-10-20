from fpdf import FPDF

def save_summary_to_pdf(summary, filename="reddit_report.pdf"):
    """Generate a simple PDF summary report."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Weekly Reddit Pain Points Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, "Top 5 recurring pain points identified from Reddit:\n", align="L")
    pdf.ln(5)

    for idx, line in enumerate(summary.split('\n')):
        if line.strip():
            pdf.set_font("Arial", "B", 12)
            pdf.cell(10, 10, f"{idx+1}.", ln=0)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, line.strip())
            pdf.ln(2)

    pdf.output(filename)
    print(f"📄 PDF report generated successfully: {filename}")
