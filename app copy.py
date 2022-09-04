import pandas as pd
import plotly.express as px
import streamlit as st
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
from konlpy.tag import Kkma
from wordcloud import WordCloud

# data.csv 파일구조(칼럼이름)
	# col0 : 시간, 	col1 : 참관여부, 	col2 : 학년, 
	# col3 : 반, 		col4: 만족도, 		col5:학부모 의견

# streamlit 페이지 생성
st.set_page_config(
    page_title='학부모공개수업 설문결과 대시보드',		# 브라우저 탭 제목
    page_icon = ":bar_chart:",							# 브라우저 파비콘
    layout = "wide"										# 레이아웃
    )

# csv 파일 불러오기
def get_csvfile():
	# 데이터 불러오기
	df = pd.read_csv("data.csv")

	# 데이터 전처리
	df = df.dropna(subset=['학년']) 	# 학년 빈칸인 줄 삭제
	df['만족도'] = df['만족도'].map(lambda x: int(x))	# 만족도 정수로 표시
	df['학년'] = df['학년'].map(lambda x: x[0])		# 5학년 → 5 '학년'글자 삭제
	df['반'] = df['반'].map(lambda x: x[0])			# 3반 → 3 	'반'글자 삭제
	df['학년반'] = df['학년'] + df['반']

	return df

# 워드클라우드 말뭉치 만들기
def make_worcloud(df):
	df_wordcloud = df.dropna(subset=['학부모 의견'])
	lst_lines = list(df_wordcloud['학부모 의견'])
    
	line = " ".join(lst_lines)
 
	okt = Okt()
	line = okt.pos(line)

	# 명사 또는 형용사인 단어만 리스트에 담기
	lst_result = []

	for word, tag in line:
		if tag in ['Noun', 'Adjective']:
			lst_result.append(word)
	# 제외할 단어 추가
	my_stopwords = '비 더 도도 도 명 것 날 때  명 수 보 그 분 그 알 비 시 마 만 못 늘'
	my_stopwords = set(my_stopwords.split(' '))
 
	# 불용어를 제외한 단어만 남기기
	lst_result = [word for word in lst_result if not word in my_stopwords]
	
 	#가장 많이 나온 단어 100개 저장
	counts = Counter(lst_result)
	# print(counts,'\n'*3)

	tags = counts.most_common(100)
	tags = dict(tags)
 
	font="AppleGothic"
	word_cloud = WordCloud(
		font_path = font,
		background_color="white",
		width = 1000,
		height = 1000,
		max_font_size=300
	)
 
	word_cloud = word_cloud.generate_from_frequencies(tags)
	return word_cloud
 
df = get_csvfile()		# 데이터 프레임 생성

# --- 사이드바 생성하기 --- 
st.sidebar.header("Please Filter Hear: ")

# 학년 선택
grade = st.sidebar.multiselect(
	"Select the Grade:",
	options = df['학년'].unique(),
	default = df['학년'].unique()
)

# 학급 선택
class_num = st.sidebar.multiselect(
	"Select the Class_num:",
	options = df['반'].unique(),
	default = df['반'].unique()
)

# 데이터 프레임 칼럼 이름으로 설정하기
df_selection = df.query(
	"학년 == @grade & 반 == @class_num"		# '학년'은 데이터프레임 칼럼
)


# --- 메인 페이지 ---
st.title(":bar_chart: 학부모공개수업 설문 현황판")		# 화면 타이틀
st.markdown("##")		# 마크다운 문법 가능

# 상단 현황판
total_response = int(len(df_selection['학년']))

st.subheader(f"전체 응답수 : 총 {total_response}명")
st.markdown("---")

# st.dataframe(df_selection)		# 페이지에 데이터프레임 표시하기


# 만족도 현황
grouped_score = (
	df_selection.groupby('만족도').size().reset_index()
)
grouped_score.columns = ['만족도', '인원']

fig_grouped_score = px.bar(
	grouped_score,
	x = '만족도',
	y = '인원',
	title = "<b>만족도 현황</b>",
	# color = 'country',
	color_discrete_sequence=["#0083B8"] * len(grouped_score),
	template="plotly_white"
)

st.plotly_chart(fig_grouped_score)

# 워드클라우드
word_cloud = make_worcloud(df_selection)

fig = plt.figure()
# plt.title('학부모 응답 워드클라우드')
plt.imshow(word_cloud, interpolation="bilinear")
plt.axis("off")
plt.show()
st.pyplot(fig)



