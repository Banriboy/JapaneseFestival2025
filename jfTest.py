import streamlit as st
import time
import json

st.title("リアルタイム重量モニター")

# セッション変数でデータを保持
if "data" not in st.session_state:
    st.session_state.data = {
        "weight": 0.0,
        "category": "N/A",
        "co2_emission": 0.0,
        "item_count": 0
    }

# ✅ データ更新用の関数
def update_data(weight, category, co2_emission=0, item_count=0):
    st.session_state.data = {
        "weight": weight,
        "category": category,
        "co2_emission": co2_emission,
        "item_count": item_count
    }

# APIエンドポイントの受信
import requests

# リアルタイムにデータを更新するためのエンドポイント
@app.route("/update", methods=["POST"])
def update():
    try:
        data = request.json
        weight = data["weight"]
        category = data["category"]
        co2_emission = data.get("co2_emission", 0)
        item_count = data.get("item_count", 0)
        
        update_data(weight, category, co2_emission, item_count)
        return {"status": "success", "message": "Data updated"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# **💡 データ表示エリア**
st.write(f"**現在の重量:** {st.session_state.data['weight']:.3f} kg")
st.write(f"**カテゴリ:** {st.session_state.data['category']}")
if st.session_state.data["category"] == "Chopsticks":
    st.write(f"**CO2排出量:** {st.session_state.data['co2_emission']:.1f} g")
    st.write(f"**推定アイテム数:** {st.session_state.data['item_count']} 本")

# **✅ データ更新を自動化**
time.sleep(3)  # 3秒ごとに更新
st.stop()  # アプリを停止して再実行を促す

