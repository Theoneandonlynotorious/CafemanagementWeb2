import streamlit as st
from utils.helpers import load_json, save_json

st.set_page_config(page_title="Chef Panel", layout="wide")
st.title("👨‍🍳 Chef Panel")

orders = load_json("orders.json")
received_orders = [o for o in orders if o['status'] == "Received"]

if not received_orders:
    st.info("No new orders.")
else:
    for order in received_orders:
        st.write(f"### Order ID: {order['id']}")
        st.write(f"- Item: {order['item']} x{order['quantity']}")
        if st.button("Mark as Preparing", key=order['id']):
            for o in orders:
                if o['id'] == order['id']:
                    o['status'] = "Preparing"
                    break
            save_json("orders.json", orders)
            st.success("Order marked as Preparing.")
            st.rerun()
