import streamlit as st
from utils.helpers import load_json, save_json
from utils.invoice import generate_invoice

st.set_page_config(page_title="Admin Panel", layout="wide")
st.title("🛠️ Admin Panel")

menu = load_json("menu.json")
orders = load_json("orders.json")

# Menu Management
st.subheader("🍔 Manage Menu")
for item in menu:
    st.write(f"{item['name']} - ${item['price']}")

name = st.text_input("New Item Name")
price = st.number_input("Price", min_value=0.0)
if st.button("Add to Menu"):
    if name:
        menu.append({"id": len(menu)+1, "name": name, "price": price})
        save_json("menu.json", menu)
        st.success("Item added to menu.")
        st.experimental_rerun()

# Orders Overview
st.subheader("📦 All Orders")
for order in orders:
    with st.expander(f"Order ID: {order['id']} - {order['item']} x{order['quantity']}"):
        st.write(f"Status: {order['status']}")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Mark as Completed", key=f"done_{order['id']}"):
                for o in orders:
                    if o['id'] == order['id']:
                        o['status'] = "Completed"
                save_json("orders.json", orders)
                st.success("Order marked as Completed.")
                st.experimental_rerun()

        with col2:
            if st.button("Delete Order", key=f"del_{order['id']}"):
                orders = [o for o in orders if o['id'] != order['id']]
                save_json("orders.json", orders)
                st.warning("Order deleted.")
                st.experimental_rerun()

        with col3:
            if st.button("Generate Invoice", key=f"inv_{order['id']}"):
                file_path = generate_invoice(order)
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="📄 Download Invoice",
                        data=f,
                        file_name=file_path.split("/")[-1],
                        mime="application/pdf"
                    )
