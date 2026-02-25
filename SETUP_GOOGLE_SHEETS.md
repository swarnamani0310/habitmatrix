# Connect Google Sheets - Quick Setup

## Step 1: Create Google Sheet
1. Go to https://sheets.google.com
2. Create new sheet named: **HabitMatrix_Responses**
3. Add these headers in Row 1:
   ```
   Name | Age | Email | College | Year | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 | Q11 | Q12 | Comments | timestamp
   ```

## Step 2: Enable Google Sheets API
1. Go to https://console.cloud.google.com
2. Create new project: "HabitMatrix"
3. Search "Google Sheets API" → Enable
4. Search "Google Drive API" → Enable

## Step 3: Create Service Account
1. Go to "IAM & Admin" → "Service Accounts"
2. Click "Create Service Account"
3. Name: "habitmatrix-bot"
4. Click "Create and Continue" → "Done"

## Step 4: Get JSON Key
1. Click on your service account
2. Go to "Keys" tab
3. "Add Key" → "Create new key" → "JSON"
4. Download the JSON file

## Step 5: Share Sheet
1. Open the JSON file
2. Copy the `client_email` (looks like: xxx@xxx.iam.gserviceaccount.com)
3. Open your Google Sheet
4. Click "Share"
5. Paste the email → Give "Editor" access → Send

## Step 6: Add to Streamlit Cloud
1. Go to your Streamlit app
2. Click "Settings" (⚙️) → "Secrets"
3. Paste this (replace with your JSON values):

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR-PRIVATE-KEY-HERE\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"
```

4. Click "Save"
5. App will restart automatically

## Done! 🎉
All responses will now save to Google Sheets permanently!

## Test It
1. Submit a test response in your app
2. Check your Google Sheet
3. Data should appear instantly
