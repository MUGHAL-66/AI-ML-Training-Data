from datetime import datetime

def generate_order_number():
    return datetime.now().strftime("ORD-%Y%m%d-%H%M%S-%f")[:-3]

def money(value):
    return f"Rs {float(value or 0):,.2f}"

def today():
    return datetime.now().strftime("%Y-%m-%d")
