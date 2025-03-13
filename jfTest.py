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

# 取得データを確認
st.write("取得したデータ:", data)

category_totals = defaultdict(float)  # カテゴリーごとの総重量
chopsticks_totals = {"co2": 0, "item_count": 0}  # chopsticks専用データ

if not data:
    st.write("データがありません。")
else:
    for record in data:
        category = record.get("Category", "不明")  # カテゴリーを取得
        weight = record.get("Weight", 0)  # 重量を取得

        # デバッグ用に各レコードのデータを表示
        st.write(f"処理中のデータ: {record}")

        # 重量データの処理
        try:
            weight = float(weight)
            category_totals[category] += weight
        except ValueError:
            st.warning(f"無効な重量データ: {weight}")

        # chopsticks の場合、CO2排出量とアイテム数も計算
        if category == "chopsticks":
            co2 = record.get("CO2 Emission", 0)
            item_count = record.get("Item Count", 0)

            try:
                co2 = float(co2)
                item_count = int(item_count)
                chopsticks_totals["co2"] += co2
                chopsticks_totals["item_count"] += item_count
            except ValueError:
                st.warning(f"無効なCO2排出量またはアイテム数: CO2={co2}, Items={item_count}")

# Streamlitでカテゴリごとの情報を表示
st.title("リアルタイム重量モニター")

for category, total_weight in category_totals.items():
    st.write(f"**カテゴリ:** {category}")
    st.write(f"**総重量:** {total_weight:.2f} kg")

    # chopsticks の場合はCO2とアイテム数も表示
    if category == "chopsticks":
        st.write(f"**CO2排出量:** {chopsticks_totals['co2']:.2f} g")
        st.write(f"**推定アイテム数:** {chopsticks_totals['item_count']} 本")

    st.write("---")

