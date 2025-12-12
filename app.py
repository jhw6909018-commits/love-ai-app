import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 0. API 設定 ---
# ⚠️ 注意：這是你的 API Key，請小心保管
GOOGLE_API_KEY = "AIzaSyAOVCNW74yDY3MVRcyPfimFKr1Q4nnwXfI" 

# 設定 Generative AI
genai.configure(api_key=GOOGLE_API_KEY)

# --- 1. 系統設定 (已修正為 centered) ---
st.set_page_config(page_title="🚑 暈船急救站 | AI Love Auditor", page_icon="💔", layout="centered")

# CSS 美化設定 (黑紅配色 + VIP 區塊樣式)
st.markdown("""
<style>
    .stApp {background-color: #0e1117; color: #fff;}
    .report-box {background-color: #1f2937; padding: 20px; border-radius: 10px; border: 1px solid #374151; margin-top: 20px;}
    .vip-lock {border: 2px dashed #ffd700; padding: 20px; text-align: center; border-radius: 10px; background-color: #222; margin-top: 20px;}
    .stButton>button {width: 100%; font-weight: bold; border-radius: 8px; height: 50px;}
    /* 隱藏預設選單 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 2. 側邊欄設定 (VIP 解鎖功能) ---
with st.sidebar:
    st.title("⚙️ 設定台")
    st.markdown("---")
    st.header("🔐 VIP 通道")
    vip_input = st.text_input("輸入解鎖碼 (VIP Code)", placeholder="購買後獲得...")
    
    # *** 設定正確密碼 (對應 Gumroad 的發貨內容) ***
    VALID_CODE = "LOVE2026" 
    is_vip = (vip_input == VALID_CODE)
    
    if is_vip:
        st.success("✅ VIP 權限已啟動：全功能解鎖")
    else:
        st.info("🔒 目前為普通模式：僅顯示基礎分數")
        st.markdown("---")
        # 側邊欄的購買連結
        st.markdown("[👉 點此花 1 美金購買 VIP 解鎖碼](https://eclipsed84.gumroad.com/l/umuvow)")

# --- 3. 主程式邏輯 ---
st.title("🚑 暈船急救站")
st.caption("AI 幫你判斷：他是真的忙，還是你只是備胎？")

uploaded_file = st.file_uploader("上傳對話截圖 (LINE/IG/Messenger)", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="已上傳截圖", use_container_width=True)
    
    if st.button("💉 開始診斷 (AI Analysis)"):
        # 選擇模型
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        with st.spinner('AI 正在讀取空氣中的尷尬指數...'):
            try:
                # 構建 Prompt (提示詞)
                if is_vip:
                    # VIP 模式：完整分析
                    prompt = """
                    你是一位頂級戀愛心理學家。請分析這張對話截圖：
                    1. 【暈船指數】：直接給出 0-100 的數字 (Simp Score)，越高代表越卑微。
                    2. 【深度側寫】：分析對方的心理狀態、潛台詞是什麼？他/她對使用者有興趣嗎？
                    3. 【神回覆建議】：給出 3 個回覆選項 (A.高冷反殺 B.幽默化解 C.直球對決)，並解釋為什麼這樣回。
                    4. 語氣要求：專業但帶點幽默，像個很懂人性的朋友。
                    """
                else:
                    # 免費模式：吊胃口 (Sales Copy)
                    prompt = """
                    你是一位毒舌評論家。請分析這張對話截圖：
                    1. 【暈船指數】：直接給出 0-100 的數字。
                    2. 【一句話吐槽】：針對這個狀況給出一句犀利的點評。
                    3. 重要：最後必須加上這句話：「⚠️ 想知道對方潛台詞與神回覆建議？請輸入 VIP 碼解鎖完整報告。」
                    """

                response = model.generate_content([prompt, image])
                
                # --- 4. 顯示結果 ---
                st.markdown("---")
                st.subheader("📋 診斷報告")
                st.write(response.text)
                
                # 如果是免費版，顯示購買按鈕 (Call to Action)
                if not is_vip:
                    st.markdown("""
                    <div class="vip-lock">
                        <h3 style="color: #ffd700;">🔒 進階分析已鎖定</h3>
                        <p>想看「對方潛台詞分析」與「必勝神回覆」？</p>
                        <p style="font-size: 0.9em; color: #aaa;">少喝一杯飲料，換回你的戀愛尊嚴。</p>
                        
                        <!-- 你的 Gumroad 購買按鈕 -->
                        <a href="https://eclipsed84.gumroad.com/l/umuvow" target="_blank" style="text-decoration: none;">
                            <button style="background-color: #ffd700; color: black; border: none; padding: 12px 24px; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%;">
                                🚀 取得 VIP 解鎖碼 (約 NT$32)
                            </button>
                        </a>
                        
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"分析發生錯誤，可能是圖片無法辨識或 API 限制。({e})")
