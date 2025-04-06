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
chopsticks_totals = {"co2": 0.0, "item_count": 0}

if not data:
    st.write("データがありません。")
else:
    for record in data:
        category = record.get("Category", "").strip().lower()
        weight = record.get("Weight", 0)

        try:
            weight = float(weight)
            category_totals[category] += weight
        except ValueError:
            st.warning(f"無効な重量データ: {weight}")

        if category == "chopsticks":
            co2 = record.get("CO2 Emission", 0)
            item_count = record.get("Item Count", 0)
            try:
                chopsticks_totals["co2"] += float(co2)
                chopsticks_totals["item_count"] += int(item_count)
            except ValueError:
                st.warning(f"無効なCO2排出量またはアイテム数: CO2={co2}, Items={item_count}")

total_weight = category_totals.get("recycle", 0) + category_totals.get("chopsticks", 0)

# タイトル
st.title("🌎 Our Recycling Efforts Results")

# カラムで2列に分けてカード風表示
col1, col2 = st.columns(2)

with col1:
import time

if "chopsticks" in category_totals:
    # アニメーション用の空要素
    chopsticks_placeholder = st.empty()

    target_weight = category_totals['chopsticks']
    target_items = chopsticks_totals['item_count']
    target_co2 = chopsticks_totals['co2']

    # アニメーションのステップ数
    steps = 30
    for i in range(1, steps + 1):
        weight = target_weight * i / steps
        items = int(target_items * i / steps)
        co2 = target_co2 * i / steps

        chopsticks_placeholder.markdown(f"""
        <div style='
            border-radius: 15px;
            padding: 25px;
            background-color: #fef6e4;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
            text-align: center;
        '>
            <h3 style='color: #e67e22;'>Chopsticks</h3>
            <h1 style='font-size: 48px;'>{weight:.2f} kg</h1>
            <p>{items} pairs of chopsticks</p>
            <p style='color: gray;'>{co2:.2f} kg CO2 reduced</p>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(0.03)  # スピード調整（数字が速く/遅く増える）

with col2:
    if "recycle" in category_totals:
        st.markdown(f"""
        <div style='
            border-radius: 15px;
            padding: 25px;
            background-color: #eafbea;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
            text-align: center;
        '>
            <h3 style='color: #27ae60;'>Recyclables</h3>
            <h1 style='font-size: 48px;'>{category_totals['recycle']:.2f} kg</h1>
        </div>
        """, unsafe_allow_html=True)

# 全体の合計
st.markdown(f"""
<div style='
    margin-top: 40px;
    padding: 20px;
    background-color: #f0f0f0;
    border-radius: 12px;
    text-align: center;
'>
    <p style='font-size: 22px;'>
        👏 <strong>Visitors have collectively contributed to reducing <span style='color:#2c3e50;'>{total_weight:.2f} kg</span> of waste through recycling efforts!</strong>
    </p>
</div>
""", unsafe_allow_html=True)

st.write("Thank you for your cooperation!")

