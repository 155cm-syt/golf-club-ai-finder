import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import time

st.set_page_config(page_title="Golf Club Pro Profit AI", layout="wide")

st.title("⛳ Golf Club Pro Profit AI")
st.write("中古ショップから利益クラブを自動検出")

shaft_keywords = [
"VENTUS","Ventus",
"Tour AD",
"Speeder",
"Diamana",
"TENSEI"
]

shops = {
"GDO Used":"https://shop.golfdigest.co.jp/used/",
"Golf Partner":"https://www.golfpartner.co.jp/"
}

def get_mercari_price(keyword):

    url=f"https://jp.mercari.com/search?keyword={keyword}"

    try:

        r=requests.get(url,timeout=10)
        soup=BeautifulSoup(r.text,"html.parser")

        prices=[]

        for span in soup.find_all("span"):

            text=span.text

            if "¥" in text:

                p=re.sub("[^0-9]","",text)

                if p:

                    price=int(p)

                    if 5000<price<150000:

                        prices.append(price)

        if len(prices)>5:

            avg=sum(prices[:10])/10

            return int(avg)

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

                    buy=20000

                    sell=get_mercari_price(name)

                    if sell:

                        profit=sell-buy

                        rate=profit/buy*100

                        if rate>10:

                            items.append({
                                "shop":shop,
                                "name":name.strip(),
                                "buy":buy,
                                "sell":sell,
                                "profit":profit,
                                "rate":round(rate,1)
                            })

    except:

        pass

    return items


min_profit = st.slider("最低利益率 %",5,50,10)

if st.button("AIスキャン開始"):

    all_items=[]

    progress=st.progress(0)

    i=0

    for shop,url in shops.items():

        data=scan_shop(shop,url)

        all_items+=data

        i+=1

        progress.progress(i/len(shops))

        time.sleep(1)

    if len(all_items)==0:

        st.warning("利益クラブなし")

    else:

        all_items=sorted(all_items,key=lambda x:x["rate"],reverse=True)

        for item in all_items:

            if item["rate"]>=min_profit:

                st.success(
f"""
{item['name']}

ショップ: {item['shop']}

仕入れ想定: ¥{item['buy']}

メルカリ相場: ¥{item['sell']}

利益: ¥{item['profit']}

利益率: {item['rate']}%
"""
)
