import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
from numpy import polyfit
import os

df_pop = pd.read_csv("PopulationData/proj.csv", on_bad_lines='skip')
df_en = pd.read_csv("PopulationData/energy.csv", on_bad_lines='skip')

#finding index for 1960
index = 0
for i in range(df_en.shape[0]):
    index += 1 
    if int(df_en.loc[i,'YYYYMM']) == 196001:
        break
regress_df_en = df_en[index-1:]
regress_pop_df = df_pop[:regress_df_en.shape[0]]
pred_pop_df = df_pop[regress_df_en.shape[0]:]

x = regress_pop_df["Population"]
y = regress_df_en["Total"]

res = polyfit(x, y, deg = 2)

def pred_func(x, two_coeff, one_coeff, intercept, continuity_correction):
    return two_coeff*x*x + x*one_coeff + intercept + continuity_correction

proj_pop = list(pred_pop_df["Population"])
cc = list(regress_df_en["Total"])[-1] - pred_func(proj_pop[0], res[0], res[1], res[2], 0)
pred = list(regress_df_en["Total"]) + [pred_func(pop, res[0], res[1], res[2], cc) for pop in proj_pop]
date_array = df_pop['Year']

part = 63*12
#plot1
dtpt1 = date_array[:part]
pred1 = pred[:part]
plt.plot(dtpt1, pred1, '-', label='data', color = 'red')
#plot2
dtpt2 = date_array[part:]
pred2 = pred[part:]
plt.plot(dtpt2, pred2, '-', label='data', color = 'green')

out_df = pd.DataFrame(
    {
        "Year": date_array,
        "Energy": pred
    }
)

try:
    os.remove('PopulationData/energy_proj.csv')
except:
    print("There is no file")
finally:
    out_df.to_csv('PopulationData/energy_proj.csv', index=False)

plt.show()
