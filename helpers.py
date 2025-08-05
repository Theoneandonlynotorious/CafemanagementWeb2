import json

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def add_order(order):
    orders = load_json('orders.json')
    orders.append(order)
    save_json('orders.json', orders)
