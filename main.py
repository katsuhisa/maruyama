import pandas as pd
# import matplotlib.pyplot as plt
# import yfinance as yf
import yahoo_finance_api2 as yf
from yahoo_finance_api2 import share
# %matplotlib inline
import altair as alt
import streamlit as st

st.title('米国株価可視化アプリ')

st.sidebar.write("""
# GAFA株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")
# =================================
st.sidebar.write("""
## 表示日数選択
""")
days = st.sidebar.slider('日数', 1, 50, 20)

st.write(f"""
### 過去 **{days}日間** のGAFA株価
""")
try: 
    # =================================
    st.sidebar.write("""
    ## 株価の範囲指定
    """)
    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください。',
        0.0, 3500.0, (0.0, 1000.0) # 範囲最小値,範囲最大値(デフォルト最小値,デフォルト最大値)
    )
    # =================================
    # 取得データの会社名（ティッカー）リスト
    tickers = {
        'apple': 'AAPL',
        'facebook': 'FB',
        'google': 'GOOGL',
        'microsoft': 'MSFT',
        'netflix': 'NFLX',
        'amazon': 'AMZN'
    }
    # =================================
    @st.cache # 毎回データを取得すると面倒なため、Cacheにためておく。読取速度向上

    def get_data(days, tickers):
        df = pd.DataFrame()
        for company in tickers.keys():
            # 株式データ取得
            tkr = share.Share(tickers[company])# ティッカーシンボルを指定
            hist = None
            hist = tkr.get_historical(
                    share.PERIOD_TYPE_DAY, days,
                    share.FREQUENCY_TYPE_DAY, 1
                    )
            hist = pd.DataFrame(hist)# データフレーム型に変換
            # 日付列（Date）を作成し、データフレームを整形
            hist["Date"] = pd.to_datetime(hist.timestamp, unit="ms")
            hist["Date"] = hist["Date"].dt.date # 日付のみ取得
            hist['Date'] = pd.to_datetime(hist['Date']) # datetime64[ns]型に変換
            hist = hist.drop("timestamp",axis=1)
            hist = hist.reindex(columns=['Date', 'open', 'high', 'low', 'close', 'volume'])
            hist = hist.set_index('Date')# 日付列（Date）をIndex化

            hist.index = hist.index.strftime('%d %B %Y') # IndexであるDate列の日付表示方法を変更
            hist = hist[['close']] # close列のデータのみ使用し、列名を社名に
            hist.columns = [company]
            hist = hist.T
            hist.index.name = 'Company'
            df = pd.concat([df,hist])
        return df
    df = get_data(days, tickers)
    # =================================
    companies = st.multiselect(
            '会社名を選択してください。',
            list(df.index), # データのインデックスをリスト化。それが選択肢
            ['google', 'amazon', 'facebook', 'apple'] # デフォルト
        )
    # =================================
    # グラフ描写
    if not companies:
        st.error('少なくとも一社は選んでください。')
    else:
        data = df.loc[companies]
        st.write("""株価(USD)""",data.sort_index())
        # グラフ用にデータ整形
        data = data.T.reset_index()
        # Date列を基準にデータフレームをアンピボット
        data = pd.melt(data, id_vars=['Date']) 
        # 列名変更
        data = data.rename(columns={'value': 'Stock Prices(USD)'})
        # グラフ描写
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True) # 折れ線グラフ（opacity：透明度、clip=True:グラフ範囲外のデータは除外）
            .encode(
                x="Date:T", # Timeを意味
                y=alt.Y("Stock Prices(USD):Q", # "Stock Prices(USD):Q"の「:Q」は定量化を意味
                        stack=None, 
                        scale=alt.Scale(domain=[ymin, ymax])), # scale=alt.Scale:グラフの表示範囲指定
                color='Company:N'
            )
        )
        st.altair_chart(chart, use_container_width=True) # use_container_width=True: 画面の横幅いっぱいに表示
except:
    st.error(
        "エラーが起きているようです。"
    )

    
# # from random import randint
# import streamlit as st
# import numpy as np
# import pandas as pd
# # import random as rand

# # 文字列を表示
# st.title('Streamlit 入門')
# st.write('DataFrame')

# # ----------------------------
# # 表を表示
# df = pd.DataFrame({
#     '1列目': [1,2,3,4],
#     '2列目': [10,20,30,40]
# })
# st.write(df) # 動的グラフ
# # st.dataframe(df.style,width=100,height=100) # 縦・横の長さを指定可能。動的グラフ
# # st.dataframe(df.style.hightlight_max(axis=0)) # 各行で最大の値をハイライト。動的グラフ
# st.table(df) # 静的グラフ。ソートなど出来ない。

# # ----------------------------
# # グラフを表示
# df = pd.DataFrame(
#     np.random.rand(20,3),
#     columns=['a','b','c']
# )
# st.line_chart(df) # 折れ線グラフ
# st.area_chart(df) # 面グラフ
# st.bar_chart(df) # 棒グラフ

# # ----------------------------
# # 地図を表示
# df = pd.DataFrame(
#     np.random.rand(100,2)/[50,50] + [35.69,139.70], # 新宿周辺の緯度・経度の点を地図にプロット
#     columns=['lat','lon']
# )
# st.map(df) # Map上に点をプロット。

# # # ----------------------------
# # # 画像を表示
# from PIL import Image
# # img = Image.open('Profile.jpg')
# # st.image(img, caption='Katsuhisa Deto', use_column_width=True) # use_column_width：アプリのレイアウトの横幅に併せて表示

# # ----------------------------
# # ----------------------------
# # インタラクティブなウィジェット(UI)
# # ----------------------------
# # チェックボックス
# if st.checkbox('Show Image'):
#     img = Image.open('Profile.jpg')
#     st.image(img, caption='Katsuhisa Deto', use_column_width=True) # use_column_width：アプリのレイアウトの横幅に併せて表示

# # ----------------------------
# # セレクトボックス
# option = st.selectbox(
#     'あなたの好きな数字を入力してください。',
#     list(range(1,11))
# )
# 'あなたの好きな数字は、', option, 'です。'

# # # ----------------------------
# # # テキスト入力
# # hobby = st.text_input('あなたの趣味を教えてください。')
# # 'あなたの趣味：',hobby,'です。'

# # # ----------------------------
# # # スライド
# # condition = st.slider('あなたの今の調子は？',0,100,50)
# # 'あなたのコンディション：', condition

# # ----------------------------
# # サイドバー
# # ----------------------------
# # テキスト入力
# hobby = st.sidebar.text_input('あなたの趣味を教えてください。')
# 'あなたの趣味：',hobby,'です。'

# # ----------------------------
# # スライド
# condition = st.sidebar.slider('あなたの今の調子は？',0,100,50)
# 'あなたのコンディション：', condition

# # ----------------------------
# # 画面分割
# # ----------------------------
# left_column, right_column = st.columns(2)
# # button = left_column('右カラムに文字を表示') # 左カラムの入力内容
# # コンテキストマネージャとして使う
# with right_column:
#     st.header('right_column')
#     right_column.write('ここは右カラム')
# # ----------------------------
# # プルダウン
# expander1 = st.expander('問い合わせ1')
# expander1.write('問い合わせ1の回答')
# expander2 = st.expander('問い合わせ2')
# expander2.write('問い合わせ2の回答')
# expander3 = st.expander('問い合わせ3')
# expander3.write('問い合わせ3の回答')
# # ----------------------------
# # プログレスバーの表示
# # ----------------------------
# 'Start!!'
# latest_iteration = st.empty()
# bar = st.progress(0)

# import time
# for i in range(100):
#     latest_iteration.text(f'Iteration {i+1}')
#     bar.progress(i+1)
#     time.sleep(0.1)

# 'DONE'