# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

figure, axis = plt.subplots(3, 3, figsize=(10, 10))
coords = [[0, 0], [0, 1], [0, 2], [1, 0], [
    1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

df_index = pd.read_csv('index.csv', index_col=0)
start = 8

for i in range(start, 17):
    mass = df_index['Mass'][i]
    df_run = pd.read_csv('experiments/{}.csv'.format(i))
    df_run.drop(df_run.tail(1).index, inplace=True)
    df_run.rename(columns={'rotation number': 'n',
                  'time after start [s]': 't'}, inplace=True)
    df_run['dt'] = df_run['t'] - df_run['t'].shift(1)
    df_run = df_run[df_run['dt'] > 0.01]
    df_run['dt'] = df_run['t'] - df_run['t'].shift(1)
    df_run['w'] = 2*math.pi/df_run['dt']
    axis[coords[i-start][0], coords[i-start][1]
         ].plot(df_run['t'], df_run['w'], label="Run: {}, Weight: = {}kg".format(i, mass))
    axis[coords[i-start][0], coords[i-start][1]].grid()
    axis[coords[i-start][0], coords[i-start][1]].set_xlabel('t [s]')
    axis[coords[i-start][0], coords[i-start][1]].set_ylabel('w [rad/s]')
    axis[coords[i-start][0], coords[i-start][1]
         ].set_title('Run {}, Weight: {}kg'.format(i, mass))
figure.suptitle(
    'Angular velocity of test construction with flywheel', fontsize=24)
figure.tight_layout()
plt.show()
