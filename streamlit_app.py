import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.title("⛳ Golf Club Profit Finder")

shaft_keywords = [
"VENTUS","Ventus",
"Tour AD",
"Speeder",
"Diamana",
"TENSEI"
]

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

                    p=int(num)

                    if 5000<p<150000:

                        prices.append(p)

        if len(prices)>3:

            return int(sum(prices[:5])/5)

    except:
        pass

    return None


def check_club(name,price):

    sell=mercari_price(name)

    if sell:

        profit=sell-price

        rate=profit/price*100

        return sell,profit,rate

    return None,None,None


club_list=[
("TaylorMade Driver Ventus",22000),
("Callaway FW Tour AD",18000),
("PING Hybrid Speeder",15000),
("Titleist Driver Tensei",20000)
]


if st.button("AIスキャン開始"):

    for name,price in club_list:

        sell,profit,rate=check_club(name,price)

        if sell:

            if rate>10:

                st.success(
f"""
{name}

仕入れ価格 ¥{price}

メルカリ相場 ¥{sell}

利益 ¥{profit}

利益率 {round(rate,1)}%
"""
)
