import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
import os

# --- 0. API 設定 ---
# ⚠️ 請將這裡換成你自己的 Key
GOOGLE_API_KEY = "AIzaSyAOVCNW74yDY3MVRcyPfimFKr1Q4nnwXfI"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 1. 頁面基礎設定 ---
st.set_page_config(
    page_title="🚑 暈船急救站 | Love Emergency",
    page_icon="💔",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. CSS 高級美化 (Cyberpunk ER 風格) ---
st.markdown("""
<style>
    /* 全站背景與字體 */
    .stApp {
        background-color: #050505;
        color: #e0e0e0;
    }
    
    /* 標題樣式 */
    h1 {
        color: #ff4b4b !important;
        text-shadow: 0 0 10px #990000;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* 側邊欄美化 */
    [data-testid="stSidebar"] {
        background-color: #111;
        border-right: 1px solid #333;
    }
    
    /* 上傳區塊美化 (帶有呼吸燈效果) */
    [data-testid="stFileUploader"] {
        border: 2px dashed #ff4b4b;
        border-radius: 10px;
        padding: 20px;
        background-color: #1a0505;
        transition: all 0.3s;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #ff0000;
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.3);
    }
    
    /* 按鈕美化 */
    .stButton>button {
        background: linear-gradient(90deg, #990000 0%, #ff4b4b 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        font-weight: bold;
        border-radius: 8px;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(255, 0, 0, 0.3);
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(255, 0, 0, 0.5);
    }

    /* VIP 金卡區塊 */
    .vip-card {
        background: linear-gradient(135deg, #2c2c2c 0%, #1a1a1a 100%);
        border: 1px solid #ffd700;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin-top: 10px;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.1);
    }
    .vip-btn {
        background: linear-gradient(90deg, #ffd700 0%, #ffcc00 100%);
        color: #000;
        text-decoration: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: 800;
        display: inline-block;
        margin-top: 10px;
        width: 100%;
        box-shadow: 0 4px 10px rgba(255, 215, 0, 0.4);
    }
    .vip-btn:hover {
        background: #fff;
        box-shadow: 0 0 20px #ffd700;
    }
    
    /* 隱藏不必要的元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. 側邊欄 (VIP 控制台) ---
with st.sidebar:
    # 如果有 logo.png 就顯示，沒有就顯示文字
    if os.path.exists("logo.png"):
        st.image("logo.png", width=100)
    else:
        st.header("⚙️ 控制台")
        
    st.markdown("---")
    
    st.markdown("### 🔐 VIP 通行證")
    vip_input = st.text_input("輸入解鎖碼 (Code)", placeholder="請輸入 LOVE2026")
    
    # 驗證密碼
    VALID_CODE = "LOVE2026" 
    is_vip = (vip_input == VALID_CODE)
    
    if is_vip:
        st.success("✅ 尊爵 VIP 已啟用")
        st.caption("無限次深度分析 / 神回覆建議")
    else:
        st.info("🔒 一般訪客模式")
        st.caption("僅顯示基礎暈船分數")
        
        # 美化版的購買連結
        st.markdown("""
        <div class="vip-card">
            <div style="color: #ffd700; font-size: 18px; font-weight: bold;">👑 升級 VIP 版</div>
            <div style="color: #aaa; font-size: 12px; margin-bottom: 5px;">解鎖「對方潛台詞」與「必勝回覆」</div>
            <a href="https://eclipsed84.gumroad.com/l/umuvow" target="_blank" class="vip-btn">
                ⚡ 取得解鎖碼 ($1)
            </a>
        </div>
        """, unsafe_allow_html=True)

# --- 4. 主畫面設計 ---

# 頂部 Banner (如果有圖檔的話)
if os.path.exists("banner.png"):
    st.image("banner.png", use_container_width=True)
else:
    # 沒有圖檔時的備案
    st.markdown("# 🚑 暈船急救站")
    st.markdown("### <span style='color:#ff4b4b'>全台首創 AI 戀愛診斷系統</span>", unsafe_allow_html=True)

st.caption("👉 上傳你們的對話紀錄，AI 幫你判斷：他是真的忙，還是你只是備胎？")

# 檔案上傳區
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], help="支援 LINE / IG / Messenger 截圖")

if uploaded_file:
    # 顯示預覽圖 (稍微縮小一點比較好看)
    image = Image.open(uploaded_file)
    with st.expander("📸 預覽已上傳的截圖", expanded=True):
        st.image(image, use_container_width=True)
    
    # 分析按鈕
    if st.button("💉 開始診斷 (Start Analysis)"):
        # 建立模型
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 模擬讀取進度條 (增加儀式感)
        progress_text = "AI 正在掃描對話..."
        my_bar = st.progress(0, text=progress_text)
        
        for percent_complete in range(100):
            time.sleep(0.01)
            if percent_complete == 30:
                my_bar.progress(percent_complete + 1, text="正在計算曖昧濃度...")
            elif percent_complete == 60:
                my_bar.progress(percent_complete + 1, text="正在分析對方潛台詞...")
            else:
                my_bar.progress(percent_complete + 1)
        
        my_bar.empty() # 清除進度條

        with st.spinner('生成最終診斷報告中...'):
            try:
                # Prompt 設計
                if is_vip:
                    prompt = """
                    你是一位專業、犀利但富有同理心的戀愛心理學家。請分析這張對話截圖：
                    
                    【📊 暈船診斷書】
                    1. **暈船指數 (0-100%)**：請給出一個具體分數。
                    2. **病徵分析**：使用者的對話有什麼問題？對方的反應代表什麼？(請詳細分析潛台詞)
                    3. **急救處方籤**：
                       - 如果還有救：給出三個「神回覆」選項 (高冷/幽默/直球)。
                       - 如果沒救了：請溫柔地勸退使用者。
                    
                    語氣要求：像個很懂人性的朋友，專業中帶點幽默。使用 Markdown 格式排版，多用 emoji。
                    """
                else:
                    prompt = """
                    你是一位毒舌的戀愛評論家。請分析這張對話截圖：
                    
                    1. **暈船指數 (0-100%)**：直接給分。
                    2. **一句話短評**：用最犀利的一句話吐槽這個狀況。
                    3. **結尾引導**：請務必在最後加上：「⚠️ 想知道對方心裡在想什麼？想獲得必勝神回覆？請解鎖 VIP 查看完整報告。」
                    """

                response = model.generate_content([prompt, image])
                
                # --- 結果顯示區 ---
                st.markdown("---")
                
                if is_vip:
                    st.success("✅ 分析完成！以下是您的詳細報告")
                    st.markdown(response.text)
                    st.balloons() # VIP 限定特效
                else:
                    st.warning("⚠️ 基礎分析完成 (完整版已鎖定)")
                    st.write(response.text)
                    
                    # 再次強力引導付費
                    st.markdown("---")
                    st.markdown("""
                    <div style="background-color: #111; border: 2px dashed #ffd700; padding: 30px; text-align: center; border-radius: 10px;">
                        <h2 style="color: #ffd700; margin:0;">🔓 解鎖完整分析報告</h2>
                        <p style="color: #ccc; margin-top: 10px;">對方的潛台詞是什麼？這句該怎麼回？</p>
                        <p style="color: #ff4b4b; font-weight: bold;">少喝一杯手搖飲，換回你的戀愛主導權。</p>
                        <br>
                        <a href="https://eclipsed84.gumroad.com/l/umuvow" target="_blank" style="text-decoration: none;">
                            <button style="background: linear-gradient(90deg, #ffd700 0%, #ffcc00 100%); color: black; border: none; padding: 15px 30px; font-size: 18px; border-radius: 50px; cursor: pointer; font-weight: 800; box-shadow: 0 0 20px rgba(255, 215, 0, 0.6);">
                                🚀 立即取得 VIP 碼 ($1)
                            </button>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"分析失敗，請重試。({e})")
