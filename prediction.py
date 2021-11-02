from sys import winver
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

df = pd.read_csv('data.csv')
df.columns = ['hp', 'score', 'time', 'result']
print(df.head())
df, test_data = df.iloc[:-5], df.iloc[-5:]

x1 = df.loc[:, ['hp', 'time']]
x2 = df.loc[:, ['hp', 'score']]
x3 = df.loc[:, ['score', 'time']]
y1 = df.loc[:, ['score']]
y2 = df.loc[:, ['time']]
y3 = df.loc[:, ['hp']]
print(x1.head())
print(y1.head())
LR_score = LinearRegression()
LR_time = LinearRegression()
LR_hp = LinearRegression()
LR_score.fit(x1, y1)
LR_time.fit(x2, y2)
LR_hp.fit(x3, y3)
predict_score = LR_score.predict(test_data.loc[:, ['hp', 'time']])
predict_hp = LR_score.predict(test_data.loc[:, ['score', 'time']])
predict_time = LR_score.predict(test_data.loc[:, ['hp', 'score']])
result = []
for i in predict_hp:
    if i > 0:
        result.append('win')
    else:
        result.append('lose')
for i in range(len(predict_time)):
    predict_time[i] = int(predict_time[i]/100)
    predict_hp[i] = int(predict_hp[i])
    predict_score[i] = int(predict_score[i])
predicted_games = pd.DataFrame(np.hstack(
    (predict_hp, predict_score, predict_time)))
predicted_games[4] = pd.Series(result)
df.to_csv("data2.csv", mode='w', index=False, header=False)
predicted_games.to_csv("data2.csv", mode='a', index=False, header=False)
print(predicted_games)
print(test_data)
