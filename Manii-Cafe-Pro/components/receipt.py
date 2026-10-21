from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from services.order_service import get_order_by_id,get_order_items

def create_pdf_receipt(order_id):
    order=get_order_by_id(order_id)
    if not order: return None
    items=get_order_items(order_id)
    folder=Path("exports/receipts"); folder.mkdir(parents=True,exist_ok=True)
    path=folder/f"{order['order_number']}.pdf"
    c=canvas.Canvas(str(path),pagesize=A4)
    y=800
    c.setFont("Helvetica-Bold",18); c.drawCentredString(297,y,"MANII CAFE PRO"); y-=28
    c.setFont("Helvetica",10); c.drawCentredString(297,y,"Cafe Management & POS"); y-=35
    c.drawString(50,y,f"Order: {order['order_number']}"); y-=16
    c.drawString(50,y,f"Date: {order['created_at']}"); y-=25
    c.line(50,y,545,y); y-=20
    for item in items:
        c.setFont("Helvetica-Bold",10)
        c.drawString(50,y,f"{item['product_name']} ({item['size_name']})")
        c.setFont("Helvetica",10)
        c.drawRightString(545,y,f"{item['quantity']} x Rs {item['unit_price']:,.2f} = Rs {item['total_price']:,.2f}")
        y-=18
    y-=5; c.line(50,y,545,y); y-=20
    for label,value in [("Subtotal",order["subtotal"]),("Discount",order["discount"]),("Tax",order["tax"]),("TOTAL",order["total"])]:
        c.setFont("Helvetica-Bold" if label=="TOTAL" else "Helvetica",11)
        c.drawString(350,y,label); c.drawRightString(545,y,f"Rs {value:,.2f}"); y-=18
    c.drawString(50,y,f"Payment: {order['payment_method']}"); y-=18
    if order["payment_method"]=="Cash":
        c.drawString(50,y,f"Received: Rs {order['amount_received']:,.2f}"); y-=18
        c.drawString(50,y,f"Change: Rs {order['change_amount']:,.2f}"); y-=25
    c.drawCentredString(297,y,"Thank you for visiting MANII CAFE!")
    c.save()
    return str(path)
