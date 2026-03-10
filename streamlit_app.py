import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.title("⛳ ゴルフクラブ転売 利益計算AI")

club_name = st.text_input("クラブ名を入力（例: SIM2 Ventus）")

buy_price = st.number_input("仕入れ価格",0,100000,20000)

def mercari_price(keyword):

    url=f"https://jp.mercari.com/search?keyword={keyword}"

    try:

        r=requests.get(url)

        soup=BeautifulSoup(r.text,"html.parser")

        prices=[]

        for span in soup.find_all("span"):

            text=span.text

            if "¥" in text:

                num=re.sub("[^0-9]","",text)

                if num:

                    price=int(num)

                    if 5000<price<150000:

                        prices.append(price)

        if len(prices)>5:

            avg=sum(prices[:10])/10

            return int(avg)

    except:
        pass

    return None


if st.button("利益計算"):

    if club_name=="":

        st.warning("クラブ名を入力してください")

    else:

        sell=mercari_price(club_name)

        if sell:

            profit=sell-buy_price

            rate=profit/buy_price*100

            st.success(f"メルカリ平均価格: ¥{sell}")

            st.success(f"利益: ¥{profit}")

            st.success(f"利益率: {round(rate,1)} %")

        else:

            st.error("相場取得できませんでした")
