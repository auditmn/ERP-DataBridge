# data_generator/generators/customers_generator.py
import csv
import logging

# Import utility function for Faker
from utils import get_faker_instance
# Import configuration settings
from config import CUSTOMERS_FILE, NUM_ROWS_TO_GENERATE

def generate_customers_data():
    """
    Generates synthetic customer data and saves it to a CSV file.
    Each row includes CustomerID, FirstName, LastName, Email, PhoneNumber,
    Address, City, State, ZipCode, and RegistrationDate.
    """
    # Get a Faker instance
    fake = get_faker_instance()
    # Define the output filename
    filename = CUSTOMERS_FILE
    # Define the number of rows to generate
    num_rows = NUM_ROWS_TO_GENERATE

    logging.info(f"Starting generation of {num_rows} rows for {filename}.")

    try:
        # Open the CSV file in write mode
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Define the headers for the CSV file
            fieldnames = [
                'CustomerID', 'FirstName', 'LastName', 'Email', 'PhoneNumber',
                'Address', 'City', 'State', 'ZipCode', 'RegistrationDate'
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
                    'CustomerID': f'CUST{i:04d}', # Unique customer ID
                    'FirstName': fake.first_name(),
                    'LastName': fake.last_name(),
                    'Email': fake.email(),
                    'PhoneNumber': fake.phone_number(),
                    'Address': fake.street_address(),
                    'City': fake.city(),
                    'State': fake.state(),
                    'ZipCode': fake.postcode(),
                    'RegistrationDate': fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d')
                })
            logging.info(f"Successfully generated {num_rows} rows for {filename}.")
    except IOError as e:
        # Log any I/O errors during file writing
        logging.error(f"Error writing to {filename}: {e}")
    except Exception as e:
        # Catch any other unexpected errors
        logging.error(f"An unexpected error occurred during customer data generation: {e}")

# Log that the customers generator is loaded
logging.info("Customers generator module loaded.")