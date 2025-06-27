# data_generator/generators/purchases_generator.py
import csv
import random
import logging

# Import utility function for Faker
from utils import get_faker_instance
# Import configuration settings
from config import PURCHASES_FILE, NUM_ROWS_TO_GENERATE

def generate_purchases_data():
    """
    Generates synthetic purchase order data and saves it to a CSV file.
    Each row includes PurchaseID, SupplierID, ProductID, PurchaseDate,
    Quantity, UnitPrice, TotalPrice, PaymentStatus, and DeliveryStatus.
    """
    # Get a Faker instance
    fake = get_faker_instance()
    # Define the output filename
    filename = PURCHASES_FILE
    # Define the number of rows to generate
    num_rows = NUM_ROWS_TO_GENERATE

    logging.info(f"Starting generation of {num_rows} rows for {filename}.")

    try:
        # Open the CSV file in write mode
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Define the headers for the CSV file
            fieldnames = [
                'PurchaseID', 'SupplierID', 'ProductID', 'PurchaseDate',
                'Quantity', 'UnitPrice', 'TotalPrice', 'PaymentStatus',
                'DeliveryStatus'
            ]
            # Create a DictWriter object
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Write the header row to the CSV file
            writer.writeheader()
            logging.info(f"CSV header written for {filename}.")

            # Loop to generate each row of data
            for i in range(1, num_rows + 1):
                # Generate a random purchase date
                purchase_date = fake.date_between(start_date='-2y', end_date='today')
                # Generate a random quantity
                quantity = random.randint(5, 50)
                # Generate a random unit price
                unit_price = round(random.uniform(5.0, 500.0), 2)
                # Calculate total price
                total_price = round(quantity * unit_price, 2)

                # Write the generated row to the CSV file
                writer.writerow({
                    'PurchaseID': f'PURC{i:05d}', # Unique purchase ID
                    'SupplierID': f'SUPP{random.randint(1, 500):04d}', # Random supplier ID
                    'ProductID': f'PROD{random.randint(1, 1000):04d}', # Random product ID
                    'PurchaseDate': purchase_date.strftime('%Y-%m-%d'),
                    'Quantity': quantity,
                    'UnitPrice': unit_price,
                    'TotalPrice': total_price,
                    'PaymentStatus': random.choice(['Paid', 'Pending', 'Overdue']),
                    'DeliveryStatus': random.choice(['Delivered', 'Pending', 'Shipped', 'Cancelled'])
                })
            logging.info(f"Successfully generated {num_rows} rows for {filename}.")
    except IOError as e:
        # Log any I/O errors during file writing
        logging.error(f"Error writing to {filename}: {e}")
    except Exception as e:
        # Catch any other unexpected errors
        logging.error(f"An unexpected error occurred during purchases data generation: {e}")

# Log that the purchases generator is loaded
logging.info("Purchases generator module loaded.")