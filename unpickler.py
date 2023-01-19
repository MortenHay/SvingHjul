# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

figure, axis = plt.subplots(3, 3, figsize=(30, 30), sharex=True, sharey=True)
dir = 'figures/'
for i, ax in enumerate(axis.flat):
    filename = '{}'.format(i+8)
    r = pd.read_csv(os.path.join(dir, '{}/r'.format(filename)), index_col=0)
    s = pd.read_csv(os.path.join(dir, '{}/s'.format(filename)), index_col=0)
    c = pd.read_csv(os.path.join(dir, '{}/c'.format(filename)), index_col=0)
    rope_length = c['values']['rope_length']
    u0 = c['values']['u0']
    uc = c['values']['uc']
    weight = c['values']['weight']
    ax.plot(s['t'], s['w'], label='Simulation')
    ax.plot(r['t'], r['w'], label='Experiment')
    ax.legend(fontsize=24)
    ax.grid()
    #ax.set_xlabel('Time [s]',fontsize = 18)
    #ax.set_ylabel('Angular velocity [rad/s]', fontsize = 18)
    #ax.set_title('Angular velocity | Run {}'.format(filename),fontsize=18)
    
    ax.text(0.95, 0.7, 'Weight: {}kg\nRope length: {}m\nµ0: {}Ns\nµC: {}'.format(weight, rope_length.__round__(1), u0, uc), fontsize=24, ha='right', va='center', transform=ax.transAxes, backgroundcolor='lightgray')
    ax.tick_params(axis='both', which='major', labelsize=24)
    ax.label_outer()
    ax.set_title('Run {}'.format(filename), fontsize=24)

#axis[0,0].set_ylabel('Changing µ0',fontsize = 24)
#axis[1,0].set_ylabel('Changing µC',fontsize = 24)
figure.suptitle('Experiment vs simulation without flywheel', fontsize=48)
figure.supylabel('Angular velocity [rad/s]', fontsize=36)
figure.supxlabel('Time [s]', fontsize=36)
figure.tight_layout()
figure.subplots_adjust(top=0.92, left=0.09)
