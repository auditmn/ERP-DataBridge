# main.py
import logging
import os

# Import generator functions from their respective modules
from generators.sales_generator import generate_sales_data
from generators.inventory_generator import generate_inventory_data
from generators.ledger_generator import generate_ledger_data
from generators.customers_generator import generate_customers_data
from generators.purchases_generator import generate_purchases_data
from generators.suppliers_generator import generate_suppliers_data

# Import configuration settings to ensure logging is set up early
from config import (
    NUM_ROWS_TO_GENERATE,
    SALES_FILE,
    INVENTORY_FILE,
    LEDGER_FILE,
    CUSTOMERS_FILE,
    PURCHASES_FILE,
    SUPPLIERS_FILE,
    OUTPUT_DIR
)

def run_all_generators():
    """
    Executes all data generation functions to create the required CSV files.
    Logs the start and completion of each generation process.
    """
    logging.info("Starting ERP data generation process.")

    # Call each data generation function
    logging.info(f"Generating sales data into {SALES_FILE}...")
    generate_sales_data()

    logging.info(f"Generating inventory data into {INVENTORY_FILE}...")
    generate_inventory_data()

    logging.info(f"Generating ledger data into {LEDGER_FILE}...")
    generate_ledger_data()

    logging.info(f"Generating customers data into {CUSTOMERS_FILE}...")
    generate_customers_data()

    logging.info(f"Generating purchases data into {PURCHASES_FILE}...")
    generate_purchases_data()

    logging.info(f"Generating suppliers data into {SUPPLIERS_FILE}...")
    generate_suppliers_data()

    logging.info(f"All CSV files generated successfully with at least {NUM_ROWS_TO_GENERATE} rows each.")
    logging.info("ERP data generation process completed.")

if __name__ == "__main__":
    # Ensure the output directory exists if needed (though files are written to current dir)
    # If you want them in a 'data' subfolder, uncomment and modify:
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        logging.info(f"Created output directory: {OUTPUT_DIR}")

    # Run the main generation process
    run_all_generators()