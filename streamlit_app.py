import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Streamlit 페이지 설정
st.set_page_config(page_title="대한민국 지역별 강수량 지도 및 비교", layout="wide")

st.title("대한민국 지역별 강수량 지도 및 비교")
st.markdown("""
이 웹앱은 대한민국의 지역별 강수량 데이터를 지도 위에 시각화하고 막대 차트로 비교합니다.
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
col1, col2 = st.columns(2)

with col1:
    st.subheader("지역별 강수량 데이터")
    st.dataframe(filtered_df, use_container_width=True)

with col2:
    st.subheader("지역별 강수량 막대 차트")
    if not filtered_df.empty:
        chart_data = filtered_df.set_index('지역')['강수량(mm)']
        st.bar_chart(chart_data)
    else:
        st.info("선택된 강수량 범위에 해당하는 지역 데이터가 없습니다.")

st.markdown("---")

# --- 지도 생성 및 시각화 ---
st.subheader("대한민국 지도에서 강수량 시각화")

# 지도 생성
m = folium.Map(location=[36.5, 127.8], zoom_start=7)

# 필터링된 데이터 기반으로 지도에 원형 마커 추가
for idx, row in filtered_df.iterrows():
    radius = max(row["강수량(mm)"] / 15, 5)
    
    folium.CircleMarker(
        location=[row["위도"], row["경도"]],
        radius=radius,
        popup=f"**{row['지역']}**: {row['강수량(mm)']}mm",
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.6
    ).add_to(m)

st_folium(m, width=900, height=600)

st.markdown("---")

# --- 질문 및 답변 섹션 (새로 추가됨) ---

st.header("🌦️ 강수량 데이터 관련 질문 및 피드백")
st.markdown("앱에 대해 궁금한 점이나 의견을 남겨주세요.")

# 질문 리스트 정의
questions = [
    "1. 슬라이더를 조정했을 때 지도 마커 크기도 동적으로 변하는 것이 만족스러운가요?",
    "2. 현재 강수량 데이터의 단위(mm)가 명확하게 이해되나요?",
    "3. 차트와 지도를 함께 보여주는 구성이 강수량 비교에 효과적인가요?",
    "4. 추가했으면 하는 데이터(예: 온도, 습도 등)가 있다면 무엇인가요?",
    "5. 앱 사용 중 불편했던 점이나 개선할 부분이 있다면 알려주세요."
]

# 세션 상태 초기화: 답변을 저장하기 위해 사용
if 'answers' not in st.session_state:
    st.session_state.answers = {f'q{i+1}': "" for i in range(len(questions))}

# 답변 입력 박스 생성 함수
def update_answer(question_key):
    # Textarea의 현재 값을 세션 상태에 저장
    st.session_state.answers[question_key] = st.session_state[question_key]

# 각 질문에 대한 입력 박스 생성
with st.container(border=True):
    for i, q in enumerate(questions):
        q_key = f'q{i+1}'
        st.subheader(f"❓ {q}")
        st.text_area(
            "답변을 입력하세요.",
            key=q_key, # 이 키를 사용하여 입력 값에 접근
            value=st.session_state.answers[q_key], # 세션 상태에 저장된 값을 표시
            on_change=update_answer, # 값이 변경될 때마다 세션 상태 업데이트 함수 호출
            args=(q_key,), # on_change 함수에 전달할 인자
            placeholder="여기에 답변을 입력해 주세요."
        )
        st.markdown("---")

# (선택 사항) 저장된 답변을 확인하는 버튼 (디버깅/확인용)
if st.button("제출된 답변 확인 (개발자용)"):
    st.json(st.session_state.answers)