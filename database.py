import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st

def get_google_sheet():
    """Connect to Google Sheets"""
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
        client = gspread.authorize(creds)
        sheet = client.open("HabitMatrix_Responses").sheet1
        return sheet
    except:
        return None

def save_to_sheet(responses):
    """Save response to Google Sheets"""
    sheet = get_google_sheet()
    if sheet:
        row = [responses.get(key, '') for key in responses.keys()]
        sheet.append_row(row)
        return True
    return False

def load_from_sheet():
    """Load all responses from Google Sheets"""
    sheet = get_google_sheet()
    if sheet:
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    return pd.DataFrame()
