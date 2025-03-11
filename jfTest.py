import streamlit as st
import time
import json

st.title("リアルタイム重量モニター")

# **セッション変数でデータを保持**
if "data" not in st.session_state:
    st.session_state.data = {
        "weight": 0.0,
        "category": "N/A",
        "co2_emission": 0.0,
        "item_count": 0
    }

# **✅ データ更新用の関数**
def update_data(weight, category, co2_emission=0, item_count=0):
    st.session_state.data = {
        "weight": weight,
        "category": category,
        "co2_emission": co2_emission,
        "item_count": item_count
    }

# **✅ Raspberry Piからのデータ受信シミュレーション**
def simulate_data_receiving():
    # ここでRaspberry Piからのデータを受信する想定
    # 実際にはAPIを使って受け取る部分が必要
    # サンプルデータ
    input_data = '{"weight": 1.23, "category": "Chopsticks", "co2_emission": 5.0, "item_count": 10}'
    
    try:
        new_data = json.loads(input_data)
        update_data(**new_data)
        st.success("データ更新完了！")
    except Exception as e:
        st.error(f"エラー: {e}")

# **📩 データ更新をシミュレーション**
with st.expander("📩 データ受信 API（開発用）"):
    if st.button("データ更新"):
        simulate_data_receiving()

# **💡 データ表示エリア**
st.write(f"**現在の重量:** {st.session_state.data['weight']:.3f} kg")
st.write(f"**カテゴリ:** {st.session_state.data['category']}")
if st.session_state.data["category"] == "Chopsticks":
    st.write(f"**CO2排出量:** {st.session_state.data['co2_emission']:.1f} g")
    st.write(f"**推定アイテム数:** {st.session_state.data['item_count']} 本")

# **✅ データ更新を自動化**
time.sleep(3)  # 3秒ごとに更新
st.stop()  # アプリを停止して再実行を促す


