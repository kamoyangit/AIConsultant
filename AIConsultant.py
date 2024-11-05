# ========================================================================================================
# 事業アイデアのLLMで評価するためのプロンプトを生成するアプリ
# 条件付きで、LLM（Google Gemini）にアクセスして、事業評価結果を出力する機能あり
# 2024/11/04 Koji Kamogawa
# ========================================================================================================
import streamlit as st
from utils import check_password, check_date
from llmAccess import sub_main

DEBUG_MODE = False  # デバッグモードを有効/無効にするフラグ
filepath = "my_prompt.txt"
text_data = ""

# ========================================================================================================
# 評価方法
def check_evaluation(param):
    text1 = "あなたは、優秀な事業コンサルタントです。ユーザの考えた事業アイデアに対して、厳しく評価して下さい"
    text2 = "あなたは、優秀な事業コンサルタントです。ユーザの考えた事業アイデアに対して、偏見を持たずに中庸に評価して下さい"
    text3 = "あなたは、優秀な事業コンサルタントです。ユーザの考えた事業アイデアに対して、前向きかつ、ポジティブに評価して下さい"
    ans = ""
    if param == "厳密":
        ans = text1
    elif param == "中庸":
        ans = text2
    elif param == "寛容":
        ans = text3
    else :
        ans = text2
    return ans

# 会社名
def check_companyName(param):
    return param

# 会社のアセット
def check_companyAssets(param):
    return param

# 想定顧客(男女)
def check_targetUserSex(param):
    ans = ""
    if param == "両方":
        ans = "男女問わず両方"
    elif param == "男性":
        ans = "主に男性"
    elif param == "女性":
        ans = "主に女性"
    else:
        ans = "男女問わず両方"
    return ans

# 想定顧客(年齢)
def check_targetUserAge(param0, param1, param2, param3, param4, param5, param6):
    ans = ""
    if param0 == True:
        ans += "20歳未満 "
    if param1 == True:
        ans += "20代 "
    if param2 == True:
        ans += "30代 "
    if param3 == True:
        ans += "40代 "
    if param4 == True:
        ans += "60代 "
    if param5 == True:
        ans += "70代 "
    if param6 == True:
        ans += "70歳以上 "
    if ans == "":
        ans = "年齢を問わず全世代"
    return ans

# 解決する社会課題
def check_socialIssue(param):
    return param

# ソリューションの名称
def check_solutionName(param):
    return param

# ソリューションの説明
def check_solutionDetail(param):
    return param

