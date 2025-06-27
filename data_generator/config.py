# data_generator/config.py
import logging
import os # Import os module here as well

# Configure logging for the entire application
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- NEW: Define the output directory ---
OUTPUT_DIR = 'data'

# Number of rows to generate for each CSV file
NUM_ROWS_TO_GENERATE = 10000

# Output filenames (just the base names)
SALES_BASENAME = 'sales.csv'
INVENTORY_BASENAME = 'inventory.csv'
LEDGER_BASENAME = 'ledger.csv'
CUSTOMERS_BASENAME = 'customers.csv'
PURCHASES_BASENAME = 'purchases.csv'
SUPPLIERS_BASENAME = 'suppliers.csv'

# Full paths for the files
SALES_FILE = os.path.join(OUTPUT_DIR, SALES_BASENAME)
INVENTORY_FILE = os.path.join(OUTPUT_DIR, INVENTORY_BASENAME)
LEDGER_FILE = os.path.join(OUTPUT_DIR, LEDGER_BASENAME)
CUSTOMERS_FILE = os.path.join(OUTPUT_DIR, CUSTOMERS_BASENAME)
PURCHASES_FILE = os.path.join(OUTPUT_DIR, PURCHASES_BASENAME)
SUPPLIERS_FILE = os.path.join(OUTPUT_DIR, SUPPLIERS_BASENAME)

# Base balance for ledger
INITIAL_LEDGER_BALANCE = 1000000.0

# Log configuration loaded
logging.info("Configuration parameters loaded successfully, including output directory.")