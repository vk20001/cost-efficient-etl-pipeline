import sys
import logging
from datetime import datetime

sys.path.append("/opt/airflow/src")

from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine

# ---------- Logging Setup ----------
LOG_PATH = "logs/etl.log"
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_metric(msg):
    print(msg)
    logging.info(msg)
# -----------------------------------

# Load environment variables from .env
load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = "5432"
DB_NAME = os.getenv("POSTGRES_DB")

# Create the SQLAlchemy engine
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

RAW_DATA_PATH = os.getenv("RAW_DATA_PATH", "data/raw")

dataset_files = {
    "olist_customers_dataset": "customers",
    "olist_geolocation_dataset": "geolocation",
    "olist_orders_dataset": "orders",
    "olist_order_items_dataset": "order_items",
    "olist_order_payments_dataset": "order_payments",
    "olist_order_reviews_dataset": "order_reviews",
    "olist_products_dataset": "products",
    "olist_sellers_dataset": "sellers",
    "product_category_name_translation": "category_translation"
}

from etl.cleaners.customers_cleaner import clean_customers
from etl.cleaners.geolocation_cleaner import clean_geolocation
from etl.cleaners.orders_cleaner import clean_orders
from etl.cleaners.order_items_cleaner import clean_order_items
from etl.cleaners.order_payments_cleaner import clean_order_payments
from etl.cleaners.order_reviews_cleaner import clean_order_reviews
from etl.cleaners.products_cleaner import clean_products
from etl.cleaners.sellers_cleaner import clean_sellers
from etl.cleaners.category_translation_cleaner import clean_category_translation

CLEANERS = {
    "customers": clean_customers,
    "geolocation": clean_geolocation,
    "orders": clean_orders,
    "order_items": clean_order_items,
    "order_payments": clean_order_payments,
    "order_reviews": clean_order_reviews,
    "products": clean_products,
    "sellers": clean_sellers,
    "category_translation": clean_category_translation
}

def load_and_store_data():
    start_time = datetime.now()
    log_metric("ETL Start: {}".format(start_time.isoformat()))

    for file, table in dataset_files.items():
        try:
            file_path = os.path.join(RAW_DATA_PATH, f"{file}.csv")
            log_metric(f"📥 Reading {file_path}")
            df = pd.read_csv(file_path)
            df.columns = [col.strip().lower() for col in df.columns]

            if table in CLEANERS:
                log_metric(f"🧹 Cleaning '{table}' dataset...")
                df = CLEANERS[table](df)
            else:
                log_metric(f"⚠️  No cleaning logic for '{table}', skipping cleaner.")

            row_count = len(df)
            log_metric(f"📊 '{table}' rows: {row_count}")

            df.to_sql(table, engine, if_exists="replace", index=False)
            log_metric(f"✅ Loaded '{file}' into '{table}'")

        except Exception as e:
            log_metric(f"❌ ERROR processing {file_path} → {str(e)}")

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    log_metric("ETL End: {}".format(end_time.isoformat()))
    log_metric("ETL Duration (s): {}".format(duration))

if __name__ == "__main__":
    load_and_store_data()
