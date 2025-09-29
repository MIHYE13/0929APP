import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 한글 폰트 설정 (NanumGothic)
font_path = "./fonts/nanumgothic-regular.ttf"
font_manager.fontManager.addfont(font_path)
plt.rc('font', family='NanumGothic')

# Streamlit 페이지 설정
st.set_page_config(page_title="대한민국 지역별 강수량 지도", layout="wide")

st.title("대한민국 지역별 강수량 지도")
st.markdown("""
이 웹앱은 대한민국의 지역별 강수량 데이터를 지도 위에 시각화합니다.
""")

# 샘플 강수량 데이터
data = {
    "지역": ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종", "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"],
    "강수량(mm)": [120, 150, 110, 130, 140, 115, 125, 100, 135, 160, 105, 120, 110, 145, 115, 130, 200],
    "위도": [37.5665, 35.1796, 35.8714, 37.4563, 35.1595, 36.3504, 35.5384, 36.4800, 37.4138, 37.8228, 36.6357, 36.6588, 35.8200, 34.8161, 36.4919, 35.2384, 33.4996],
    "경도": [126.9780, 129.0756, 128.6014, 126.7052, 126.8526, 127.3845, 129.3114, 127.2890, 127.5183, 128.1555, 127.4913, 126.6728, 127.1088, 126.4630, 128.8889, 128.6922, 126.5312]
}
df = pd.DataFrame(data)

# --- 사이드바 필터 ---
st.sidebar.header("강수량 범위 필터")

min_val = int(df["강수량(mm)"].min())
max_val = int(df["강수량(mm)"].max())

min_rain, max_rain = st.sidebar.slider(
    "강수량(mm) 범위 선택",
    min_val,
    max_val,
    (min_val, max_val)
)

# 필터링된 데이터프레임
filtered_df = df[(df["강수량(mm)"] >= min_rain) & (df["강수량(mm)"] <= max_rain)]

# --- 데이터 시각화 섹션 ---
st.subheader("지역별 강수량 데이터")
st.dataframe(filtered_df, use_container_width=True)

# 한글 폰트가 적용된 막대 차트
st.subheader("지역별 강수량 막대 차트")
if not filtered_df.empty:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(filtered_df["지역"], filtered_df["강수량(mm)"], color='skyblue')
    ax.set_xlabel("지역", fontsize=12)
    ax.set_ylabel("강수량(mm)", fontsize=12)
    ax.set_title("지역별 강수량 비교", fontsize=14)
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.info("선택된 강수량 범위에 해당하는 지역 데이터가 없습니다.")

st.markdown("---")

# --- 지도 생성 및 시각화 ---
st.subheader("대한민국 지도에서 강수량 시각화")

# 지도 생성
m = folium.Map(location=[36.5, 127.8], zoom_start=7)

# 필터링된 데이터 기반으로 지도에 원형 마커 추가
for idx, row in filtered_df.iterrows():
    folium.CircleMarker(
        location=[row["위도"], row["경도"]],
        radius=max(row["강수량(mm)"] / 15, 5),
        popup=f"{row['지역']}: {row['강수량(mm)']}mm",
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.6
    ).add_to(m)

st_folium(m, width=900, height=600)