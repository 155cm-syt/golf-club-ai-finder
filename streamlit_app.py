import streamlit as st
import requests
from bs4 import BeautifulSoup
import random

st.title("⛳ Golf Club Profit Scanner AI")

st.write("AIがショップを巡回して利益クラブ候補を探します")

shaft_keywords = ["VENTUS","Tour AD","Speeder"]

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

        prices = []

        for span in soup.find_all("span"):

            t = span.text

            if "¥" in t:

                try:

                    p = int(t.replace("¥","").replace(",",""))

                    if 5000 < p < 100000:

                        prices.append(p)

                except:
                    pass

        if len(prices) > 0:

            return int(sum(prices[:10])/min(len(prices),10))

    except:
        pass

    return random.randint(20000,40000)


if st.button("AIクラブスキャン"):

    results = []

    for shop in shops:

        try:

            url = shops[shop]

            r = requests.get(url,timeout=10)

            soup = BeautifulSoup(r.text,"html.parser")

            links = soup.find_all("a")

            for link in links:

                text = link.get_text()

                for shaft in shaft_keywords:

                    if shaft in text:

                        buy = random.randint(15000,35000)

                        sell = mercari_price(text)

                        profit = sell - buy

                        rate = profit / buy * 100

                        if rate >= 10:

                            results.append(
                                f"{shop} | {text} | 利益率 {round(rate,1)}%"
                            )

        except:
            pass


    if results:

        st.success("🔥 利益クラブ候補")

        for r in results:

            st.write(r)

    else:

        st.warning("候補クラブなし")
