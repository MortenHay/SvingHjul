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

# %% Definere konstanter og parameter
# Konstanter som i skal bruge i jeres beregninger
# Fx. friktions konstanter/parameter, masser, længder, radier, ...

# Changable parameters
run_number = 10  # 1-16
rope_length = 7  # m


# Load test parameters from index.csv
df_index = pd.read_csv('index.csv')
df_index.set_index('Run', inplace=True)
mass_weight = df_index.loc[run_number, 'Mass']
wheel_in_use = df_index.loc[run_number, 'Wheel']

# friction parameters
friction_constant = 0.025  # N/(m/s^2)

# Permanent constants
mass_steel = 4.048  # kg
mass_wood = 0.943  # kg
mass_wheel_total = mass_steel + mass_wood  # kg
mass_axis = 2.031  # kg
mass_end_disc = 0.037  # kg
mass_nut = 0.054  # kg
mass_washer = 0.011  # kg
mass_pulley = 0.104  # kg
mass_chip = 0.1867 / 40  # kg

radius_of_steel = 0.025  # m
radius_to_steel_inner = 0.125  # m
radius_to_steel_outer = 0.175  # m
radius_to_steel_center = (radius_to_steel_inner + radius_to_steel_outer)/2  # m
radius_wheel_inner = 0.01  # m
radius_wheel_outer = 0.2  # m
radius_pulley_outer = 0.023  # m
radius_pulley_inner = 0.01  # m
radius_axis = 0.01  # m
radius_end_disc_inner = 0.01  # m
radius_end_disc_outer = 0.075  # m
radius_nut_inner = 0.01  # m
radius_nut_outer = 0.033/2  # m
radius_washer_inner = 0.021/2  # m
radius_washer_outer = 0.036/2  # m
radius_bearing_inner = 0.01  # m
radius_bearing_outer = 0.036/2  # m
radius_bearing_pitch = (radius_bearing_inner + radius_bearing_outer)/2  # m

number_of_end_discs = 3
number_of_nuts = 12
number_of_washers = 12
number_of_chips = 4*16

gravity = 9.82  # m/s^2

# Beregn inertimomentet og drejningsmomentet
# Inertia of test construction
inertia_axis = mass_axis*radius_axis**2
inertia_pulley = 1/2 * mass_pulley * \
    (radius_pulley_outer**2 + radius_pulley_inner**2)
inertia_end_disc = 1/2 * mass_end_disc * \
    (radius_end_disc_outer**2 + radius_end_disc_inner**2) * number_of_end_discs
inertia_nut = 1/2 * mass_nut * \
    (radius_nut_outer**2 + radius_nut_inner**2) * number_of_nuts
inertia_washer = 1/2 * mass_washer * \
    (radius_washer_outer**2 + radius_washer_inner**2) * number_of_washers
inertia_test_construction = inertia_axis + inertia_pulley + \
    inertia_end_disc + inertia_nut + inertia_washer
print("{} kg*m^2".format(inertia_test_construction))

# Inertia of wheel
inertia_wood = 1/2 * (mass_wood + mass_chip*number_of_chips) * \
    (radius_wheel_inner**2 + radius_wheel_outer**2)
inertia_steel = mass_steel * radius_to_steel_center**2
inertia_removed_chips = mass_chip * number_of_chips * radius_to_steel_center**2
inertia_wheel = inertia_wood + inertia_steel - inertia_removed_chips

# Total inertia
inertia_total = inertia_test_construction + inertia_wheel*wheel_in_use

# Definere en funktion som beregner friktionen
mass_test_construction = mass_axis + mass_pulley + mass_end_disc * \
    number_of_end_discs + mass_nut * number_of_nuts + mass_washer * number_of_washers


def friction(omega, weight_active):
    mass_total = mass_test_construction + mass_wheel_total * \
        wheel_in_use + mass_weight * weight_active
    return friction_constant * mass_total * omega * radius_bearing_pitch

# Definere en funktion som beregner accelerationen indtil lodet rammer gulven


def acceleration(omega):
    Ta = mass_weight * gravity * radius_pulley_outer
    Tf = friction(omega, True)
    return (Ta - Tf) / (inertia_total + mass_weight * radius_pulley_outer**2)

# Definere en funktion som beregner decelerationen efter lodet ramte gulven


def deceleration(omega):
    Tf = friction(omega, False)
    return -Tf / inertia_total

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
    t = np.arange(t0, tn, h)
    w = np.zeros(len(t))

    w[0] = w0
    weight_active = True
    total_stretch = w[0] * radius_pulley_outer * t0  # m

    # Lave en for-loop til at beregne vinkelhastighedens udvikling
    # Husk at vinkelacceleration ændre sig nå lodet rammer jorden
    # hvordan skal i tage højde for det i for-loopet?

    for k in range(1, len(t)):
        w[k] = w[k-1] + acceleration(w[k-1]) * \
            h if weight_active else w[k-1] + deceleration(w[k-1]) * h
        total_stretch += w[k] * radius_pulley_outer * h
        weight_active = False if total_stretch >= rope_length else True
    # Retunere resultaterne

    return t, w


# %% Indlæse data fra jeres forsøg (Husk: funktionen pd.read_csv())
df_run = pd.read_csv('experiments/{}.csv'.format(run_number))
df_run = df_run.rename(
    columns={'rotation number': 'n', 'time after start [s]': 't'})
df_run.drop(df_run.tail(1).index, inplace=True)
df_run['dt'] = df_run['t'] - df_run['t'].shift(1)
df_run = df_run[df_run['dt'] > 0.01]

# Omregn måledata til en tidserie med vinkelhastighedsværdier
df_run['dt'] = df_run['t'] - df_run['t'].shift(1)
df_run['w'] = 2*math.pi/df_run['dt']
df_run.reset_index(drop=True)

# %% Kald jeres Eulers-metode funktion til at køre en simulation
t, w = eulersMethod(acceleration, deceleration,
                    df_run['t'].iloc[1], df_run['w'].iloc[1], 0.001, df_run['t'].iloc[-1])
df_sim = pd.DataFrame({'t': t, 'w': w})
# %% Plot resultater fra jeres simulation og forsøg
# Plot Forsøg
plt.plot(df_run['t'], df_run['w'], label='Forsøg')
plt.plot(df_sim['t'], df_sim['w'], label='Simulation')
plt.legend()
plt.grid()
plt.xlabel('Time [s]')
plt.ylabel('Angular velocity [rad/s]')
