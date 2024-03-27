#streamlit run /Users/lizongsiou/Desktop/數值分析/波動/波動.py
import mpltw
import streamlit as st
import numpy as np
from scipy.stats import qmc, norm
import plotly.graph_objects as go
import matplotlib.pyplot as plt
# 設置 Streamlit 頁面的基本配置
st.set_page_config(
   page_title="波動",  # 設定網頁標題
   layout="wide",  # 設定頁面布局為寬屏模式
   initial_sidebar_state="expanded" ) # 初始時側邊欄狀態為展開

# 在頁面頂部顯示一幅圖片
# 顯示應用的標題
st.title("假設股價為布朗模型下，請利用模擬方法得到歐式選擇權評價，探討變異數降低法對結果之影響")

with st.sidebar.form(key='my_form'):
    option_type = st.radio("選擇權型態",("Call", "Put"),horizontal=True)
    # 初始股價的滑動選擇
    S0 = st.slider('選擇初始股價 S0', min_value=50, max_value=300, value=100)

    # 行使價格的滑動選擇
    K = st.slider('選擇行使價格 K', min_value=50, max_value=300, value=105)

    # 到期時間的滑動選擇（以年為單位）
    T = st.slider('選擇到期時間 T (年)', min_value=0.1, max_value=2.0, value=1.0, step=0.1)

    # 無風險利率的滑動選擇
    r = st.slider('選擇無風險利率 r', min_value=0.01, max_value=0.10, value=0.03, step=0.01)

    # 模擬次數的滑動選擇
    N = st.slider('選擇模擬次數', min_value=100, max_value=3000, value=1000, step=1000)

    # 實驗重複次數的滑動選擇
    M = st.slider('選擇實驗重複次數', min_value=10, max_value=100, value=10, step=10)
    seed = st.text_input(label="亂數種子", value="123457")
    submit_button = st.form_submit_button(label='計算')
sigma_values = np.linspace(0.1, 0.5, 10)  # 波動率範圍
if submit_button:
    bar = st.progress(20)#顯示進度條
    fig, ax = plt.subplots()  # 使用 matplotlib 創建圖表和軸
    if option_type == "Call":
        # 固定亂數種子情況
        call_means_fixed = []
        for sigma in sigma_values:
            np.random.seed(int(seed))
            Z_fixed = np.random.normal(0, 1, N)
            ST_fixed = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z_fixed)
            call_payoffs_fixed = np.maximum(ST_fixed - K, 0)  # 歐式看漲期權到期收益
            call_means_fixed.append(np.mean(call_payoffs_fixed))

        # 繪製固定亂數種子的結果為一條明確的線
        ax.plot(sigma_values, call_means_fixed, marker='o', linestyle='-', color='blue', label='固定亂數種子')
        bar = bar.progress(40)
        # 不固定亂數種子情況，進行M次模擬
        for i in range(M):
            call_means_variable = []
            for sigma in sigma_values:
                call_payoffs_variable = []
                for _ in range(N):
                    np.random.seed(None)  # 確保每次迴圈亂數都不同
                    Z_variable = np.random.normal(0, 1)
                    ST_variable = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z_variable)
                    call_payoffs_variable.append(np.maximum(ST_variable - K, 0))  # 歐式看漲期權到期收益
                call_means_variable.append(np.mean(call_payoffs_variable))

            # 繪製每次模擬的結果
            ax.plot(sigma_values, call_means_variable, linestyle='--', alpha=0.5)
        bar = bar.progress(90)
        ax.set_title('歐式看漲期權到期收益平均值與波動率的關係')
        ax.set_xlabel('波動率 (σ)')
        ax.set_ylabel('歐式看漲期權到期收益的平均值')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)  # 將圖表顯示在 Streamlit 應用中
        bar = bar.progress(100)
    if option_type == "Put":
        put_means_fixed = []
        for sigma in sigma_values:
            np.random.seed(int(seed))
            Z_fixed = np.random.normal(0, 1, N)
            ST_fixed = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z_fixed)
            put_payoffs_fixed = np.maximum(K - ST_fixed, 0)  # 歐式看跌期權到期收益
            put_means_fixed.append(np.mean(put_payoffs_fixed))

        # 繪製固定亂數種子的結果為一條明確的線
        ax.plot(sigma_values, put_means_fixed, marker='o', linestyle='-', color='blue', label='固定亂數種子')
        bar = bar.progress(40)
        # 不固定亂數種子情況，進行M次模擬
        for i in range(M):
            put_means_variable = []
            for sigma in sigma_values:
                put_payoffs_variable = []
                for _ in range(N):
                    np.random.seed(None)  # 確保每次迴圈亂數都不同
                    Z_variable = np.random.normal(0, 1)
                    ST_variable = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z_variable)
                    put_payoffs_variable.append(np.maximum(K - ST_variable, 0))  # 歐式看跌期權到期收益
                put_means_variable.append(np.mean(put_payoffs_variable))
            
            # 繪製每次模擬的結果
            ax.plot(sigma_values, put_means_variable, linestyle='--', alpha=0.5)
        bar = bar.progress(90)
        ax.set_title('歐式看跌期權到期收益平均值與波動率的關係')
        ax.set_xlabel('波動率 (σ)')
        ax.set_ylabel('歐式看跌期權到期收益的平均值')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)  # 將圖表顯示在 Streamlit 應用中
        bar = bar.progress(100)