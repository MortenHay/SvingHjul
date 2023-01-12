# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 21:23:55 2023

@author: tweck
"""
# %% Importere minimum følgende pakker
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# Definere konstanter og parameter
# Konstanter som i skal bruge i jeres beregninger
# Fx. friktions konstanter/parameter, masser, længder, radier, ...

# Beregn inertimomentet og drejningsmomentet

# Definere en funktion som beregner friktionen


# Definere en funktion som beregner accelerationen indtil lodet rammer gulven


# Definere en funktion som beregner decelerationen efter lodet ramte gulven

# Definere Eulers metode til integration
# (husk: øvelsen om befolkningsmodellen og simulationen af varmepumpen)
def eulersMethod(f1, f2, t0, w0, h, tn):
    '''
    Parameters
    ----------
    f1 : Funktion for acceleration
    f2 : Funktion for deceleration
    t0 : Start tid 
    w0 : Start værdi af vinkelhastigheden
    dt : Skridtstørrelse
    tn : Slut tid

    Returns
    -------
    t : Tid
    w : Vinkelhastighed.
    '''
    # Definere en dataframe eller array til at gemme resultater

    # Lave en for-loop til at beregne vinkelhastighedens udvikling
    # Husk at vinkelacceleration ændre sig nå lodet rammer jorden
    # hvordan skal i tage højde for det i for-loopet?

    # Retunere resultaterne

# Kald jeres Eulers-metode funktion til at køre en simulation


# %% Indlæse data fra jeres forsøg (Husk: funktionen pd.read_csv())
df_run = pd.read_csv('experiments/14.csv')
df_run = df_run.rename(
    columns={'rotation number': 'n', 'time after start [s]': 't'})
df_run['dt'] = df_run['t'] - df_run['t'].shift(1)
df_run = df_run[df_run['dt'] > 0.01]
df_run['dt'] = df_run['t'] - df_run['t'].shift(1)
df_run['w'] = 2*math.pi/df_run['dt']
df_run.reset_index(drop=True)
df_run.plot(x='t', y='w')
# Omregn måledata til en tidserie med vinkelhastighedsværdier


# Plot resultater fra jeres simulation og forsøg
# %% Plot Forsøg
