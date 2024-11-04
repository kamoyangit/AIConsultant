# ========================================================================================================
# パスワードのチェック関数
# 日付チェック（期限日の判定）関する関数
# 2024/11/05 Koji Kamogawa
# ========================================================================================================
import streamlit as st
import os

error_max_count = 3

# パスワードの確認
def check_password():
    # 環境変数を取得
    PASSWD = os.environ.get('PASS_KEY')
    password = st.text_input("パスワードを入力してください", type="password", key="1")
    error_count = st.session_state.get('error_count', 0) # セッション状態からエラー回数を取得、初期値は0
    if error_count >= error_max_count:
        st.error(f"パスワードを3回間違えたため、実行を停止します。")
        st.stop() # 3回以上間違えたらアプリを終了
    if password == PASSWD:
        del password  # パスワード変数を削除
        st.session_state['error_count'] = 0 # エラー回数をリセット
        return True
    else:
        error_count += 1
        st.session_state['error_count'] = error_count
        del password  # パスワード変数を削除
        return False

# パスワードの確認
def check_password2():
    # 環境変数を取得
    PASSWD2 = os.environ.get('PASS_KEY')
    password2 = st.text_input("パスワードを入力してください", type="password",key="2")
    if password2 == PASSWD2:
        del password2  # パスワード変数を削除
        return True
    else:
        del password2  # パスワード変数を削除
        return False

# ========================================================================================================
import datetime
import pytz

# 今日は期限日以前かどうかをチェック
def check_date(date_string):
    try:
        # 日付文字列をdatetimeオブジェクトに変換
        date_object = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        # ISOカレンダー形式に変換して表示用にフォーマット
        iso_year, iso_week, iso_weekday = date_object.isocalendar()
        iso_string = f"{iso_year}-{iso_week:02d}-{iso_weekday:02d}"  # 例: 2024-45-6
        # print(f"ISO 8601 calendar week: {iso_string}")
    except ValueError:
        st.write(f'Not YYYY-MM-DD')
        # print("不正な日付フォーマットです。YYYY-MM-DD形式で入力してください。")

    # 現在の東京時間の日付を取得
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    japan_tz = pytz.timezone('Asia/Tokyo')
    japan_time = utc_now.astimezone(japan_tz)
    today_iso = japan_time.date().isocalendar()

    # 入力された日付の週と今日の週を比較
    if (iso_year, iso_week) >= (today_iso[0], today_iso[1]):
        return True  # 期限日がまだ先の場合
    else:
        return False  # 期限が過ぎている場合