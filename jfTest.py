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
chopsticks_totals = {"co2": 0.0, "item_count": 0}

if not data:
    st.write("データがありません。")
else:
    for record in data:
        category = record.get("Category", "").strip().lower()  # 小文字に変換して統一
        weight = record.get("Weight", 0)

        # データの型変換
        try:
            weight = float(weight)
            category_totals[category] += weight
        except ValueError:
            st.warning(f"無効な重量データ: {weight}")

        # chopsticks の場合、CO2排出量とアイテム数も合計
        if category == "chopsticks":
            co2 = record.get("CO2 Emission", 0)
            item_count = record.get("Item Count", 0)

            try:
                chopsticks_totals["co2"] += float(co2)
                chopsticks_totals["item_count"] += int(item_count)
            except ValueError:
                st.warning(f"無効なCO2排出量またはアイテム数: CO2={co2}, Items={item_count}")

# Streamlitでカテゴリごとの情報を左右に分けて表示
st.title("Our Recycling Efforts Results")

col1, col2 = st.columns(2)  # 左右のカラムを作成

with col1:  # 左側 (Chopsticks)
    if "chopsticks" in category_totals:
        st.header("Collected Chopsticks")
        st.write(f"{category_totals['chopsticks']:.3f} kg ({chopsticks_totals['item_count']} chopsticks equivalent)")
        st.write(f"**CO2排出量:** {chopsticks_totals['co2']:.3f} g")
        st.write(f"**推定アイテム数:** {chopsticks_totals['item_count']} 本")

with col2:  # 右側 (Recycle)
    if "recycle" in category_totals:
        st.header("Recycle")
        st.write(f"**総重量:** {category_totals['recycle']:.3f} kg")

