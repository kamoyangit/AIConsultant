# ========================================================================================================
# クラウド上のLLMにアクセス【実験的実装】
# LLM:Google Gemini-1.5-Flash
# 2024/11/04 Koji Kamogawa
# ========================================================================================================
import streamlit as st
import os
import google.generativeai as genai
import time
from utils import check_date

# Google API KEYをGoogle Studio AIからコピーして""の中に貼り付ける
MY_API_KEY=""

# チャットのAPIを使えるように設定する関数
def configure_api():
    if MY_API_KEY == "":
        # 環境変数からGoogle APIキーを取得
        GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
        if not GOOGLE_API_KEY:
            raise ValueError("Google API key is missing")
        # APIキーを用いてGoogle AIを設定
        genai.configure(api_key=GOOGLE_API_KEY)
    else:
        # 上記で設定したAPIキーを用いてGoogle AIを設定
        genai.configure(api_key=MY_API_KEY)
    return genai.GenerativeModel("gemini-1.5-flash")

# ダイアログ表示
@st.dialog("評価結果", width="large")
def result_disp(text):
    st.write(text)

def sub_main(text_data):
    # 日付をチェック
    if check_date("2024-11-9"):
        # 少し時間が掛かるのを明示するため
        with st.spinner('処理中...'):
            time.sleep(20)  # 時間がかかる処理をシミュレート
        # modelの設定
        model = configure_api()
        # システムプロンプトとユーザー入力の結合
        full_prompt = f"{text_data}"
        # Gemini API へのプロンプト送信
        response = model.generate_content(full_prompt)
        # 応答の表示
        result_disp(response.text)
    