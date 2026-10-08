from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

OUTPUT_DIR = Path("generated_certificates")
TEMPLATE_PATH = Path("templates/certificate_template.png")
OUTPUT_DIR.mkdir(exist_ok=True)

def generate_certificate(
    recipient_name: str,
    event_name: str,
    issue_date: str,
    recipient_id: int
):
    file_path = OUTPUT_DIR / f"certificate_{recipient_id}.pdf"

    page_width, page_height = landscape(A4)

    pdf = canvas.Canvas(
        str(file_path),
        pagesize=(page_width, page_height)
    )

    pdf.drawImage(
        str(TEMPLATE_PATH),
        0,
        0,
        width=page_width,
        height=page_height
    )

    pdf.setFillColorRGB(0.05, 0.12, 0.25)
    pdf.setFont("Times-BoldItalic", 34)
    pdf.drawCentredString(
        page_width / 2,
        280,
        recipient_name
    )

    pdf.setFont("Times-Bold", 19)
    pdf.drawCentredString(
        page_width / 2,
        180,
        event_name
    )

    formatted_date = datetime.strptime(
        issue_date,
        "%Y-%m-%d"
    ).strftime("%d %B %Y")

    pdf.setFont("Times-Roman", 13)
    pdf.drawCentredString(
        page_width / 2,
        80,
        formatted_date
    )

    pdf.save()
    return str(file_path)