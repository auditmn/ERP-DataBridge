const { Storage } = require('@google-cloud/storage');
const chokidar = require('chokidar');
const path = require('path');
const fs = require('fs');

// Load environment variables from .env file
require('dotenv').config();

// --- Configuration ---
// The local folder to watch for new files.
const WATCH_FOLDER = process.env.WATCH_FOLDER || './uploads';
// The name of the GCS bucket to upload files to.
const GCS_BUCKET_NAME = process.env.GCS_BUCKET_NAME;
// The path to your service account key file.
// Set this in your .env file via GOOGLE_APPLICATION_CREDENTIALS.
const GCS_KEYFILE = process.env.GOOGLE_APPLICATION_CREDENTIALS;

// --- Validation ---
if (!GCS_BUCKET_NAME) {
    console.error('Error: GCS_BUCKET_NAME environment variable not set.');
    process.exit(1);
}

if (!GCS_KEYFILE || !fs.existsSync(GCS_KEYFILE)) {
    console.error(`Error: Service account key file not found at path specified by GOOGLE_APPLICATION_CREDENTIALS.`);
    console.error(`Current path: ${GCS_KEYFILE}`);
    process.exit(1);
}

// Create the watch folder if it doesn't exist
if (!fs.existsSync(WATCH_FOLDER)) {
    console.log(`Creating watch folder: ${WATCH_FOLDER}`);
    fs.mkdirSync(WATCH_FOLDER, { recursive: true });
}

// --- GCS and File Watcher Initialization ---

// Creates a client from a service account key file.
const storage = new Storage({
    keyFilename: GCS_KEYFILE,
});

const bucket = storage.bucket(GCS_BUCKET_NAME);

/**
 * Uploads a file to Google Cloud Storage.
 * @param {string} filePath The full path to the local file.
 */
async function uploadFile(filePath) {
    const fileName = path.basename(filePath);
    console.log(`Attempting to upload ${fileName}...`);

    try {
        await bucket.upload(filePath, {
            destination: fileName,
        });
        console.log(`✅ Successfully uploaded ${fileName} to ${GCS_BUCKET_NAME}.`);
    } catch (error) {
        console.error(`❌ Failed to upload ${fileName}:`, error);
    }
}

// Initialize watcher.
const watcher = chokidar.watch(WATCH_FOLDER, {
    ignored: /(^|[\/\\])\../, // ignore dotfiles
    persistent: true,
    ignoreInitial: true, // Don't upload files that are already there on startup
});

// --- Event Listeners ---
console.log('Starting file watcher...');

watcher
    .on('add', filePath => {
        console.log(`[+] File added: ${path.basename(filePath)}`);
        uploadFile(filePath).catch(console.error);
    })
    .on('ready', () => console.log(`🚀 Watcher is ready. Watching for new files in ${path.resolve(WATCH_FOLDER)}.`))
    .on('error', error => console.error(`Watcher error: ${error}`));

console.log(`Listening for file additions in '${WATCH_FOLDER}'. Press Ctrl+C to exit.`);