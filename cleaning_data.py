import pandas as pd
import numpy as np
from numpy import ones,vstack
from numpy.linalg import lstsq
import matplotlib.pyplot as plt
import os


def lineFromPoints(x, P, Q):
    points = [P,Q]
    x_coords, y_coords = zip(*points)
    A = vstack([x_coords,ones(len(x_coords))]).T
    m, c = lstsq(A, y_coords)[0]
    print("Line Solution is y = {m}x + {c}".format(m=m,c=c))
    return x*m + c

df = pd.read_csv("EnergyData/India_capacity_data.csv", on_bad_lines='skip')
useful_cols = ['YYYYMM', 'Hydro', 'Coal', 'Gas', 'Diesel', 'Nuclear', 'RES']
df = df[useful_cols]

dates = []
for year in range(1947, 2024):
    for month in range(12):
        dates.append(year*100+month+1)

check_list = list(df["YYYYMM"])
count = 0
first_val = True
interpol_init = [0,[]]
interpol_fin = [0,[]]
interpol_len = 0

final_df = pd.DataFrame(columns=useful_cols)
for index, date in enumerate(dates):

    foundflag = False
    for check in check_list:
        if int(date) == int(check):
            
            a = df.loc[count]
            add_row = [date] + [a[i] for i in useful_cols[1:]]
            final_df.loc[index] = add_row
            count += 1
            foundflag = True

            if first_val:
                interpol_init = [index,add_row]
                first_val = False
            else:
                interpol_fin = [index,add_row]
            break
    if foundflag:
        continue
    else:
        final_df.loc[index] = [date, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan] 

final_df.ffill(inplace=True)
final_df.dropna()
final_df['Total'] = final_df['Hydro'] + final_df['Coal'] + final_df['Gas'] + final_df['Diesel'] + final_df['Nuclear']  + final_df['RES']
final_df = final_df[11:-9]

plt.plot(final_df["YYYYMM"], final_df["Total"], '-', label='fit')
plt.show()

try:
    os.remove('PopulationData/energy.csv')
except:
    print("There is no file")
finally:
    final_df.to_csv('PopulationData/energy.csv', index=False)
