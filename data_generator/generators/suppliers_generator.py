# data_generator/generators/suppliers_generator.py
import csv
import random
import logging

# Import utility function for Faker
from utils import get_faker_instance
# Import configuration settings
from config import SUPPLIERS_FILE, NUM_ROWS_TO_GENERATE

def generate_suppliers_data():
    """
    Generates synthetic supplier data and saves it to a CSV file.
    Each row includes SupplierID, SupplierName, ContactPerson, Email,
    PhoneNumber, Address, City, State, ZipCode, SupplyCategory, and ContractStartDate.
    """
    # Get a Faker instance
    fake = get_faker_instance()
    # Define the output filename
    filename = SUPPLIERS_FILE
    # Define the number of rows to generate
    num_rows = NUM_ROWS_TO_GENERATE

    logging.info(f"Starting generation of {num_rows} rows for {filename}.")

    try:
        # Open the CSV file in write mode
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Define the headers for the CSV file
            fieldnames = [
                'SupplierID', 'SupplierName', 'ContactPerson', 'Email',
                'PhoneNumber', 'Address', 'City', 'State', 'ZipCode',
                'SupplyCategory', 'ContractStartDate'
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
                    'SupplierID': f'SUPP{i:04d}', # Unique supplier ID
                    'SupplierName': fake.company(),
                    'ContactPerson': fake.name(),
                    'Email': fake.email(),
                    'PhoneNumber': fake.phone_number(),
                    'Address': fake.street_address(),
                    'City': fake.city(),
                    'State': fake.state(),
                    'ZipCode': fake.postcode(),
                    'SupplyCategory': random.choice(['Raw Materials', 'Finished Goods', 'Services', 'Packaging']),
                    'ContractStartDate': fake.date_between(start_date='-10y', end_date='-1y').strftime('%Y-%m-%d')
                })
            logging.info(f"Successfully generated {num_rows} rows for {filename}.")
    except IOError as e:
        # Log any I/O errors during file writing
        logging.error(f"Error writing to {filename}: {e}")
    except Exception as e:
        # Catch any other unexpected errors
        logging.error(f"An unexpected error occurred during supplier data generation: {e}")

# Log that the suppliers generator is loaded
logging.info("Suppliers generator module loaded.")