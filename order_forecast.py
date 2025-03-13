# 🔒 비밀번호 보호 기능 (Streamlit Cloud의 secrets 사용)
PASSWORD = st.secrets["PASSWORD"]

password_input = st.text_input("비밀번호를 입력하세요:", type="password")
if password_input != PASSWORD:
    st.warning("비밀번호가 틀렸습니다! 😭")
    st.stop()  # 비밀번호가 맞지 않으면 코드 중단import pandas as pd
import numpy as np
import streamlit as st

def calculate_order(df):
    orders = []
    for _, row in df.iterrows():
        avg_3_days = (row['하루전 판매량'] + row['이틀전 판매량'] + row['삼일전 판매량']) / 3
        avg_7_days = row['일주일 판매량'] / 7
        daily_demand = (avg_3_days * 0.7) + (avg_7_days * 0.3)
        required_stock = max(0, (daily_demand * 2) - row['현재고'] - row['입고예정량'])
        order_qty = np.ceil(required_stock / row['입수단위']) * row['입수단위'] if required_stock > 0 else 0
        orders.append(int(order_qty))
    df['발주 수량'] = orders
    return df

st.title("📦 발주 예측 시스템")
st.write("숫자를 입력하면 자동으로 발주 수량을 계산해줍니다!")

num_rows = st.number_input("상품 개수 입력", min_value=1, max_value=50, value=5)

data = {
    '현재고': [],
    '입고예정량': [],
    '하루전 판매량': [],
    '이틀전 판매량': [],
    '삼일전 판매량': [],
    '일주일 판매량': [],
    '입수단위': []
}

for i in range(num_rows):
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        data['현재고'].append(st.number_input(f'현재고 {i+1}', min_value=0, value=0))
    with col2:
        data['입고예정량'].append(st.number_input(f'입고예정량 {i+1}', min_value=0, value=0))
    with col3:
        data['하루전 판매량'].append(st.number_input(f'하루전 판매량 {i+1}', min_value=0, value=0))
    with col4:
        data['이틀전 판매량'].append(st.number_input(f'이틀전 판매량 {i+1}', min_value=0, value=0))
    with col5:
        data['삼일전 판매량'].append(st.number_input(f'삼일전 판매량 {i+1}', min_value=0, value=0))
    with col6:
        data['일주일 판매량'].append(st.number_input(f'일주일 판매량 {i+1}', min_value=0, value=0))
    with col7:
        data['입수단위'].append(st.number_input(f'입수단위 {i+1}', min_value=1, value=1))

if st.button("🔍 발주 수량 계산"):
    df = pd.DataFrame(data)
    df = calculate_order(df)
    st.write("### 📊 계산된 발주 수량")
    st.dataframe(df)
