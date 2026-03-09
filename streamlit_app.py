import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="Golf Club Auto Profit AI",layout="wide")

st.title("⛳ Golf Club Auto Profit AI")
st.write("AIが利益クラブを自動検出します")

shaft_keywords = ["VENTUS","Ventus","Tour AD","Speeder"]

shops = {
    "Golf Partner":"https://www.golfpartner.co.jp/",
    "GDO":"https://shop.golfdigest.co.jp/",
    "Golf5":"https://www.golf5.co.jp/"
}

def mercari_price(keyword):

    url = f"https://jp.mercari.com/search?keyword={keyword}"

    try:
        r = requests.get(url,timeout=10)
        soup = BeautifulSoup(r.text,"html.parser")

        prices=[]

        for span in soup.find_all("span"):
            t=span.text

            if "¥" in t:

                p=re.sub("[^0-9]","",t)

                if p!="":

                    price=int(p)

                    if 5000<price<150000:

                        prices.append(price)

        if len(prices)>5:

            return int(sum(prices[:10])/10)

    except:
        pass

    return None


def scan_shop(shop,url):

    items=[]

    try:

        r=requests.get(url,timeout=10)
        soup=BeautifulSoup(r.text,"html.parser")

        links=soup.find_all("a")

        for link in links:

            name=link.get_text()

            for shaft in shaft_keywords:

                if shaft in name:

                    buy=15000

                    sell=mercari_price(name)

                    if sell:

                        profit=sell-buy
                        rate=profit/buy*100

                        if rate>10:

                            items.append({
                                "shop":shop,
                                "name":name,
                                "buy":buy,
                                "sell":sell,
                                "profit":profit,
                                "rate":round(rate,1)
                            })

    except:
        pass

    return items


if st.button("AIスキャン開始"):

    all_items=[]

    for shop,url in shops.items():

        result=scan_shop(shop,url)

        all_items+=result

    if len(all_items)==0:

        st.warning("利益候補なし")

    else:

        all_items=sorted(all_items,key=lambda x:x["rate"],reverse=True)

        for item in all_items[:20]:

            st.success(
                f"{item['name']} | {item['shop']} | 利益率 {item['rate']}%"
            )
