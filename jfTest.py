import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import defaultdict

# ---------------------- 🌸 CSS & 桜エフェクト ----------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #ffe4e1, #add8e6);
    background-attachment: fixed;
    background-size: cover;
}

.transparent-card {
    background-color: rgba(255, 255, 255, 0.5);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 30px;
    margin: 20px 0;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    text-align: center;
    transition: transform 0.3s ease;
}

.transparent-card:hover {
    transform: scale(1.02);
}

.transparent-card h2 {
    font-size: 32px;
    margin-bottom: 10px;
    color: #333;
}

.transparent-card h3 {
    font-size: 28px;
    margin: 5px 0;
}

.transparent-card p {
    font-size: 18px;
    margin: 5px 0;
}

.sakura {
    position: fixed;
    top: -10px;
    z-index: 9999;
    pointer-events: none;
    width: 15px;
    height: 15px;
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Cherry_blossom_icon.svg/1024px-Cherry_blossom_icon.svg.png');
    background-size: contain;
    background-repeat: no-repeat;
    animation: fall linear infinite;
    opacity: 0.7;
}

@keyframes fall {
    0% {
        transform: translateY(0) rotate(0deg);
        opacity: 1;
    }
    100% {
        transform: translateY(100vh) rotate(360deg);
        opacity: 0;
    }
}
</style>

<script>
const NUM_SAKURA = 20;
for (let i = 0; i < NUM_SAKURA; i++) {
    const sakura = document.createElement("div");
    sakura.classList.add("sakura");
    sakura.style.left = Math.random() * 100 + "vw";
    sakura.style.animationDuration = (5 + Math.random() * 5) + "s";
    sakura.style.animationDelay = (Math.random() * 5) + "s";
    document.body.appendChild(sakura);
}
</script>
""", unsafe_allow_html=True)

# ---------------------- 🌱 データ処理 ----------------------
if "gcp_service_account" not in st.secrets:
    st.error("Google認証情報が設定されていません。")
    st.stop()

creds_dict = st.secrets["gcp_service_account"]
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

spreadsheet_name = "Japanese Festival 2025"
try:
    sheet = client.open(spreadsheet_name).sheet1
except gspread.exceptions.SpreadsheetNotFound:
    st.error(f"スプレッドシート '{spreadsheet_name}' が見つかりません。")
    st.stop()

data = sheet.get_all_records()
category_totals = defaultdict(float)
chopsticks_totals = {"co2": 0.0, "chopsticks_count": 0}

if not data:
    st.write("データがありません。")
else:
    for record in data:
        category = record.get("Category", "").strip().lower()
        weight = record.get("Weight (kg)", 0)

        try:
            weight = float(weight)
            category_totals[category] += weight
        except ValueError:
            st.warning(f"無効な重量データ: {weight}")

        if category == "chopsticks":
            co2 = record.get("CO2 Emission (kg)", 0)
            item_count = record.get("Chopsticks Count (pair)", 0)

            try:
                chopsticks_totals["co2"] += float(co2)
                chopsticks_totals["chopsticks_count"] += int(item_count)
            except ValueError:
                st.warning(f"無効なCO2排出量またはアイテム数: CO2={co2}, Chopsticks={item_count}")

total_weight = category_totals.get("recycle", 0) + category_totals.get("chopsticks", 0)

# ---------------------- 🌟 表示 ----------------------
st.markdown("<h1 style='text-align: center; color: #333;'>🌸 Our Recycling Efforts Results 💙</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if "chopsticks" in category_totals:
        st.markdown(f"""
        <div class="transparent-card">
            <h2>🥢 Chopsticks</h2>
            <h3>{category_totals['chopsticks']:.2f} kg</h3>
            <p>{chopsticks_totals['chopsticks_count']} chopsticks</p>
            <p>{chopsticks_totals['co2']:.2f} kg CO₂ reduced</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    if "recycle" in category_totals:
        st.markdown(f"""
        <div class="transparent-card">
            <h2>♻️ Recyclables</h2>
            <h3>{category_totals['recycle']:.2f} kg</h3>
        </div>
        """, unsafe_allow_html=True)

st.markdown(f"""
<div class="transparent-card">
    <h2>🌍 Total Waste Reduced</h2>
    <h3>{total_weight:.2f} kg</h3>
    <p>Thank you for your cooperation! 💖</p>
</div>
""", unsafe_allow_html=True)

