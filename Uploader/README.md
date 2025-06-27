# GCS Folder Watcher and Uploader

This Node.js application watches a specified local folder. When a new file is added to this folder, the script automatically uploads it to a designated Google Cloud Storage (GCS) bucket.

It uses `chokidar` for efficient file system watching and `@google-cloud/storage` for interacting with the GCS API.

## Prerequisites

1.  **Node.js**: Make sure you have Node.js (v14 or newer) and npm installed.
2.  **Google Cloud Platform (GCP) Account**: You need a GCP account and a project.
3.  **GCS Bucket**: Create a GCS bucket where the files will be uploaded.
4.  **Service Account**:
    *   In your GCP project, create a service account.
    *   Grant this service account the **"Storage Object Creator"** or **"Storage Object Admin"** role on your bucket.
    *   Create a JSON key for this service account and download it to your computer.

## Setup

1.  **Create a project folder and copy the files** into it.

2.  **Install dependencies:**
    Open your terminal in the project folder and run:
    ```bash
    npm install
    ```

3.  **Configure Environment Variables:**

    Create a `.env` file in the root of the project. You can do this by copying the example file:

    ```bash
    cp .env.example .env
    ```

    Now, edit the `.env` file with your specific configuration:

    ```env
    # The name of your Google Cloud Storage bucket
    GCS_BUCKET_NAME="your-gcs-bucket-name"

    # The relative path to your downloaded GCP service account JSON key file
    # IMPORTANT: Make sure this file is not committed to version control.
    GOOGLE_APPLICATION_CREDENTIALS="./path/to/your-gcp-key.json"

    # (Optional) The local folder to watch. Defaults to './uploads' if not set.
    WATCH_FOLDER="./uploads"
    ```

    **Security Note:** The `.gitignore` file is already configured to ignore `.env` and `*.json` files. Never commit your service account keys or other secrets to a public repository.

## Running the Application

1.  **Start the watcher:**

    ```bash
    npm start
    ```

    The script will initialize and print a message indicating that it's watching the target folder.

    ```
    Creating watch folder: ./uploads
    Starting file watcher...
    🚀 Watcher is ready. Watching for new files in /full/path/to/project/uploads.
    Listening for file additions in './uploads'. Press Ctrl+C to exit.
    ```

2.  **Test the upload:**

    Add a file to the `uploads` folder (or the folder you specified in `WATCH_FOLDER`). You can do this by dragging and dropping a file or using the command line:

    ```bash
    echo "hello world" > uploads/test.txt
    ```

    You should see output in the console indicating the file was detected and successfully uploaded.

3.  **Verify in GCS:**

    Go to the Google Cloud Console, navigate to your GCS bucket, and you should see the `test.txt` file there.