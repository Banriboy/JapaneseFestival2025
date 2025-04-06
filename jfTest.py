import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import defaultdict
import time

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

# 数字のパタパタエフェクトを追加
st.title("Our Recycling Efforts Results")

col1, col2 = st.columns(2)  # 左右のカラムを作成

# 左側 (Chopsticks)
with col1:
    if "chopsticks" in category_totals:
        st.markdown("""
        <div style='padding: 20px; border-radius: 10px; background-color: #FF5733; color: white;'>
            <h2 style='font-size: 40px; text-align: center;'>Collected Chopsticks</h2>
            <h3 style='font-size: 36px; text-align: center;' id='chopsticks-weight'></h3>
            <p style='font-size: 24px; text-align: center;'>{0} chopsticks equivalent</p>
            <h4 style='font-size: 24px; text-align: center;'>CO2 Emission: {1:.2f} kg</h4>
        </div>
        <script>
            let weight = {2};
            let element = document.getElementById('chopsticks-weight');
            let currentWeight = 0;
            let interval = setInterval(function() {{
                if (currentWeight < weight) {{
                    currentWeight += 0.1;  // スムーズに増加する速度
                    element.innerHTML = currentWeight.toFixed(2) + ' kg';
                }} else {{
                    clearInterval(interval);
                }}
            }}, 30);
        </script>
        """.format(category_totals['chopsticks'], chopsticks_totals['co2'], category_totals['chopsticks']), unsafe_allow_html=True)

# 右側 (Recycle)
with col2:
    if "recycle" in category_totals:
        st.markdown("""
        <div style='padding: 20px; border-radius: 10px; background-color: #4CAF50; color: white;'>
            <h2 style='font-size: 40px; text-align: center;'>Collected Recyclable Wastes</h2>
            <h3 style='font-size: 36px; text-align: center;' id='recycle-weight'></h3>
        </div>
        <script>
            let weight = {0};
            let element = document.getElementById('recycle-weight');
            let currentWeight = 0;
            let interval = setInterval(function() {{
                if (currentWeight < weight) {{
                    currentWeight += 0.1;
                    element.innerHTML = currentWeight.toFixed(2) + ' kg';
                }} else {{
                    clearInterval(interval);
                }}
            }}, 30);
        </script>
        """.format(category_totals['recycle']), unsafe_allow_html=True)

st.write(f"Thank you for your cooperation!")
st.write(f"Visitors have collectively contributed to reducing {total_weight:.2f} kg of waste through recycling efforts so far.")

# オシャレに感謝メッセージを表示
st.markdown("<h2 style='text-align: center; color: #2E7D32;'>Keep up the great work!</h2>", unsafe_allow_html=True)
