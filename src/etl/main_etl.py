import os
import time
import pandas as pd
import logging
import yaml
from prometheus_client import Counter, Summary, start_http_server

# ------------------------------
# Load config
# ------------------------------
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../../config/config.yaml")
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

input_file = config["input_file"]
output_file = config["output_file"]
log_file = config["log_file"]
columns_to_keep = config["columns_to_keep"]

# ------------------------------
# Override paths for local testing
# ------------------------------
if not os.path.exists("/.dockerenv"):  # Not running inside Docker
    input_file = "data/raw/sales_data.csv"
    output_file = "data/processed/processed_sales.csv"
    log_file = "logs/etl.log"

# ------------------------------
# Ensure log directory exists
# ------------------------------
log_dir = os.path.dirname(log_file)
os.makedirs(log_dir, exist_ok=True)

# ------------------------------
# Logging setup
# ------------------------------
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------------------
# Prometheus metrics
# ------------------------------
RUNS_TOTAL     = Counter("etl_runs_total", "Successful ETL runs")
FAILURES_TOTAL = Counter("etl_failures_total", "Failed ETL runs")
DURATION_SEC   = Summary("etl_duration_seconds", "ETL job duration in seconds")

# Start Prometheus metrics server
start_http_server(8000, addr='0.0.0.0')


# ------------------------------
# ETL function
# ------------------------------
@DURATION_SEC.time()
def run_etl():
    try:
        logging.info("Starting ETL process...")

        df = pd.read_csv(input_file)
        logging.info(f"Loaded input data with shape {df.shape}")

        df = df[columns_to_keep]
        logging.info(f"Filtered columns: {columns_to_keep}")

        # Add total_sales
        df["total_sales"] = df["quantity"] * df["price"]
        logging.info("Calculated total_sales")

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file, index=False)
        logging.info(f"Saved processed data to {output_file}")

        RUNS_TOTAL.inc()
        logging.info("ETL pipeline finished successfully ✅")

    except Exception as e:
        FAILURES_TOTAL.inc()
        logging.error(f"ETL process failed: {e}", exc_info=True)
        raise

# ------------------------------
# Entry point
# ------------------------------
if __name__ == "__main__":
    run_etl()
    print("ETL done, starting infinite loop to keep metrics server alive...")
    while True:
        time.sleep(10)
