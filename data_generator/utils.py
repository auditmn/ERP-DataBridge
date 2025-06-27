# data_generator/utils.py
from faker import Faker
import logging

# Initialize Faker with a specific locale for realistic data
def get_faker_instance():
    """
    Initializes and returns a Faker instance with the 'en_IN' locale.
    Using 'en_IN' generates Indian-specific names, addresses, and phone numbers.
    """
    logging.info("Initializing Faker instance with 'en_IN' locale.")
    return Faker('en_IN')

# Log utility functions loaded
logging.info("Utility functions loaded successfully.")