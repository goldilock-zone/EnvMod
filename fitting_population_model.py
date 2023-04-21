import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import math
import os
    
length_pred = 100
#Source of the function: https://www.studysmarter.co.uk/explanations/math/calculus/models-for-population-growth/

#Population data: https://data.worldbank.org/indicator/SP.POP.TOTL?locations=IN

#getting population data
df = pd.read_csv("PopulationData/pop.csv", on_bad_lines='skip')

x_array = [i for i in range(1960, 2022)]

y_array = []

for i in range(df.shape[0]):
    a = df.iloc[i]
    if a['Country Name'] == 'India':
        for j in x_array:
            y_array.append(a[str(j)])


#fitting
# define the true objective function
def objective(x, k, C):
    M = 200
    N = (M*C)/(C + math.e**((-k)*x))
    return N

# curve fit
x_train_array = [i for i in range(len(x_array))]
y_array = [y/10000000 for y in y_array]

parameters, covariance = curve_fit(objective, x_train_array, y_array)
k_est = parameters[0]
C_est = parameters[1]

fit_obj = [objective(i, k_est, C_est) for i in x_train_array]

plt.plot(x_array, y_array, 'o', label='data')
plt.plot(x_array, fit_obj, '-', label='fit')

pred = [objective(i, k_est, C_est) for i in range(x_train_array[-1], x_train_array[-1]+length_pred)]
x_extend = [i for i in range(x_array[-1], x_array[-1] + length_pred)]
plt.plot(x_extend, pred, '-', label='fit')

x_train = []
for i in range(len(x_array) + length_pred): 
    for j in range(12):
        x_train.append(i+(j/12))
y = [objective(i, k_est, C_est) for i in x_train]
x = [1960+x for x in x_train]

df_w = pd.DataFrame({
    'Year': x,
    'Population': y
})
try:
    os.remove('PopulationData/proj.csv')
except:
    print("There is no file")
finally:
    df_w.to_csv('PopulationData/proj.csv', index=False)
    
plt.show()