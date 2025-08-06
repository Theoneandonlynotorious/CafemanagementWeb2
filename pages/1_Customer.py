import streamlit as st
import uuid
from utils.helpers import load_json, add_order
from utils.invoice import generate_invoice

st.set_page_config(page_title="Customer Panel", layout="wide")
st.title("🧾 Customer Panel")

menu = load_json('menu.json')

st.subheader("📋 Menu")

for item in menu:
    st.write(f"### {item['name']} - ${item['price']}")
    qty = st.number_input(f"Quantity for {item['name']}", min_value=0, key=item['id'])
    if st.button(f"Add {item['name']} to Order", key=f"btn_{item['id']}"):
        if qty > 0:
            order = {
                "id": str(uuid.uuid4()),
                "item": item['name'],
                "price": item['price'],
                "quantity": qty,
                "status": "Received"
            }
            add_order(order)
            st.success(f"{item['name']} x{qty} added to order!")
        else:
            st.warning("Please select a valid quantity.")

# Show customer's orders and allow invoice download
orders = []
try:
    orders = load_json('orders.json')
except FileNotFoundError:
    orders = []

st.subheader("🪪 Your Orders")
for order in orders:
    with st.expander(f"Order ID: {order['id']} - {order['item']} x{order['quantity']}"):
        st.write(f"Status: {order['status']}")
        if st.button("Generate Invoice", key=f"cust_invoice_{order['id']}"):
            file_path = generate_invoice(order)
            with open(file_path, "rb") as f:
                st.download_button(
                    label="📄 Download Invoice",
                    data=f,
                    file_name=file_path.split("/")[-1],
                    mime="application/pdf"
                )
