import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import defaultdict

# --- カードのCSSスタイル追加 ---
st.markdown("""
    <style>
    .card {
        padding: 20px;
        margin: 10px 0;
        border-radius: 15px;
        background-color: #FF5733;
        color: white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        text-align: center;
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
        font-size: 22px;
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
st.title("🌍 Our Recycling Efforts Results")

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
        <div class="card" style="background-color: #4CAF50;">
            <h2>Collected Recyclables</h2>
            <h3>{category_totals['recycle']:.2f} kg</h3>
        </div>
        """, unsafe_allow_html=True)

# --- 合計 ---
st.write("♻️ Visitors have collectively contributed to reducing:")
st.markdown(f"<h2 style='font-size: 32px; color: #2E8B57;'>{total_weight:.2f} kg of waste</h2>", unsafe_allow_html=True)
st.write("Thank you for your cooperation! 🙌")
