"""
Example test — provided for reference.

Candidates should add their own tests alongside this file.
"""

import os


def test_raw_data_exists():
    """Verify the seed data files are present."""
    raw_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
    assert os.path.isfile(os.path.join(raw_dir, "orders.csv"))
    assert os.path.isfile(os.path.join(raw_dir, "orders_v2_sample.csv"))
    assert os.path.isfile(os.path.join(raw_dir, "products.json"))