# ========================================================================================================
def main():
    # Header / subheader
    st.header("AI コンサルタント(プロトタイプ Ver0.1)")
    # st.subheader("あなたの事業アイデアを評価")
    st.write("あなたの事業アイデアを《AIコンサルタント》が評価します")

    # パスワードチェック
    if check_password():
        st.divider()
        # Radio Button
        # 複数の選択肢から一つの項目を選ぶときに使用する。horizontal引数にTrueを指定すると横に並ぶ
        decision = st.radio("【評価方法】", ('厳密', '中庸', '寛容'), index=1, horizontal=True)
        if DEBUG_MODE:
            st.write(f"{decision}に評価します")

        # text input
        # 1行でテキストを入力する部品。入力した値は戻り値として返す
        company = st.text_input('【会社名】：必須', placeholder='xxxxxx株式会社')
        if DEBUG_MODE:
            st.write('入力会社名：', company)

        # text Area
        # 複数行のテキスト入力を受け付ける部品。入力したテキストは文字列として返す
        assets = st.text_area('【会社のアセット】：必須', placeholder='あなたの会社の持つアセット・特徴・強みなどを記述して下さい')
        if DEBUG_MODE:
            st.write(f'{assets}')
        st.divider()

        # Radio Button
        # 複数の選択肢から一つの項目を選ぶときに使用する。horizontal引数にTrueを指定すると横に並ぶ
        sex = st.radio("【想定顧客】", ('両方','男性', '女性'), index=0, horizontal=True)
        if DEBUG_MODE:
            st.write(f"{sex}")
        # CheckBox
        # 選択するとTrueを返す
        col0, col1, col2, col3, col4, col5, col6 = st.columns(7)
        with col0:
            option0 = st.checkbox('20歳未満')
        with col1:
            option1 = st.checkbox('20代')
        with col2:
            option2 = st.checkbox('30代')
        with col3:
            option3 = st.checkbox('40代')
        with col4:
            option4 = st.checkbox('50代')
        with col5:
            option5 = st.checkbox('60代')
        with col6:
            option6 = st.checkbox('70歳以上')
        if DEBUG_MODE:
            st.write(f'You selected -20:{option0} 20:{option1} 30:{option2} 40{option3} 50{option4} 60{option5} 70-{option6}')
        st.divider()

        # Select
        # プルダウンメニューから項目を選択するときの部品
        issue = st.selectbox(
            '【解決する社会課題】',
            ('少子高齢化と人口減少','災害の激甚化','環境問題','都市部への人口集中と地方の過疎化','情報リテラシーの格差','生産性の低迷','ジェンダー平等','インフラの老朽化','気候変動による自然災害の増加','大型地震の発生','その他'))
        if DEBUG_MODE:
            st.write('解決する社会課題:', issue)
        st.divider()

        # text input
        # 1行でテキストを入力する部品。入力した値は戻り値として返す
        solution_title = st.text_input('【ソリューションの名称】：必須', placeholder='例）万能アシスタント家電')
        if DEBUG_MODE:
            st.write('ソリューション名：', solution_title)

        # text Area
        # 複数行のテキスト入力を受け付ける部品。入力したテキストは文字列として返す
        solution_detail = st.text_area('【ソリューションの説明】：必須', placeholder='提案するソリューションについて、出来るだけ詳しく記述して下さい')
        if DEBUG_MODE:
            st.write(f'{solution_detail}')
        st.divider()

        # DEBUG_MODEの時は、値を自動で挿入する
        if DEBUG_MODE:
            company = "日立グローバルライフソリューションズ"
            assets = "白物家電の製造・販売、全国保守網、高信頼性製品"
            issue = "少子高齢化と人口減"
            solution_title = "高齢者遠隔見守りサービス「ドシテル」"
            solution_detail = "マイクロ波のセンサーを高齢者宅に取り付け、高齢者の宅内での活動をマクロ波センサーで検知する。検知したデータは、Wifeとインターネットを通じて、サーバーにアップロードする。サーバーにアップロードされたデータは定期的にデータ処理され、高齢者の活動量を把握するデータとして生成される。高齢者を見守る遠隔地の家族は、スマートフォンやPCを使って、サーバーにアクセスし、高齢者の活動量を見ることで、異常がないか（起きれないままになっていないか、活動量が減ってないか）を知ることができる。また、マイクロ波センサーを使っているため、一般的なカメラの使うのと比較して、高齢者のプライバシーが守られる、通信に使うデータが少なくて済むといった特徴がある。"

        text_data = f"""
        #命令書：
        以下の内容に基づいて、業務を遂行して下さい。
        - 評価方法：{check_evaluation(decision)}

        # アイデア評価のための情報
        - 会社名：{check_companyName(company)}
        - 会社のアセット：{check_companyAssets(assets)}
        - 想定顧客男女：{check_targetUserSex(sex)}
        - 想定顧客年齢：{check_targetUserAge(option0,option1,option2,option3,option4,option5,option6)}
        - 解決する社会課題：{check_socialIssue(issue)}
        - ソリューション名：{check_solutionName(solution_title)}
        - ソリューションの説明：{check_solutionDetail(solution_detail)}

        # 評価基準
        - 会社のアセットが、ソリューションの説明の内容とマッチしているかどうか
        - 想定顧客男女と想定顧客年齢が、ソリューションの説明の内容とマッチしているかどうか
        - 解決する社会課題と、ソリューションの説明の内容とマッチしているかどうか
        - ソリューションの説明の内容自体に新規性、独自性が含まれているかどうか
        - ソリューションの説明の内容自体の実現可能性は高いかどうか

        # 評価結果の出力フォーマット
        - ソリューションの概要（100文字以内）
        - ソリューションにより期待される効果
        - ソリューションの長所
        - ソリューションの短所
        - ソリューションの更なる改善案の提示
        - ソリューションと類似した製品/サービスに関する情報
        - ソリューションの総合評価結果
        """

        # Button
        # BUttonが押されると、Trueを返す
        #st.write("各項目の入力が済んだら、【アイデア評価ボタン】を押して下さい")
        #if st.button('【アイデア生成ボタン】'):
        #    if company=="" or assets == "" or issue == "" or solution_title == "" or solution_detail == "":
        #        st.write(f'必要項目の記載が漏れていますので、見直して下さい')
        #    else:
        #        data_save(text_data)
        #        if DEBUG_MODE:
        #            st.write('make file')

        st.write("各項目の入力が済んだら、【チェック・ボタン】を押して下さい")
        if st.button('【チェック・ボタン】'):
            if company=="" or assets == "" or issue == "" or solution_title == "" or solution_detail == "":
                st.write(f'必須項目の記載が漏れていますので、見直して下さい')
            else:
                st.write(f'【プロンプト生成ボタン】を押すと、プロンプトがダウンロードされます')
                st.write(f"ダウンロードしたプロンプトは、LLMの入力データして利用して下さい。")
                # Download Button
                # Download BUttonが押されると、ファイルを保存する
                st.download_button(
                    label="プロンプト生成ボタン",
                    data=text_data.encode('utf-8'),
                    file_name=filepath,
                    mime='text/plain',
                )

        # Header / subheader
        st.divider()
        st.subheader("クラウド上のLLMにアクセス【実験的実装】")
        st.write(f"この機能は、データをサーバアップロードするため、社内データや個人情報を含むデータの場合には、利用しないで下さい。")
        st.write(f"尚、この機能は、2024年11月9日以降は実行できなくなります。")
        if st.button("【LLMにアクセスして評価】"):
            sub_main(text_data)

# ========================================================================================================
if __name__ == "__main__":
    main()