# Google Sheets Setup for Permanent Data Storage

## Why Google Sheets?
Streamlit Cloud resets files on every restart. Google Sheets provides FREE permanent storage.

## Setup Steps:

### 1. Create Google Sheet
1. Go to https://sheets.google.com
2. Create a new sheet named: **HabitMatrix_Responses**
3. Add headers in first row: `Name`, `Age`, `Email`, `College`, `Year`, `Q1`, `Q2`, `Q3`, `Q4`, `Q5`, `Q6`, `Q7`, `Q8`, `Q9`, `Q10`, `Q11`, `Q12`, `Comments`, `timestamp`

### 2. Create Google Cloud Project
1. Go to https://console.cloud.google.com
2. Create a new project (e.g., "HabitMatrix")
3. Enable **Google Sheets API** and **Google Drive API**

### 3. Create Service Account
1. Go to "IAM & Admin" → "Service Accounts"
2. Click "Create Service Account"
3. Name it (e.g., "habitmatrix-bot")
4. Click "Create and Continue"
5. Skip optional steps, click "Done"

### 4. Generate JSON Key
1. Click on the service account you created
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose "JSON" format
5. Download the JSON file

### 5. Share Sheet with Service Account
1. Open the JSON file
2. Copy the `client_email` value (looks like: xxx@xxx.iam.gserviceaccount.com)
3. Open your Google Sheet
4. Click "Share" button
5. Paste the email and give "Editor" access

### 6. Add Secrets to Streamlit Cloud
1. Go to your Streamlit Cloud app
2. Click "Settings" → "Secrets"
3. Add this (replace with your JSON content):

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR-PRIVATE-KEY\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"
```

### 7. For Local Testing
Create `.streamlit/secrets.toml` in your project:
```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
# ... (same as above)
```

## Done! 🎉
Your data will now be stored permanently in Google Sheets and never deleted!
