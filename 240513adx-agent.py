import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


# ホームページを定義
def home():
    st.title("ホームページ")
    st.write("施策提案と効果確認と改善提案の支援アプリケーション")

# 施策提案ページ
def policy_suggestion():
    st.title("施策提案ページ")
    # ここでDB検索やGPTを活用したサジェスト機能を実装
    current_situation = st.text_input("現状を入力してください")
    ideal_situation = st.text_input("理想を入力してください")
    submit_button = st.button("提案を生成")

    if submit_button and current_situation and ideal_situation:
        # 提案テキストの生成
        proposal_text = f"現状：{current_situation}、理想：{ideal_situation}、を達成するために、**〇〇セグメント顧客に対しての「商品特徴理解促進施策」**を提案します。ここはChatGPTに施策パッケージDBから適したそれっぽいものを選択して提案してもらいます"
        st.text_area("提案内容", proposal_text, height=300)
    
# 施策パッケージのサンプルデータ
policy_packages = [
    {"title": "商品特徴理解促進", "purpose": "特定の商品の特徴理解を促進する", "metric": "webページ遷移率"},
    {"title": "リピート購入向上", "purpose": "顧客のリピート購入を促進する", "metric": "リピート購入率の向上"},
    {"title": "新規顧客獲得", "purpose": "新規顧客を獲得する", "metric": "新規訪問者数の増加"},
]

# セッションステートにregistered_policiesを初期化
if 'registered_policies' not in st.session_state:
    st.session_state.registered_policies = ["商品特徴理解促進"]

# 施策登録ページ
def policy_registration():
    st.title("施策登録ページ")

    for policy in policy_packages:
        with st.container():
            expander = st.expander(f"{policy['title']}")
            with expander:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(policy["title"])
                    st.write("目的：", policy["purpose"])
                    st.write("効果測定指標：", policy["metric"])
                with col2:
                    if st.button("登録", key=policy["title"]):
                        st.session_state.registered_policies.append(policy)
                        st.success(f"{policy['title']} が登録されました。")


# モックデータの生成
def create_mock_data():
    data = {
        "セグメント": ["セグメントA", "セグメントB", "セグメントC", "セグメントD", "セグメントE"],
        "QR遷移率": [0.05, 0.19, 0.09, 0.14, 0.03],
        "QR読込数": [74, 121, 98, 44, 109]
    }
    return pd.DataFrame(data)

# 日付範囲を選択するフィールド
def date_range_selector():
    st.write("日付範囲選択")

    # デフォルトの日付範囲を設定
    default_start_date = datetime.today() - timedelta(days=7)
    default_end_date = datetime.today()

    # 日付選択フィールド
    start_date = st.date_input("開始日", value=default_start_date)
    end_date = st.date_input("終了日", value=default_end_date)


# データの閾値チェックと改善提案の生成
def generate_improvements(data, threshold=0.1):
    improvements = []
    for idx, row in data.iterrows():
        for col in ["QR遷移率"]:
            if row[col] < threshold:
                improvements.append(f"{row['セグメント']} の{col}が低いです。**ChatGPTで生成した改善案**を提案します。")
    return improvements

# 効果可視化ページ
def policy_visualization():
    st.title("効果可視化ページ")
    date_range_selector()
     # 水平線と空行を挿入
    st.markdown("---")
    st.write("")
    if st.session_state.registered_policies:
        policy_titles = [p['title'] for p in st.session_state.registered_policies]
        selected_policy = st.selectbox("登録済み施策を選択してください", policy_titles)
        
        if selected_policy == "商品特徴理解促進":
            st.write("選択した施策: 商品特徴理解促進")
            st.write("効果測定指標: webページ遷移率")
            data = create_mock_data()
            st.dataframe(data.style.applymap(lambda x: 'background-color: red' if x < 0.1 else '', subset=['QR遷移率']))
            improvements = generate_improvements(data)
            if improvements:
                for improvement in improvements:
                    st.error(improvement)
    else:
        st.write("登録された施策がありません。")

# 施策改善ページ
def policy_improvement():
    st.title("施策改善ページ")
    st.text_area("施策の内容を編集してください")

# ナビゲーション
st.sidebar.title("ナビゲーション")
page = st.sidebar.radio("ページを選択", ("ホーム", "施策提案", "施策登録", "効果可視化", "施策改善"))

if page == "ホーム":
    home()
elif page == "施策提案":
    policy_suggestion()
elif page == "施策登録":
    policy_registration()
elif page == "効果可視化":
    policy_visualization()
elif page == "施策改善":
    policy_improvement()
