# from random import randint
import streamlit as st
import numpy as np
import pandas as pd
# import random as rand

# 文字列を表示
st.title('Streamlit 入門')
st.write('DataFrame')

# ----------------------------
# 表を表示
df = pd.DataFrame({
    '1列目': [1,2,3,4],
    '2列目': [10,20,30,40]
})
st.write(df) # 動的グラフ
# st.dataframe(df.style,width=100,height=100) # 縦・横の長さを指定可能。動的グラフ
# st.dataframe(df.style.hightlight_max(axis=0)) # 各行で最大の値をハイライト。動的グラフ
st.table(df) # 静的グラフ。ソートなど出来ない。

# ----------------------------
# グラフを表示
df = pd.DataFrame(
    np.random.rand(20,3),
    columns=['a','b','c']
)
st.line_chart(df) # 折れ線グラフ
st.area_chart(df) # 面グラフ
st.bar_chart(df) # 棒グラフ

# ----------------------------
# 地図を表示
df = pd.DataFrame(
    np.random.rand(100,2)/[50,50] + [35.69,139.70], # 新宿周辺の緯度・経度の点を地図にプロット
    columns=['lat','lon']
)
st.map(df) # Map上に点をプロット。

# # ----------------------------
# # 画像を表示
from PIL import Image
# img = Image.open('Profile.jpg')
# st.image(img, caption='Katsuhisa Deto', use_column_width=True) # use_column_width：アプリのレイアウトの横幅に併せて表示

# ----------------------------
# ----------------------------
# インタラクティブなウィジェット(UI)
# ----------------------------
# チェックボックス
if st.checkbox('Show Image'):
    img = Image.open('Profile.jpg')
    st.image(img, caption='Katsuhisa Deto', use_column_width=True) # use_column_width：アプリのレイアウトの横幅に併せて表示

# ----------------------------
# セレクトボックス
option = st.selectbox(
    'あなたの好きな数字を入力してください。',
    list(range(1,11))
)
'あなたの好きな数字は、', option, 'です。'

# # ----------------------------
# # テキスト入力
# hobby = st.text_input('あなたの趣味を教えてください。')
# 'あなたの趣味：',hobby,'です。'

# # ----------------------------
# # スライド
# condition = st.slider('あなたの今の調子は？',0,100,50)
# 'あなたのコンディション：', condition

# ----------------------------
# サイドバー
# ----------------------------
# テキスト入力
hobby = st.sidebar.text_input('あなたの趣味を教えてください。')
'あなたの趣味：',hobby,'です。'

# ----------------------------
# スライド
condition = st.sidebar.slider('あなたの今の調子は？',0,100,50)
'あなたのコンディション：', condition

# ----------------------------
# 画面分割
# ----------------------------
left_column, right_column = st.columns(2)
# button = left_column('右カラムに文字を表示') # 左カラムの入力内容
# コンテキストマネージャとして使う
with right_column:
    st.header('right_column')
    right_column.write('ここは右カラム')
# ----------------------------
# プルダウン
expander1 = st.expander('問い合わせ1')
expander1.write('問い合わせ1の回答')
expander2 = st.expander('問い合わせ2')
expander2.write('問い合わせ2の回答')
expander3 = st.expander('問い合わせ3')
expander3.write('問い合わせ3の回答')
# ----------------------------
# プログレスバーの表示
# ----------------------------
'Start!!'
latest_iteration = st.empty()
bar = st.progress(0)

import time
for i in range(100):
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i+1)
    time.sleep(0.1)

'DONE'