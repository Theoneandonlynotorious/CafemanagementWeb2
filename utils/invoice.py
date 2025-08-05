from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

def generate_invoice(order):
    filename = f"invoices/invoice_{order['id']}.pdf"
    os.makedirs("invoices", exist_ok=True)

    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Smart Café - Invoice", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Order ID: {order['id']}", styles['Normal']))
    elements.append(Spacer(1, 12))

    data = [
        ["Item", "Quantity", "Price", "Total"],
        [order['item'], order['quantity'], f"${order['price']}", f"${order['price'] * order['quantity']}"]
    ]

    table = Table(data, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 24))
    total_price = order['price'] * order['quantity']
    elements.append(Paragraph(f"<b>Total: ${total_price:.2f}</b>", styles['Heading3']))

    doc.build(elements)
    return filename
