#!/usr/bin/env python3
"""
Generate synthetic order data for the pipeline trial assignment.

Usage:
    python scripts/generate_data.py --num-orders 5000 --output-dir data/raw

The seed data included in data/raw/ is sufficient for the assignment.
This script is provided in case candidates want to regenerate the dataset
or produce different volumes for load testing / idempotency checks.
"""

import argparse
import csv
import json
import os
import random
from datetime import datetime, timedelta

PRODUCTS = [
    # Electronics — Peripherals
    {"product_id": "PROD-A1", "product_name": "Wireless Mouse", "category": "Electronics", "subcategory": "Peripherals", "cost_price": 12.50, "weight_kg": 0.15},
    {"product_id": "PROD-D4", "product_name": "Ergonomic Keyboard", "category": "Electronics", "subcategory": "Peripherals", "cost_price": 32.00, "weight_kg": 0.85},
    {"product_id": "PROD-K11", "product_name": "Webcam 1080p", "category": "Electronics", "subcategory": "Peripherals", "cost_price": 18.00, "weight_kg": 0.12},
    # Electronics — Audio
    {"product_id": "PROD-B2", "product_name": "Noise-Cancelling Headphones", "category": "Electronics", "subcategory": "Audio", "cost_price": 65.00, "weight_kg": 0.35},
    {"product_id": "PROD-H8", "product_name": "Bluetooth Speaker", "category": "Electronics", "subcategory": "Audio", "cost_price": 22.00, "weight_kg": 0.60},
    # Electronics — Displays
    {"product_id": "PROD-E5", "product_name": '27" Monitor', "category": "Electronics", "subcategory": "Displays", "cost_price": 89.00, "weight_kg": 4.20},
    {"product_id": "PROD-L12", "product_name": "Portable Monitor 15.6\"", "category": "Electronics", "subcategory": "Displays", "cost_price": 55.00, "weight_kg": 0.90},
    # Electronics — Accessories
    {"product_id": "PROD-C3", "product_name": "USB-C Cable (2m)", "category": "Electronics", "subcategory": "Accessories", "cost_price": 3.20, "weight_kg": 0.05},
    {"product_id": "PROD-F6", "product_name": "USB-C Hub 7-in-1", "category": "Electronics", "subcategory": "Accessories", "cost_price": 14.00, "weight_kg": 0.10},
    {"product_id": "PROD-G7", "product_name": "Laptop Stand — Aluminum", "category": "Electronics", "subcategory": "Accessories", "cost_price": 15.00, "weight_kg": 1.20},
    # Office — Furniture
    {"product_id": "PROD-I9", "product_name": "Desk Lamp LED", "category": "Office", "subcategory": "Furniture", "cost_price": 11.00, "weight_kg": 0.70},
    {"product_id": "PROD-M13", "product_name": "Monitor Arm — Single", "category": "Office", "subcategory": "Furniture", "cost_price": 28.00, "weight_kg": 3.10},
    # Office — Supplies
    {"product_id": "PROD-J10", "product_name": "Notebook — Dotted A5", "category": "Office", "subcategory": "Supplies", "cost_price": 2.00, "weight_kg": 0.18},
    {"product_id": "PROD-N14", "product_name": "Whiteboard Markers (8-pack)", "category": "Office", "subcategory": "Supplies", "cost_price": 3.50, "weight_kg": 0.15},
    {"product_id": "PROD-O15", "product_name": "Cable Management Kit", "category": "Office", "subcategory": "Supplies", "cost_price": 5.00, "weight_kg": 0.25},
]

# Retail prices per product (keyed by product_id)
PRICES = {
    "PROD-A1": 29.99,
    "PROD-B2": 149.99,
    "PROD-C3": 9.99,
    "PROD-D4": 74.50,
    "PROD-E5": 199.99,
    "PROD-F6": 39.99,
    "PROD-G7": 49.95,
    "PROD-H8": 59.99,
    "PROD-I9": 34.99,
    "PROD-J10": 12.99,
    "PROD-K11": 54.99,
    "PROD-L12": 149.00,
    "PROD-M13": 89.99,
    "PROD-N14": 14.99,
    "PROD-O15": 19.99,
}

COUNTRIES = ["US", "US", "US", "CA", "UK", "DE", "FR", "JP", "AU", "NL", "SE", "BR", "MX"]
# Weighted: ~60% completed, ~15% pending, ~15% shipped, ~10% cancelled
STATUSES = [
    "completed", "completed", "completed", "completed", "completed", "completed",
    "pending", "pending",
    "shipped", "shipped",
    "cancelled",
]


def generate_orders(num_orders: int, start_date: str = "2024-01-01", days_span: int = 90) -> list[dict]:
    random.seed(42)
    base_date = datetime.strptime(start_date, "%Y-%m-%d")
    product_ids = list(PRICES.keys())
    orders = []

    for i in range(1, num_orders + 1):
        product_id = random.choice(product_ids)
        order_date = base_date + timedelta(days=random.randint(0, days_span - 1))
        quantity = random.choices([1, 2, 3, 4, 5, 6, 8, 10], weights=[40, 25, 15, 8, 5, 3, 2, 2])[0]

        orders.append({
            "order_id": f"ORD-{i:05d}",
            "customer_id": f"CUST-{random.randint(1000, 1499)}",
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": PRICES[product_id],
            "order_date": order_date.strftime("%Y-%m-%d"),
            "status": random.choice(STATUSES),
            "shipping_country": random.choice(COUNTRIES),
        })

    return orders


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic order data")
    parser.add_argument("--num-orders", type=int, default=5000, help="Number of orders to generate")
    parser.add_argument("--output-dir", type=str, default="data/raw", help="Output directory")
    parser.add_argument("--start-date", type=str, default="2024-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--days-span", type=int, default=90, help="Number of days the orders span")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    # Write orders CSV
    orders = generate_orders(args.num_orders, args.start_date, args.days_span)
    orders_path = os.path.join(args.output_dir, "orders.csv")
    with open(orders_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=orders[0].keys())
        writer.writeheader()
        writer.writerows(orders)
    print(f"Wrote {len(orders)} orders to {orders_path}")

    # Write products JSON
    products_path = os.path.join(args.output_dir, "products.json")
    with open(products_path, "w") as f:
        json.dump(PRODUCTS, f, indent=2)
    print(f"Wrote {len(PRODUCTS)} products to {products_path}")


if __name__ == "__main__":
    main()
