import os
import pandas as pd
import pytest

from etl.cleaners.customers_cleaner import clean_customers
from etl.cleaners.orders_cleaner import clean_orders
from etl.cleaners.products_cleaner import clean_products

# 📍 Setup paths
RAW_DATA_PATH = "data/raw"

@pytest.mark.parametrize("filename,cleaner", [
    ("olist_customers_dataset.csv", clean_customers),
    ("olist_orders_dataset.csv", clean_orders),
    ("olist_products_dataset.csv", clean_products),
])
def test_cleaners_return_dataframe(filename, cleaner):
    """Test that all cleaners return non-empty DataFrame"""
    path = os.path.join(RAW_DATA_PATH, filename)
    assert os.path.exists(path), f"{filename} not found"

    df = pd.read_csv(path)
    cleaned_df = cleaner(df)

    assert isinstance(cleaned_df, pd.DataFrame)
    assert not cleaned_df.empty, f"{filename} cleaner returned empty DataFrame"

def test_customers_schema():
    """Test expected columns exist after cleaning"""
    df = pd.read_csv(os.path.join(RAW_DATA_PATH, "olist_customers_dataset.csv"))
    df_clean = clean_customers(df)

    expected_cols = {"customer_id", "customer_unique_id", "customer_city", "customer_state"}
    assert expected_cols.issubset(set(df_clean.columns)), "Missing expected columns"

def test_orders_nulls_removed():
    """Ensure no null values in cleaned orders data"""
    df = pd.read_csv(os.path.join(RAW_DATA_PATH, "olist_orders_dataset.csv"))
    df_clean = clean_orders(df)

    assert not df_clean.isnull().any().any(), "Null values still present in cleaned orders"

def test_products_price_positive():
    """Ensure product prices are all non-negative"""
    df = pd.read_csv(os.path.join(RAW_DATA_PATH, "olist_products_dataset.csv"))
    df_clean = clean_products(df)

    if "price" in df_clean.columns:
        assert (df_clean["price"] >= 0).all(), "Negative prices found"
