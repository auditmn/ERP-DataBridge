# data_generator/generators/sales_generator.py
import csv
import random
import logging

# Import utility function for Faker
from utils import get_faker_instance
# Import configuration settings
from config import SALES_FILE, NUM_ROWS_TO_GENERATE

def generate_sales_data():
    """
    Generates synthetic sales data and saves it to a CSV file.
    Each row includes SaleID, CustomerID, ProductID, SaleDate, Quantity,
    UnitPrice, TotalPrice, PaymentMethod, ShippingAddress, and Status.
    """
    # Get a Faker instance
    fake = get_faker_instance()
    # Define the output filename
    filename = SALES_FILE
    # Define the number of rows to generate
    num_rows = NUM_ROWS_TO_GENERATE

    logging.info(f"Starting generation of {num_rows} rows for {filename}.")

    try:
        # Open the CSV file in write mode
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Define the headers for the CSV file
            fieldnames = [
                'SaleID', 'CustomerID', 'ProductID', 'SaleDate', 'Quantity',
                'UnitPrice', 'TotalPrice', 'PaymentMethod', 'ShippingAddress',
                'Status'
            ]
            # Create a DictWriter object
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Write the header row to the CSV file
            writer.writeheader()
            logging.info(f"CSV header written for {filename}.")

            # Loop to generate each row of data
            for i in range(1, num_rows + 1):
                # Generate a random sale date within the last 2 years
                sale_date = fake.date_between(start_date='-2y', end_date='today')
                # Generate a random quantity between 1 and 10
                quantity = random.randint(1, 10)
                # Generate a random unit price, rounded to 2 decimal places
                unit_price = round(random.uniform(10.0, 1000.0), 2)
                # Calculate total price
                total_price = round(quantity * unit_price, 2)

                # Write the generated row to the CSV file
                writer.writerow({
                    'SaleID': f'SALE{i:05d}',
                    'CustomerID': f'CUST{random.randint(1, 2000):04d}', # Random customer ID
                    'ProductID': f'PROD{random.randint(1, 1000):04d}', # Random product ID
                    'SaleDate': sale_date.strftime('%Y-%m-%d'),
                    'Quantity': quantity,
                    'UnitPrice': unit_price,
                    'TotalPrice': total_price,
                    'PaymentMethod': random.choice(['Credit Card', 'Cash', 'Online Transfer', 'UPI']),
                    'ShippingAddress': fake.address().replace('\n', ', '),
                    'Status': random.choice(['Completed', 'Pending', 'Shipped', 'Cancelled'])
                })
            logging.info(f"Successfully generated {num_rows} rows for {filename}.")
    except IOError as e:
        # Log any I/O errors during file writing
        logging.error(f"Error writing to {filename}: {e}")
    except Exception as e:
        # Catch any other unexpected errors
        logging.error(f"An unexpected error occurred during sales data generation: {e}")

# Log that the sales generator is loaded
logging.info("Sales generator module loaded.")