import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


# ホームページを定義
def home():
    st.title("ホームページ")
    st.write("施策提案と効果確認と改善提案の企画支援アプリケーション")


# ヒアリングシートシートページ
def hearing_sheet():
    st.title("ヒアリングシート")

    # 5W3Hの質問とプレテキスト
    questions = {
        "Why: 目的": "ゴール: 顧客のリピート利用率を高めたい\nKGI: ニーズに合った商品訴求力の向上\nKPI: 訴求商品のQR遷移率",
        "What: 訴求内容": "・お礼メッセージ\n・次回利用で使えるクーポン\n・購入商品に基づくおすすめ",
        "When: スケジュール": "3ヶ月のお試し実施で、効果が見られれば半年延長",
        "Where: 媒体": "チラシ",
        "Who: 誰が": "自動化",
        "How: 手段": "自動化WF+QRチェッカー+CRMデータ",
        "How much: 見積": "ランニングコスト: \n設置コスト: \n チラシ代: \nコンサル費用: ",
        "How much: 想定結果": "Nか月後に目標となる再利用率%を上回ったら、半年延長する\nQR遷移率がXX%を下回ったら、訴求方針を変更する",
    }

    # 回答を保持する辞書
    responses = {}

    # ユーザー入力フィールドの生成
    for question, placeholder in questions.items():
        responses[question] = st.text_area(question, value=placeholder, height=100)


# 施策提案ページ
def policy_suggestion():
    st.title("施策提案ページ")
    # ここでDB検索やGPTを活用したサジェスト機能を実装
    # プレ入力されたテキスト例
    default_current = "現在の市場シェアは10%で、競合に比べて低迷しています。顧客のニーズに十分応えられていない可能性があります。"
    default_ideal = "市場シェアを20%に拡大し、顧客満足度を向上させることで、業界のリーダーとしての地位を確立したい。"

    # テキストエリアでの入力
    current_situation = st.text_area(
        "現状を入力してください", value=default_current, height=100
    )
    ideal_situation = st.text_area(
        "理想を入力してください", value=default_ideal, height=100
    )
    submit_button = st.button("生成AIで施策提案を生成")

    if submit_button and current_situation and ideal_situation:
        # 提案テキストの生成
        proposal_text = f"現状：{current_situation}\n理想：{ideal_situation}\nを達成するために、\n**〇〇セグメント顧客に対しての「新規紹介キャンペーン」**を提案します。ここはChatGPTに施策パッケージDBから適したそれっぽいものを選択して提案してもらいます"
        st.text_area("提案内容", proposal_text, height=200)


# 施策パッケージのサンプルデータ
policy_packages = [
    {
        "title": "展示会リードフォローアップ",
        "purpose": "展示会の後に追いDMを送って商談化を狙う",
        "metric": "電話問い合わせ数、QR遷移率",
        "price": "10万円/10000通",
    },
    {
        "title": "高級商材リードフォローアップ",
        "purpose": "不動産など高級商材のリードナーチャリング",
        "metric": "問い合わせ数、QR遷移率",
        "price": "10万円/10000通",
    },
    {
        "title": "長期費用発生ものリードフォローアップ",
        "purpose": "塾など長期契約もののリードナーチャリング",
        "metric": "模試申込数、QR遷移率",
        "price": "10万円/10000通",
    },
    {
        "title": "新規紹介キャンペーン",
        "purpose": "知人友人紹介のクーポンで新規獲得を狙う",
        "metric": "新規登録数",
        "price": "10万円/10000通",
    },
    {
        "title": "ロイヤルティ向上",
        "purpose": "購買後に、同一目的でのリピート利用を促進する",
        "metric": "再利用数、QR遷移率",
        "price": "10万円/10000通",
    },
    {
        "title": "ブランドへの入り口増設",
        "purpose": "購買後に、別の新しい目的での利用を促進する",
        "metric": "利用数、QR遷移率",
        "price": "10万円/10000通",
    },
    {
        "title": "顧客インサイト特定",
        "purpose": "誰に何を伝えればいいかわからないとき、セグメント別のニーズを特定する",
        "metric": "QR遷移率",
        "price": "10万円/10000通",
    },
    {
        "title": "ブランド強みの特定",
        "purpose": "どのような理由で購買してくれているのか分からないとき、利用目的を調査する",
        "metric": "アンケート回答数、QR遷移率",
        "price": "10万円/10000通",
    },
]

