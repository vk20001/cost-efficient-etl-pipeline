import great_expectations as gx
import sys

def validate_data(data_path: str, expectation_suite_name: str = "processed_data_suite"):
    # Initialize the Data Context
    context = gx.get_context()

    # Define the batch request
    batch_request = {
        "datasource_name": "cost_etl",
        "data_connector_name": "default_inferred_data_connector_name",
        "data_asset_name": 'processed_sales.csv',  # Use passed argument
        "limit": 1000,
    }

    # Run the checkpoint
    results = context.run_checkpoint(
        checkpoint_name="validation_checkpoint",
        validations=[{
            "batch_request": batch_request,
            "expectation_suite_name": expectation_suite_name,
        }],
    )

    if not results["success"]:
        print("Validation failed!")
        sys.exit(1)  # Exit with error to stop pipeline or alert

    print("Validation passed!")
    return results

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_data.py <data_file_name>")
        sys.exit(1)

    data_file = sys.argv[1]
    validate_data(data_file)
