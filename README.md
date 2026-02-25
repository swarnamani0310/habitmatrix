# Behavioral Pattern Mapping System

A data-driven lifestyle and productivity self-assessment platform using ML clustering.

## Setup

### Local Development
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

### Streamlit Cloud Deployment
1. Follow `GOOGLE_SHEETS_SETUP.md` to setup permanent data storage
2. Push code to GitHub
3. Connect repo to Streamlit Cloud
4. Add Google Sheets credentials to Streamlit secrets

## Features

- **12-question behavioral assessment**
- **ML-based clustering** (KMeans with preprocessing)
- **10 Tamil movie character profiles** with personalized insights
- **Admin dashboard** with analytics & visualizations
- **Permanent data storage** (Google Sheets integration)
- **Animated UI** with memes and videos

## Usage

### User Assessment
1. Navigate to "Assessment" page
2. Answer all 12 questions
3. Submit to receive your behavioral profile

### Admin Dashboard
1. Navigate to "Admin Dashboard"
2. Enter password: `admin123`
3. View analytics, clusters, and correlations

## Data Privacy

- Responses stored securely in Google Sheets
- Only admin can access aggregated data
- Individual responses remain confidential

## Tech Stack

- **Frontend**: Streamlit
- **ML**: scikit-learn (KMeans, StandardScaler)
- **Data**: pandas, numpy, Google Sheets API
- **Visualization**: plotly
