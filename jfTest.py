import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import defaultdict

# --- グラデーション背景とカードCSS追加 ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #ffe4e1, #add8e6);
    }
    .card {
        padding: 20px;
        margin: 10px 0;
        border-radius: 15px;
        background-color: rgba(255, 255, 255, 0.8);
        color: #333;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        text-align: center;
        backdrop-filter: blur(10px);
    }
    .card h2 {
        font-size: 36px;
        margin-bottom: 10px;
    }
    .card h3 {
        font-size: 32px;
        margin: 5px 0;
    }
    .card p {
        font-size: 20px;
        margin: 5px 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- Streamlit Secrets から認証情報を取得 ---
if "gcp_service_account" not in st.secrets:
    st.error("Google認証情報が設定されていません。Streamlit Secretsを確認してください。")
    st.stop()

creds_dict = st.secrets["gcp_service_account"]

# --- Google Sheets API認証 ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# --- Google Sheetsにアクセス ---
spreadsheet_name = "Japanese Festival 2025"
try:
    sheet = client.open(spreadsheet_name).sheet1
except gspread.exceptions.SpreadsheetNotFound:
    st.error(f"スプレッドシート '{spreadsheet_name}' が見つかりません。アクセス権を確認してください。")
    st.stop()

# --- データを取得 ---
data = sheet.get_all_records()
category_totals = defaultdict(float)
chopsticks_totals = {"co2": 0.0, "chopsticks_count": 0}

if not data:
    st.write("データがありません。")
else:
    for record in data:
        category = record.get("Category", "").strip().lower()
        weight = record.get("Weight (kg)", 0)

        try:
            weight = float(weight)
            category_totals[category] += weight
        except ValueError:
            st.warning(f"無効な重量データ: {weight}")

        if category == "chopsticks":
            co2 = record.get("CO2 Emission (kg)", 0)
            item_count = record.get("Chopsticks Count (pair)", 0)

            try:
                chopsticks_totals["co2"] += float(co2)
                chopsticks_totals["chopsticks_count"] += int(item_count)
            except ValueError:
                st.warning(f"無効なCO2排出量またはアイテム数: CO2={co2}, Chopsticks={item_count}")

total_weight = category_totals.get("recycle", 0) + category_totals.get("chopsticks", 0)

# --- タイトル ---
st.markdown("<h1 style='text-align: center; color: #444;'>🌸 Our Recycling Efforts Results 💙</h1>", unsafe_allow_html=True)

# --- カード表示 ---
col1, col2 = st.columns(2)

with col1:
    if "chopsticks" in category_totals:
        st.markdown(f"""
        <div class="card">
            <h2>Collected Chopsticks</h2>
            <h3>{category_totals['chopsticks']:.2f} kg</h3>
            <p>{chopsticks_totals['chopsticks_count']} chopsticks equivalent</p>
            <p>{chopsticks_totals['co2']:.2f} kg CO₂ reduced</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    if "recycle" in category_totals:
        st.markdown(f"""
        <div class="card">
            <h2>Collected Recyclables</h2>
            <h3>{category_totals['recycle']:.2f} kg</h3>
        </div>
        """, unsafe_allow_html=True)

# --- 合計表示 ---
st.markdown(f"""
<div style="margin-top: 30px; text-align: center;">
    <h2 style='font-size: 28px; color: #333;'>♻️ Total Waste Reduced: <strong>{total_weight:.2f} kg</strong></h2>
    <p style='font-size: 18px;'>Thank you for your cooperation! 🌟</p>
</div>
""", unsafe_allow_html=True)

