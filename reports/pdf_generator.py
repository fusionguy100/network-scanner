from reportlab.pdfgen import canvas

def generate_pdf_report(output_file, text):
    c = canvas.Canvas(output_file)
    c.setFont("Helvetica", 10)

    y = 800
    for line in text.split("\n"):
        c.drawString(40, y, line)
        y -= 14

        if y < 40:
            c.showPage()
            y = 800

    c.save()
