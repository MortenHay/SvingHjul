# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

df_break = pd.DataFrame()
mass = 4.991 + 3.026  # kg
figure, axis = plt.subplots(1, 2, figsize=(20, 10),sharey=True)

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
    axis[0].plot(df_2['w'], df_2['dw'], label="Run: {}".format(run))
    df_temp = df_2.set_index('w')['dw']
    df_temp.rename(run, inplace=True)
    df_break = pd.concat([df_break, df_temp], axis=1)

#plt.plot(df_1['w'], df_1['dw'], label='acceleration')
axis[0].legend()
axis[0].grid()
axis[0].set_xticks(np.arange(0, 44, 3))
axis[0].set_xlabel('w',fontsize = 18)
axis[0].set_ylabel('dw',fontsize = 18)
axis[0].set_title('All runs',fontsize = 18)
figure.suptitle('Breaking of flywheel as function of angular velocity',fontsize=24)


df_break.sort_index(inplace=True)
print(df_break)

df_break = df_break.groupby(df_break.index // 1).mean()

df_break['average'] = df_break.mean(numeric_only=True, axis=1)

axis[1].plot(df_break.index, df_break['average'], label='average')
axis[1].grid()
axis[1].set_xticks(np.arange(0, 44, 3))
axis[1].set_xlabel('w',fontsize = 18)
axis[1].set_title('Average',fontsize = 18)
figure.tight_layout()
#df_break.plot(y='average', label='average', grid=True, xlabel='w',ylabel='dw', title='Breaking of flywheel as function of angular velocity')

df_break.to_csv('stribby.csv')
