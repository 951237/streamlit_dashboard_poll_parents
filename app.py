import pandas as pd

# data.csv 파일구조(칼럼)
'''
col0 : 시간, 	col1 : 참관여부, 	col2 : 학년, 
col3 : 반, 		col4: 만족도, 		col5:학부모 의견
'''


# 데이터 불러오기
df = pd.read_csv("data.csv")

# 학년별 만족도 
grouped_grade = df.groupby(df.columns[2]).mean()

# 학급별 만족도
grouped_classes = df.groupby(df.columns[3]).mean()
