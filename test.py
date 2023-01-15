# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

df_break = pd.DataFrame()
mass = 4.991 + 3.026  # kg

for run in range(8, 17):
    df_run = pd.read_csv('experiments/{}.csv'.format(run))
    df_run = df_run.rename(
        columns={'rotation number': 'n', 'time after start [s]': 't'})
    df_run.drop(df_run.tail(1).index, inplace=True)
    df_run['dt'] = df_run['t'] - df_run['t'].shift(1)
    df_run = df_run[df_run['dt'] > 0.01]

    # Omregn måledata til en tidserie med vinkelhastighedsværdier
    df_run['dt'] = df_run['t'] - df_run['t'].shift(1)
    df_run['w'] = 2*math.pi/df_run['dt']
    df_run['dw'] = df_run['w'] - df_run['w'].shift(1)

    #df_1 = df_run[df_run['dw'] > 0]
    df_2 = df_run[df_run['dw'] < 0]
    df_2['dw'] = df_2['dw'] * -1
    df_run.reset_index(drop=True)
    df_2.drop(df_2.head(1).index, inplace=True)
    plt.plot(df_2['w'], df_2['dw'], label=run)
    df_temp = df_2.set_index('w')['dw']/mass
    df_temp.rename(run, inplace=True)
    df_break = pd.concat([df_break, df_temp], axis=1)

#plt.plot(df_1['w'], df_1['dw'], label='acceleration')
plt.legend()
plt.grid()
plt.xticks(np.arange(0, 44, 3))
plt.xlabel('w')
plt.ylabel('dw')
plt.title('Breaking of flywheel as function of angular velocity')


df_break.sort_index(inplace=True)
print(df_break)

df_break = df_break.groupby(df_break.index // 1).mean()

df_break['average'] = df_break.mean(numeric_only=True, axis=1)
df_break.plot(y='average', label='average', grid=True, xlabel='w',
              ylabel='dw/m', title='Breaking of flywheel as function of angular velocity')

df_break.to_csv('stribby.csv')
