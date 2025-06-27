# data_generator/generators/ledger_generator.py
import csv
import random
import logging

# Import utility function for Faker
from utils import get_faker_instance
# Import configuration settings
from config import LEDGER_FILE, NUM_ROWS_TO_GENERATE, INITIAL_LEDGER_BALANCE

def generate_ledger_data():
    """
    Generates synthetic ledger transaction data and saves it to a CSV file.
    Each row includes TransactionID, TransactionDate, AccountName, Description,
    Debit, Credit, Balance, and ReferenceID.
    """
    # Get a Faker instance
    fake = get_faker_instance()
    # Define the output filename
    filename = LEDGER_FILE
    # Define the number of rows to generate
    num_rows = NUM_ROWS_TO_GENERATE

    logging.info(f"Starting generation of {num_rows} rows for {filename}.")

    try:
        # Open the CSV file in write mode
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Define the headers for the CSV file
            fieldnames = [
                'TransactionID', 'TransactionDate', 'AccountName', 'Description',
                'Debit', 'Credit', 'Balance', 'ReferenceID'
            ]
            # Create a DictWriter object
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Write the header row to the CSV file
            writer.writeheader()
            logging.info(f"CSV header written for {filename}.")

            # Initialize current balance
            current_balance = INITIAL_LEDGER_BALANCE
            logging.info(f"Initial ledger balance set to {current_balance}.")

            # Loop to generate each row of data
            for i in range(1, num_rows + 1):
                # Generate a random transaction date
                transaction_date = fake.date_between(start_date='-3y', end_date='today')
                # Randomly choose a transaction type
                transaction_type = random.choice(['Sale', 'Purchase', 'Expense', 'Payment Received', 'Payment Made'])
                debit = 0.0
                credit = 0.0
                reference_id = ''

                # Assign debit/credit based on transaction type
                if transaction_type in ['Sale', 'Payment Received']:
                    credit = round(random.uniform(50.0, 5000.0), 2)
                    current_balance += credit
                    reference_id = f'SALE{random.randint(1, 5000):05d}' if transaction_type == 'Sale' else ''
                else:
                    debit = round(random.uniform(20.0, 2000.0), 2)
                    current_balance -= debit
                    reference_id = f'PURC{random.randint(1, 5000):05d}' if transaction_type == 'Purchase' else ''

                # Write the generated row to the CSV file
                writer.writerow({
                    'TransactionID': f'TRN{i:06d}', # Unique transaction ID
                    'TransactionDate': transaction_date.strftime('%Y-%m-%d'),
                    'AccountName': random.choice(['Sales Revenue', 'Accounts Receivable', 'Cash', 'Bank', 'Cost of Goods Sold', 'Accounts Payable', 'Expenses']),
                    'Description': f'{transaction_type} transaction',
                    'Debit': debit,
                    'Credit': credit,
                    'Balance': round(current_balance, 2),
                    'ReferenceID': reference_id
                })
            logging.info(f"Successfully generated {num_rows} rows for {filename}.")
    except IOError as e:
        # Log any I/O errors during file writing
        logging.error(f"Error writing to {filename}: {e}")
    except Exception as e:
        # Catch any other unexpected errors
        logging.error(f"An unexpected error occurred during ledger data generation: {e}")

# Log that the ledger generator is loaded
logging.info("Ledger generator module loaded.")