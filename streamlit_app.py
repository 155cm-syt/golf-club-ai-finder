import streamlit as st
import random

st.title("⛳ Golf Club Auto Profit AI")

st.write("AIが利益クラブを自動検出します")

if st.button("AIスキャン開始"):

    clubs = [
        {"name":"TaylorMade Driver + Ventus","buy":28000,"sell":35000},
        {"name":"Callaway FW + Tour AD","buy":22000,"sell":29000},
        {"name":"PING Hybrid + Speeder","buy":18000,"sell":21000},
        {"name":"Titleist Driver + Ventus","buy":30000,"sell":36000},
    ]

    for club in clubs:

        profit = club["sell"] - club["buy"]
        rate = profit / club["buy"] * 100

        if rate >= 10:
            st.success(f"{club['name']}  利益率 {round(rate,1)}%")
