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

# **✅ Webhook API なし！Streamlit のセッションを更新**
def update_data(weight, category, co2_emission=0, item_count=0):
    st.session_state.data = {
        "weight": weight,
        "category": category,
        "co2_emission": co2_emission,
        "item_count": item_count
    }

# **📌 フェイクAPI（Streamlit 内で受信シミュレーション）**
import json

with st.expander("📩 データ受信 API（開発用）"):
    input_data = st.text_area("JSON データを入力", '{"weight": 1.23, "category": "Chopsticks", "co2_emission": 5.0, "item_count": 10}')
    if st.button("データ更新"):
        try:
            new_data = json.loads(input_data)
            update_data(**new_data)
            st.success("データ更新完了！")
        except Exception as e:
            st.error(f"エラー: {e}")

# **💡 データ表示エリア**
st.write(f"**現在の重量:** {st.session_state.data['weight']:.3f} kg")
st.write(f"**カテゴリ:** {st.session_state.data['category']}")
if st.session_state.data["category"] == "Chopsticks":
    st.write(f"**CO2排出量:** {st.session_state.data['co2_emission']:.1f} g")
    st.write(f"**推定アイテム数:** {st.session_state.data['item_count']} 本")

# **✅ 自動更新**
while True:
    time.sleep(1)
    st.experimental_rerun()
