import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np


#метод зчитування даних з файла
def getFile(path):
    data = pd.read_csv(path, sep=',')
    return (data)

# зчитування необхідних даних та виправлення помилок
table = getFile("C:\\Users\\lenovo\\pythonLabs\\PacMan-1\\statistics.csv")
table = table.replace({True:1})
table = table.replace({False:0})
table = table.replace({"expectimax":0})
table = table.replace({"minimax":1})

table["time"] = pd.to_timedelta(table['time']).dt.total_seconds()

maxScore = table.loc[table['status'] == 1]['score'].max()
print(maxScore)

#інформація про дані
count = len(table)
factorNames = ['time', 'algorythm']
X = table[['time','algorythm']]
Y = table['score']
x_train, x_test, y_train, y_test = train_test_split(X,np.array(Y),test_size=0.25,shuffle=True)
model = LinearRegression().fit(x_train, y_train)

y_pred = model.predict(x_test)

plt.figure()
plt.plot(range(0, 300),range(0, 300))
plt.scatter(y_test,y_pred)
plt.show()

linearModel = LinearRegression().fit(X, Y)

a1,a2 = linearModel.coef_

print("Коефіцієнт впливу часу: "+ str(a1))
print("Коефіцієнт впливу алгоритму: "+str(a2))

for item in range(len(table)-5,len(table)):
    time, alg, score = table["time"][item], table["algorythm"][item], table["score"][item]
    predScore = linearModel.predict([[time, alg]])
    if(predScore > maxScore) : predScore = maxScore
    print("For time: {0} and algorythm: {1} predicted score is: {2}, when real is: {3}".format(time, alg, predScore, score))

# newTable =  table.groupby(table['algorythm']).count()
# newTable1 =  table.loc[table['status'] == 1].groupby(table['algorythm']).count()
# print(newTable)
# print(newTable1)