# セッションステートにregistered_policiesを初期化
if "registered_policies" not in st.session_state:
    st.session_state.registered_policies = [
        {
            "title": "展示会リードフォローアップ",
            "purpose": "展示会の後に追いDMを送って商談化を狙う",
            "metric": "電話問い合わせ数、QR遷移率",
            "price": "10万円/10000通",
        }
    ]


# 施策パッケージ登録ページ
def policy_registration():
    st.title("施策パッケージ登録ページ")
    st.write("")
    st.write("施策パッケージを選択してください")
    st.write("")

    for policy in policy_packages:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(policy["title"])
                st.write("目的：", policy["purpose"])
                st.write("効果測定指標：", policy["metric"])
                st.write("価格：", policy["price"])
            with col2:
                if st.button("登録", key=policy["title"]):
                    st.session_state.registered_policies.append(policy)
                    st.success(f"{policy['title']} が登録されました。")
            st.markdown("---")


# モックデータの生成
def create_mock_data():
    data = {
        "セグメント": [
            "セグメントA",
            "セグメントB",
            "セグメントC",
            "セグメントD",
            "セグメントE",
        ],
        "電話問い合わせ数": [5, 14, 12, 2, 7],
        "QR遷移率": [0.05, 0.19, 0.10, 0.14, 0.03],
        "QR読込数": [74, 121, 98, 44, 109],
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
                improvements.append(
                    f"{row['セグメント']} の{col}が低いです。**ChatGPTで生成した施策の改善案**を提案します。"
                )
    return improvements


# 効果可視化ページ
def policy_visualization():
    st.title("効果可視化ページ")
    date_range_selector()
    # 水平線と空行を挿入
    st.markdown("---")
    st.write("")
    if st.session_state.registered_policies:
        policy_titles = [p["title"] for p in st.session_state.registered_policies]
        selected_policy = st.selectbox("登録済み施策を選択してください", policy_titles)

        if selected_policy == "展示会リードフォローアップ":
            data = create_mock_data()
            st.dataframe(
                data.style.applymap(
                    lambda x: "background-color: red" if x < 0.1 else "",
                    subset=["QR遷移率"],
                )
            )
            improvements = generate_improvements(data)
            if improvements:
                for improvement in improvements:
                    st.error(improvement)
    else:
        st.write("登録された施策がありません。")


# 施策管理改善ページ
def policy_improvement():
    st.title("施策管理改善ページ")

    # 登録されている施策の編集
    for i, policy in enumerate(st.session_state.registered_policies):
        with st.expander(f"{policy['title']}"):
            new_title = st.text_input(
                "タイトル", value=policy["title"], key=f"title_{i}"
            )
            new_purpose = st.text_area(
                "目的", value=policy["purpose"], key=f"purpose_{i}", height=100
            )
            new_metric = st.text_input(
                "効果測定指標", value=policy["metric"], key=f"metric_{i}"
            )
            new_price = st.text_input("価格", value=policy["price"], key=f"price_{i}")
            if st.button("保存", key=f"save_{i}"):
                # 変更を保存
                policy["title"] = new_title
                policy["purpose"] = new_purpose
                policy["metric"] = new_metric
                policy["price"] = new_price
                st.success(f"{new_title} の情報が更新されました。")


# ナビゲーション
st.sidebar.title("ナビゲーション")
page = st.sidebar.radio(
    "ページを選択",
    (
        "ホーム",
        "ヒアリングシート",
        "施策提案",
        "施策パッケージ登録",
        "効果可視化",
        "施策管理改善",
    ),
)

if page == "ホーム":
    home()
elif page == "ヒアリングシート":
    hearing_sheet()
elif page == "施策提案":
    policy_suggestion()
elif page == "施策パッケージ登録":
    policy_registration()
elif page == "効果可視化":
    policy_visualization()
elif page == "施策管理改善":
    policy_improvement()
