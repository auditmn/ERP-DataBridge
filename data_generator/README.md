# ERP Synthetic Data Generator

This project provides a Python-based solution to generate realistic, synthetic ERP (Enterprise Resource Planning) data across various domains such as Sales, Inventory, Ledger, Customers, Purchases, and Suppliers. The generated data is formatted as CSV files and designed with inter-table consistency to allow for joins, simulating a real-world ERP export.

The project is structured into modular, small files, each with comprehensive comments and logging, making it easy to understand, maintain, and extend.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [How to Run](#how-to-run)
- [Output Files](#output-files)
- [Data Consistency and Joinability](#data-consistency-and-joinability)
- [Configuration](#configuration)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)

## Features

* **Generates 6 Core ERP Datasets:**
    * `sales.csv`
    * `inventory.csv`
    * `ledger.csv`
    * `customers.csv`
    * `purchases.csv`
    * `suppliers.csv`
* **Large Dataset Generation:** Each CSV file contains at least 10,000 rows by default.
* **Realistic Data:** Uses the `Faker` library to generate plausible names, addresses, dates, and other details. Indian locale (`en_IN`) is used for more relevant data where applicable.
* **Data Consistency:** IDs are generated and cross-referenced across files (e.g., `CustomerID` in `sales.csv` links to `customers.csv`) to enable joins.
* **Modular Codebase:** Split into small, manageable Python files (each under 1KB for core logic).
* **Comprehensive Comments & Logging:** Every significant step in the code is commented and logs its activity, providing transparency and aiding in debugging.
* **Configurable:** Easily adjust the number of rows, output directory, and other parameters via a central `config.py` file.

## Project Structure

The project is organized into a `data_generator` package for better modularity:

data/
├── init.py           # Makes data_generator a Python package
├── main.py               # Main script to run all data generators
├── config.py             # Centralized configuration settings
├── utils.py              # Utility functions (e.g., Faker initialization)
├── generators/           # Directory for individual data generation modules
│   ├── init.py       # Makes generators a Python sub-package
│   ├── sales_generator.py
│   ├── inventory_generator.py
│   ├── ledger_generator.py
│   ├── customers_generator.py
│   ├── purchases_generator.py
│   └── suppliers_generator.py


## Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.7+**: You can download it from [python.org](https://www.python.org/downloads/).

## Setup and Installation

Follow these steps to set up the project on your local machine:

1.  **Clone the repository (if applicable) or create the project structure:**
    If this project is part of a Git repository, clone it:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```
    Otherwise, manually create the directory structure as shown in [Project Structure](#project-structure).

2.  **Navigate into the `data_generator` directory:**
    ```bash
    cd data_generator
    ```

3.  **Install the required Python libraries:**
    The project relies on the `Faker` library. Install it using pip:
    ```bash
    pip install Faker
    ```

## How to Run

Once the setup is complete, you can generate the data with a single command:

1.  **Ensure you are in the `data_generator` directory** (the one containing `main.py`).

2.  **Execute the `main.py` script:**
    ```bash
    python main.py
    ```

    You will see log messages in your terminal indicating the progress of data generation for each file.

3.  **Check the output:**
    Upon successful completion, a new directory named `data` will be created in the `data_generator` folder, and all generated CSV files will be located inside it.

    For example, the files will be found at:
    ```
    data_generator/
    └── data/
        ├── sales.csv
        ├── inventory.csv
        ├── ledger.csv
        ├── customers.csv
        ├── purchases.csv
        └── suppliers.csv
    ```

## Output Files

The following CSV files will be generated in the `data/` subdirectory:

* `sales.csv`: Contains records of sales transactions.
* `inventory.csv`: Details of products and their stock levels.
* `ledger.csv`: Financial transaction records (debits and credits).
* `customers.csv`: Information about registered customers.
* `purchases.csv`: Records of procurement/purchase orders.
* `suppliers.csv`: Details of various suppliers.

## Data Consistency and Joinability

The generated data is designed to simulate relationships found in real ERP systems, allowing for joins between the CSV files. This is achieved by:

* **Consistent ID Generation:** Unique identifiers (e.g., `CustomerID`, `ProductID`, `SupplierID`) are generated with specific prefixes and numerical ranges.
* **Simulated Foreign Keys:** Transactional tables (e.g., `sales.csv`, `purchases.csv`) use IDs that are guaranteed to exist within their respective master data tables (e.g., `customers.csv`, `inventory.csv`, `suppliers.csv`).
* **`ledger.csv` References:** The `ReferenceID` in `ledger.csv` aims to link to `SaleID` or `PurchaseID` based on the transaction type, demonstrating potential traceability.

You can perform joins using tools like Pandas (Python), SQL (after importing into a database), or Excel's Power Query:

* **Sales & Customers:** Join `sales.csv` and `customers.csv` on `CustomerID`.
* **Sales & Inventory:** Join `sales.csv` and `inventory.csv` on `ProductID`.
* **Purchases & Suppliers:** Join `purchases.csv` and `suppliers.csv` on `SupplierID`.
* **Purchases & Inventory:** Join `purchases.csv` and `inventory.csv` on `ProductID`.
* **Ledger & Sales/Purchases:** Join `ledger.csv` with `sales.csv` on `ledger.ReferenceID = sales.SaleID` or with `purchases.csv` on `ledger.ReferenceID = purchases.PurchaseID`.

## Configuration

All configurable parameters are located in `data_generator/config.py`. You can modify these values to change the behavior of the data generation process:

* `NUM_ROWS_TO_GENERATE`: The default number of rows for each CSV file (default: `10000`).
* `OUTPUT_DIR`: The directory where CSV files will be saved (default: `'data'`).
* `INITIAL_LEDGER_BALANCE`: Starting balance for the ledger (default: `1000000.0`).
* `*_BASENAME` and `*_FILE` variables: Base filenames and their full paths.

**Example Modification:**
To generate 50,000 rows instead of 10,000, simply change `NUM_ROWS_TO_GENERATE` in `config.py`:
```python
# data_generator/config.py
NUM_ROWS_TO_GENERATE = 50000