# Streamlit 모든 기능 데모
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

st.set_page_config(
	page_title="Streamlit 모든 기능 데모",
	page_icon="🌈",
	layout="wide"
)

st.title("Streamlit 모든 기능 데모")
st.markdown("""
이 페이지는 Streamlit의 다양한 기능을 한눈에 볼 수 있도록 구성되었습니다.
""")

# 컬럼 레이아웃
col1, col2 = st.columns(2)
with col1:
	st.header("텍스트 및 마크다운")
	st.write("일반 텍스트 출력")
	st.markdown("**마크다운** 지원 :star:")
	st.code("print('Hello Streamlit!')", language='python')
	st.caption("캡션 예시")
	st.latex(r"E = mc^2")

with col2:
	st.header("알림 및 상태 표시")
	st.success("성공 메시지")
	st.info("정보 메시지")
	st.warning("경고 메시지")
	st.error("에러 메시지")

# 데이터 예시
st.header("데이터 표시")
data = {
	'국가': ['한국', '미국', '일본', '독일', '영국'],
	'GDP': [1800, 21000, 5000, 4000, 2800],
	'인구(백만)': [51, 331, 126, 83, 67]
}
df = pd.DataFrame(data)
st.dataframe(df)
st.table(df)

# 차트 예시
st.header("차트 및 시각화")
chart_data = pd.DataFrame(
	np.random.randn(20, 3),
	columns=['A', 'B', 'C']
)
st.line_chart(chart_data)
st.bar_chart(chart_data)
st.area_chart(chart_data)

# 입력 위젯
st.header("입력 위젯")
name = st.text_input("이름을 입력하세요:")
age = st.slider("나이", 0, 100, 25)
gender = st.radio("성별", ["남성", "여성", "기타"])
agree = st.checkbox("개인정보 제공에 동의합니다.")
if name and agree:
	st.success(f"안녕하세요, {name}님! 나이: {age}, 성별: {gender}")

# 파일 업로드
st.header("파일 업로드 및 이미지 표시")
uploaded_file = st.file_uploader("이미지 파일을 업로드하세요.", type=["png", "jpg", "jpeg"])
if uploaded_file:
	img = Image.open(uploaded_file)
	st.image(img, caption="업로드한 이미지", use_column_width=True)

# 확장 레이아웃
with st.expander("추가 정보 펼치기"):
	st.write("이곳에 추가 설명이나 정보를 넣을 수 있습니다.")

# 사이드바
st.sidebar.header("사이드바")
option = st.sidebar.selectbox(
	"좋아하는 국가를 선택하세요:",
	df['국가']
)
st.sidebar.write(f"선택한 국가: {option}")
st.sidebar.slider("사이드바 슬라이더", 0, 100, 50)
