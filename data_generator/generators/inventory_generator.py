# data_generator/generators/inventory_generator.py
import csv
import random
import logging

# Import utility function for Faker
from utils import get_faker_instance
# Import configuration settings
from config import INVENTORY_FILE, NUM_ROWS_TO_GENERATE

def generate_inventory_data():
    """
    Generates synthetic inventory data and saves it to a CSV file.
    Each row includes ProductID, ProductName, Category, CurrentStock,
    ReorderLevel, WarehouseLocation, and LastStockUpdate.
    """
    # Get a Faker instance
    fake = get_faker_instance()
    # Define the output filename
    filename = INVENTORY_FILE
    # Define the number of rows to generate
    num_rows = NUM_ROWS_TO_GENERATE

    logging.info(f"Starting generation of {num_rows} rows for {filename}.")

    try:
        # Open the CSV file in write mode
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Define the headers for the CSV file
            fieldnames = [
                'ProductID', 'ProductName', 'Category', 'CurrentStock',
                'ReorderLevel', 'WarehouseLocation', 'LastStockUpdate'
            ]
            # Create a DictWriter object
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Write the header row to the CSV file
            writer.writeheader()
            logging.info(f"CSV header written for {filename}.")

            # Loop to generate each row of data
            for i in range(1, num_rows + 1):
                # Write the generated row to the CSV file
                writer.writerow({
                    'ProductID': f'PROD{i:04d}', # Unique product ID
                    'ProductName': fake.word().capitalize() + ' ' + random.choice(['Shirt', 'Pants', 'Shoes', 'Hat', 'Accessory', 'Gadget', 'Book']),
                    'Category': random.choice(['Electronics', 'Apparel', 'Home Goods', 'Books', 'Food', 'Sporting Goods']),
                    'CurrentStock': random.randint(0, 500), # Random stock level
                    'ReorderLevel': random.randint(10, 50), # Random reorder level
                    'WarehouseLocation': fake.word().upper() + '-' + str(random.randint(1, 10)),
                    'LastStockUpdate': fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
                })
            logging.info(f"Successfully generated {num_rows} rows for {filename}.")
    except IOError as e:
        # Log any I/O errors during file writing
        logging.error(f"Error writing to {filename}: {e}")
    except Exception as e:
        # Catch any other unexpected errors
        logging.error(f"An unexpected error occurred during inventory data generation: {e}")

# Log that the inventory generator is loaded
logging.info("Inventory generator module loaded.")