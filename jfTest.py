import streamlit as st
import time

st.title("リアルタイム重量モニター")

# セッション変数でデータを保持
if "data" not in st.session_state:
    st.session_state.data = {
        "weight": 0.0,
        "category": "N/A",
        "co2_emission": 0.0,
        "item_count": 0
    }

# **✅ Webhook API (Raspberry Pi からデータを受信)**
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/update', methods=['POST'])
def update_weight():
    """Raspberry Pi からのデータを受け取る"""
    data = request.json
    if data:
        st.session_state.data = data
        return jsonify({"message": "Data updated successfully"}), 200
    return jsonify({"error": "Invalid data"}), 400

# Flask をバックグラウンド実行
import threading
threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000, debug=False), daemon=True).start()

# **💡 データ表示エリア**
weight_placeholder = st.empty()
category_placeholder = st.empty()
co2_placeholder = st.empty()
item_count_placeholder = st.empty()

while True:
    data = st.session_state.data
    weight_placeholder.write(f"**現在の重量:** {data['weight']:.3f} kg")
    category_placeholder.write(f"**カテゴリ:** {data['category']}")
    
    if data["category"] == "Chopsticks":
        co2_placeholder.write(f"**CO2排出量:** {data['co2_emission']:.1f} g")
        item_count_placeholder.write(f"**推定アイテム数:** {data['item_count']} 本")

    time.sleep(1)  # 1秒ごとに更新
