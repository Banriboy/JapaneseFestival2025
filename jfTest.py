import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

# GitHub Secretsから認証情報を取得
google_creds = os.getenv("GOOGLE_CREDENTIALS")

if google_creds is None:
    st.error("Google認証情報が設定されていません。GitHub Secretsを確認してください。")
else:
    creds_dict = json.loads(google_creds)

    # 一時ファイルとしてcredentials.jsonを作成
    with open("credentials.json", "w") as f:
        json.dump(creds_dict, f)

    # Google Sheets API認証
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    # Google Sheetsにアクセス
    sheet = client.open("Japanese Festival 2025").sheet1

    # データを読み込んでStreamlitに表示
    data = sheet.get_all_records()

    st.title("リアルタイム重量モニター")
    for record in data:
        st.write(f"**重量:** {record['weight']} kg")
        st.write(f"**カテゴリ:** {record['category']}")
        st.write(f"**CO2排出量:** {record['co2_emission']} g")
        st.write(f"**推定アイテム数:** {record['item_count']} 本")
        st.write("---")
