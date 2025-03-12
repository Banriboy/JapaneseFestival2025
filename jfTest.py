import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Streamlit Secrets から認証情報を取得
if "gcp_service_account" not in st.secrets:
    st.error("Google認証情報が設定されていません。Streamlit Secretsを確認してください。")
    st.stop()

creds_dict = st.secrets["gcp_service_account"]

# Google Sheets API認証
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Google Sheetsにアクセス
spreadsheet_name = "Japanese Festival 2025"
try:
    sheet = client.open(spreadsheet_name).sheet1
except gspread.exceptions.SpreadsheetNotFound:
    st.error(f"スプレッドシート '{spreadsheet_name}' が見つかりません。アクセス権を確認してください。")
    st.stop()

# データを読み込んでStreamlitに表示
data = sheet.get_all_records()

st.title("リアルタイム重量モニター")

if not data:
    st.write("データがありません。")
else:
    for record in data:
        st.write(f"**重量:** {record.get('Weight', 'N/A')} kg")
        st.write(f"**カテゴリ:** {record.get('Category', 'N/A')}")
        st.write(f"**CO2排出量:** {record.get('CO2 Emission', 'N/A')} g")
        st.write(f"**推定アイテム数:** {record.get('Item Count', 'N/A')} 本")
        st.write("---")

