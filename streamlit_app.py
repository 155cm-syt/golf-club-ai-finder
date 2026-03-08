import streamlit as st

st.title("⛳ Golf Club Profit Finder AI")

st.header("クラブ転売 利益チェック")

buy_price = st.number_input("仕入れ価格（円）", min_value=0)
sell_price = st.number_input("メルカリ販売予想価格（円）", min_value=0)

if buy_price > 0 and sell_price > 0:

    profit = sell_price - buy_price
    rate = (profit / buy_price) * 100

    st.write("利益:", profit, "円")
    st.write("利益率:", round(rate,2), "%")

    if rate >= 10:
        st.success("🔥 利益あり！仕入れ候補クラブ")
    else:
        st.warning("利益10%未満")
