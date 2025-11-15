import pdfkit

def generate_pdf_report(output_file, html_content):
    # If wkhtmltopdf isn't in PATH, set the full path manually:
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    pdfkit.from_string(html_content, output_file, configuration=config)
