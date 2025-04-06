import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import defaultdict

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

# データを読み込んでカテゴリごとの重量を計算
data = sheet.get_all_records()

# カテゴリーごとの総重量
category_totals = defaultdict(float)

# chopsticks の CO2 排出量とアイテム数も合計
chopsticks_totals = {"co2": 0.0, "chopsticks_count": 0}

if not data:
    st.write("データがありません。")
else:
    for record in data:
        category = record.get("Category", "").strip().lower()  # 小文字に変換して統一
        weight = record.get("Weight (kg)", 0)

        # データの型変換
        try:
            weight = float(weight)
            category_totals[category] += weight
        except ValueError:
            st.warning(f"無効な重量データ: {weight}")

        # chopsticks の場合、CO2排出量とアイテム数も合計
        if category == "chopsticks":
            co2 = record.get("CO2 Emission (kg)", 0)
            item_count = record.get("Chopsticks Count (pair)", 0)

            try:
                chopsticks_totals["co2"] += float(co2)
                chopsticks_totals["chopsticks_count"] += int(item_count)
            except ValueError:
                st.warning(f"無効なCO2排出量またはアイテム数: CO2={co2}, Chopsticks={item_count}")

total_weight = category_totals.get("recycle", 0) + category_totals.get("chopsticks", 0)

# Streamlitでカテゴリごとの情報を左右に分けて表示
st.title("Our Recycling Efforts Results")

col1, col2 = st.columns(2)  # 左右のカラムを作成

with col1:  # 左側 (Chopsticks)
    if "chopsticks" in category_totals:
        st.header("Collected Chopsticks")
        st.markdown(f"<h2 style='color: #FF5733; font-size: 48px;'>{category_totals['chopsticks']:.2f} kg</h2>", unsafe_allow_html=True)
        st.write(f"{chopsticks_totals['chopsticks_count']} chopsticks equivalent")
        st.markdown(f"<h3 style='color: #FF5733;'>CO2 Emission: {chopsticks_totals['co2']:.2f} kg</h3>", unsafe_allow_html=True)

with col2:  # 右側 (Recycle)
    if "recycle" in category_totals:
        st.header("Collected Recyclable Wastes")
        st.markdown(f"<h2 style='color: #4CAF50; font-size: 48px;'>{category_totals['recycle']:.2f} kg</h2>", unsafe_allow_html=True)

st.write(f"Thank you for your cooperation!")
st.write(f"Visitors have collectively contributed to reducing {total_weight:.2f} kg of waste through recycling efforts so far.")

# オシャレに感謝メッセージを表示
st.markdown("<h2 style='text-align: center; color: #2E7D32;'>Keep up the great work!</h2>", unsafe_allow_html=True)

