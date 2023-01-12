# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

df_run = pd.read_csv('experiments/16.csv')
df_run = df_run.rename(
    columns={'rotation number': 'n', 'time after start [s]': 't'})
df_run.drop(df_run.tail(1).index, inplace=True)
df_run['dt'] = df_run['t'] - df_run['t'].shift(1)
df_run = df_run[df_run['dt'] > 0.01]

# Omregn måledata til en tidserie med vinkelhastighedsværdier
df_run['dt'] = df_run['t'] - df_run['t'].shift(1)
df_run['w'] = 2*math.pi/df_run['dt']
df_run['dw'] = df_run['w'] - df_run['w'].shift(1)
df_1 = df_run[df_run['dw'] > 0]
df_2 = df_run[df_run['dw'] < 0]
df_2['dw'] = df_2['dw'] * -1
df_run.reset_index(drop=True)

plt.plot(df_1['t'], df_1['w'], label='acceleration')
plt.plot(df_2['t'], df_2['w'], label='deceleration')
