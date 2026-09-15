import streamlit as st
import pandas as pd

# 앱 기본 설정
st.set_page_config(
    page_title="서울 100년 기온 변화",
    page_icon="🌡️",
    layout="centered"
)

@st.cache_data
def load_data():
    """
    GitHub에 있는 서울 기온 데이터를 불러옵니다.
    한글 인코딩 문제(utf-8 vs cp949)를 방지하기 위해 예외 처리를 추가했습니다.
    """
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"
    try:
        df = pd.read_csv(url, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(url, encoding='cp949')
    
    return df

def preprocess_data(df):
    """
    데이터를 분석하기 좋게 가공합니다.
    """
    # 평균기온 데이터가 없는 행(결측치) 제거
    df = df.dropna(subset=['평균기온(℃)']).copy()
    
    # '날짜' 열을 문자열에서 날짜(datetime) 형식으로 변환
    df['날짜'] = pd.to_datetime(df['날짜'])
    
    # 날짜에서 '연도'만 추출하여 새로운 열 생성
    df['연도'] = df['날짜'].dt.year
    
    # 연도별로 그룹을 묶어서 평균기온의 평균을 계산
    yearly_avg = df.groupby('연도')['평균기온(℃)'].mean()
    
    return yearly_avg

def main():
    # 제목 및 설명
    st.title("🌡️ 서울의 100년 기온 변화")
    st.markdown("과거 100년이 넘는 시간 동안 **서울의 연평균 기온**이 어떻게 변해왔는지 한눈에 확인해 보세요.")

    # 데이터 로딩 상태 표시
    with st.spinner('데이터를 불러오고 분석하는 중입니다...'):
        raw_df = load_data()
        yearly_data = preprocess_data(raw_df)

    # 1. 꺾은선 그래프 그리기
    st.subheader("📈 연평균 기온 변화 그래프")
    st.write("그래프에 마우스를 올리면 정확한 연도와 기온을 확인할 수 있습니다.")
    # 스트림릿 내장 차트를 사용하여 한글 깨짐 없이 예쁘게 렌더링
    st.line_chart(yearly_data, color="#FF4B4B")

    # 2. 데이터프레임(표)으로 확인하기
    st.subheader("📊 연도별 기온 데이터")
    # 인덱스(연도)를 열로 꺼내어 보기 좋게 만듦
    display_df = yearly_data.reset_index()
    display_df.columns = ['연도', '연평균 기온(℃)']
    
    # 소수점 둘째 자리까지 표시
    display_df['연평균 기온(℃)'] = display_df['연평균 기온(℃)'].round(2)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True # 불필요한 기본 인덱스 숨김
    )

    # 3. 출처 표기
    st.caption("데이터 출처: 기상청 / Github (@greatsong)")

if __name__ == "__main__":
    main()
