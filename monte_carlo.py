import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

energy_parts = ['Hydro', 'Coal', 'Gas', 'Diesel', 'Nuclear', 'RES']
carbon_footprint = {
    'Hydro':2,
    'Coal':3,
    'Gas':4,
    'Diesel':5,
    'Nuclear':6,
    'RES':0
}

#energy_mix
df_en = pd.read_csv("PopulationData/energy.csv", on_bad_lines='skip')
a = df_en.iloc[df_en.shape[0]-1]
energylevels = {
    'Hydro': a['Hydro'],
    'Coal':a['Coal'],
    'Gas':a['Gas'],
    'Diesel':a['Diesel'],
    'Nuclear':a['Nuclear'],
    'RES':a['RES']
}

energymix = {
    'Hydro': a['Hydro']/a["Total"],
    'Coal':a['Coal']/a["Total"],
    'Gas':a['Gas']/a["Total"],
    'Diesel':a['Diesel']/a["Total"],
    'Nuclear':a['Nuclear']/a["Total"],
    'RES':a['RES']/a["Total"]
}

implied_growth = {}
impl_growth_df = df_en[-10*12:]

for col in energy_parts:
    series = impl_growth_df[col]
    pct = np.mean(series.pct_change())
    implied_growth[col] = pct

variable_mov = ['Hydro', 0.02/12]

energy_df = pd.read_csv("PopulationData/energy_proj.csv", on_bad_lines='skip')
energy_df["Growth"] = energy_df['Energy'].pct_change()

def sim(variable_mov, energy_df, energylevels, implied_growth):
    sim_df = energy_df[energy_df["Year"] > (2023.25)]

    projection_limit = 20*12
    current_level = energylevels[variable_mov[0]]
    above_trend_growth = implied_growth[variable_mov[0]] + variable_mov[1]

    simulation = pd.DataFrame(columns = ['Hydro', 'Coal', 'Gas', 'Diesel', 'Nuclear', 'RES', 'Total'])

    rest_list = []
    for i in energy_parts:
        if i == variable_mov[0]:
            continue
        else:
            rest_list.append(i)

    prop_sum = 0
    for part in rest_list:
        prop_sum += energylevels[part]

    prop = {}
    for part in rest_list:
        prop[part] = energylevels[part]/prop_sum

    for i in range(projection_limit):
        total_energy = sim_df.iloc[i]["Energy"]
        increased_amt = current_level*((1+above_trend_growth)**i)
        rest_amt = total_energy - increased_amt
        simulation.loc[i,variable_mov[0]] = increased_amt
        for part in rest_list:
            if rest_amt*prop[part] > 0:
                simulation.loc[i,part] = rest_amt*prop[part]
            else: 
                simulation.loc[i,part] = 0

        simulation.loc[i,"Total"] = simulation.loc[i,"Hydro"] + simulation.loc[i,"Coal"] + simulation.loc[i,"Gas"] + simulation.loc[i,"Diesel"] + simulation.loc[i,"Nuclear"] + simulation.loc[i,"RES"]

    ax = plt.gca()
    simulation.plot(kind = 'line', y = 'Total',ax=ax)
    simulation.plot(kind = 'line', y = 'Hydro',ax=ax)
    simulation.plot(kind = 'line', y = 'Coal',ax=ax)
    simulation.plot(kind = 'line', y = 'Gas',ax=ax)
    simulation.plot(kind = 'line', y = 'Nuclear',ax=ax)
    simulation.plot(kind = 'line', y = 'RES',ax=ax)
    
    filename = f"{variable_mov[0]} {variable_mov[1]}"
    plt.savefig(f'Simulations/{filename}.png')
    plt.clf()

sim_dict = {
    'Hydro':[(i/100)/12 for i in range(-10,10)],
    'Coal':[(i/100)/12 for i in range(-10,10)],
    'Gas':[(i/100)/12 for i in range(-10,10)],
    'Diesel':[(i/100)/12 for i in range(-10,10)],
    'Nuclear':[(i/100)/12 for i in range(-10,10)],
    'RES':[(i/100)/12 for i in range(-10,10)]
}

for part, ls in sim_dict.items():
    for grwth in ls:
        variable_mov = [part, grwth]
        sim(variable_mov, energy_df, energylevels, implied_growth)
