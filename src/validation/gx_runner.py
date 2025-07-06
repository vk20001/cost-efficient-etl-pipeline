import os
import great_expectations as gx


def _ensure_datasource(context):
    ds_name = "brazil_etl"
    if ds_name in context.datasources:
        return
    conn_str = (
        f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@postgres:5432/{os.getenv('POSTGRES_DB')}"
    )
    context.sources.add_sql(name=ds_name, connection_string=conn_str)


def run_all_checkpoints():
    context = gx.get_context()
    _ensure_datasource(context)

    checkpoint_names = [
        "customers_checkpoint",
        "geolocation_checkpoint",
        "orders_checkpoint",
        "order_items_checkpoint",
        "order_payments_checkpoint",
        "order_reviews_checkpoint",
        "products_checkpoint",
        "sellers_checkpoint",
        "category_translation_checkpoint",
    ]

    for cp in checkpoint_names:
        print(f"🚦 Running checkpoint: {cp}")
        result = context.run_checkpoint(checkpoint_name=cp)
        if not result["success"]:
            raise Exception(f"❌ Validation failed for {cp}")
        print(f"✅ Passed: {cp}")
