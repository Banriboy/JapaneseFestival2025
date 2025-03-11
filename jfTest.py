import streamlit as st
import time

st.title("リアルタイム重量モニター")

# **セッション変数でデータを保持**
if "data" not in st.session_state:
    st.session_state.data = {
        "weight": 0.0,
        "category": "N/A",
        "co2_emission": 0.0,
        "item_count": 0
    }

# **表示用のエリアを作成**
weight_display = st.empty()

# **データ更新関数**
def update_data(weight, category, co2_emission=0, item_count=0):
    st.session_state.data = {
        "weight": weight,
        "category": category,
        "co2_emission": co2_emission,
        "item_count": item_count
    }

# **データ表示**
while True:
    weight_display.write(f"**現在の重量:** {st.session_state.data['weight']:.3f} kg")
    weight_display.write(f"**カテゴリ:** {st.session_state.data['category']}")
    if st.session_state.data["category"] == "Chopsticks":
        weight_display.write(f"**CO2排出量:** {st.session_state.data['co2_emission']:.1f} g")
        weight_display.write(f"**推定アイテム数:** {st.session_state.data['item_count']} 本")
    
    time.sleep(3)
    st.experimental_rerun()  # これを使うには最新バージョンが必要

