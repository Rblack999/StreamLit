import pandas as pd

x = [1,2,3,4,5,8,20,30]
y = [4,5,6,7,1,5,30,0]
data = {'Data1':x, 'Data3':y}


df = pd.DataFrame(data)

df.to_csv('Test.csv')