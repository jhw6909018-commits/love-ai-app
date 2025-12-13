import streamlit as st
import time # 模擬 AI 生成延遲，增加真實感

# --- 1. 頁面設定 (必須放在第一行) ---
st.set_page_config(
    page_title="Love AI - 你的專屬戀愛軍師",
    page_icon="💘",
    layout="centered"
)

# --- 2. 自定義 CSS (美化 UI) ---
st.markdown("""
<style>
    /* 全局背景與字體優化 */
    .stApp {
        background-color: #FFF5F7; /* 淡粉色背景 */
    }
    h1 {
        color: #D63384; /* 深粉紅標題 */
        font-family: 'Helvetica Neue', sans-serif;
    }
    /* 聊天氣泡優化 */
    .stChatMessage {
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    /* 按鈕美化 */
    .stButton>button {
        background-color: #FF6B6B;
        color: white;
        border-radius: 20px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #FF8787;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 初始化 Session State (記憶體) ---
# 這是 Streamlit 最重要的部分，沒有這個，每次按按鈕變數都會重置
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "你好！我是你的 AI 戀愛軍師。今天想聊聊什麼？或是需要我幫你寫點什麼？💘"}
    ]

# --- 4. 側邊欄 (設定區) ---
with st.sidebar:
    st.header("⚙️ 參數設定")
    relationship_status = st.selectbox(
        "目前的關係",
        ["單身/暗戀中", "曖昧中", "交往中", "已婚/老夫老妻", "剛分手/求復合"]
    )
    tone = st.slider("語氣甜度", 0, 100, 70)
    
    st.divider()
    st.info("💡 提示：越具體的描述，AI 生成的效果越好喔！")

# --- 5. 主畫面 (聊天介面) ---
st.title("💘 Love AI Assistant")

# 顯示歷史訊息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 6. 處理使用者輸入 ---
if prompt := st.chat_input("輸入你想說的話，或貼上對方的訊息..."):
    # 顯示使用者訊息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 生成回應 (這裡模擬 API 呼叫)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # 模擬 AI 思考的過程 (UX 優化)
        with st.spinner('軍師正在思考最完美的回答...'):
            time.sleep(1) # 假裝延遲，讓使用者覺得 AI 真的在想
            
            # --- 這裡替換成真正的 OpenAI / Claude API 呼叫 ---
            # 依據 sidebar 的參數來調整 prompt
            # simulated_response = call_llm(prompt, tone, relationship_status)
            simulated_response = f"針對你們目前「{relationship_status}」的狀態，建議你可以這樣回覆：\n\n**「{prompt} 的這件事，其實我也...」**\n\n(這裡加入語氣甜度 {tone}% 的修飾)"
            
            # 打字機效果 (UX 優化)
            for chunk in simulated_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
    
    # 存入歷史紀錄
    st.session_state.messages.append({"role": "assistant", "content": full_response})
