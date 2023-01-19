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
import os

# %% Definere konstanter og parameter
# Konstanter som i skal bruge i jeres beregninger
# Fx. friktions konstanter/parameter, masser, længder, radier, ...

# Changable parameters
motor_torque =  19 # Nm
motor_on_time = 3600  # s
motor_stop_rpm = 3000
home_consumption = 1000 #W
run_time = 3600*8
write_out = True


# friction parameters
friction_constant = 0.72  # Ns
friction_constant_2 = 0.002


# Permanent constants
density_steel = 7850  # kg/m^3
radius_of_steel = 0.05  # m
number_of_cylinders = 32
radius_to_steel_center = 0.45  # m
length_of_cylinder = 3  # m
radius_bearing_pitch = 0.025  # m
motor_stop_w = motor_stop_rpm * 2 * math.pi / 60


gravity = 9.82  # m/s^2


# Beregn inertimomentet og drejningsmomentet
volume_steel = math.pi * radius_of_steel**2 * length_of_cylinder
mass_steel = density_steel * volume_steel
inertia_steel = mass_steel * radius_to_steel_center**2
inertia_total = inertia_steel * number_of_cylinders

# Definere en funktion som beregner friktionen

def friction(omega):
    mass_total = mass_steel * number_of_cylinders
    return (friction_constant * omega + friction_constant_2 * mass_total * gravity) * radius_bearing_pitch


def consumption(omega,dt):
    E_current = inertia_total * omega ** 2
    E_out = home_consumption * dt
    E_after = E_current - E_out
    omega_after = math.sqrt(E_after / inertia_total)
    return omega - omega_after

# Definere en funktion som beregner accelerationen indtil lodet rammer gulven


def acceleration(omega):
    Ta = motor_torque
    Tf = friction(omega)
    return (Ta - Tf) / inertia_total

# Definere en funktion som beregner decelerationen efter lodet ramte gulven


def deceleration(omega):
    Tf = friction(omega)
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
    motor_active = True
    time_passed = 0

    # Lave en for-loop til at beregne vinkelhastighedens udvikling
    # Husk at vinkelacceleration ændre sig nå lodet rammer jorden
    # hvordan skal i tage højde for det i for-loopet?

    for k in range(1, len(t)):
        w[k] = w[k-1] + f1(w[k-1]) * h - consumption(w[k-1],h) if motor_active else w[k-1] + f2(w[k-1]) * h- consumption(w[k-1],h)
        time_passed += h
        if w[k] > motor_stop_w:
            motor_active = False
    # Retunere resultaterne
    return t, w


# %% Kald jeres Eulers-metode funktion til at køre en simulation
t, w = eulersMethod(acceleration, deceleration,0, 200, 0.01, run_time)
df_sim = pd.DataFrame({'t': t, 'w': w})
# %% Plot resultater fra jeres simulation og forsøg
# Plot Forsøg
plt.plot(df_sim['t']/3600, df_sim['w']*60/(2*math.pi), label='Simulation')
plt.legend(fontsize=14)
plt.grid()
plt.xlabel('Time [h]', fontsize=18)
plt.ylabel('Angular velocity [rpm]', fontsize=18)
plt.title('Angular velocity | Upscaled example', fontsize=24)
plt.text(0.95, 0.6,'mass: {}t\nµ0: {}\nµC: {}'.format(round(mass_steel*number_of_cylinders/1000,1),friction_constant, friction_constant_2), fontsize=14, ha='right', va='center', transform=plt.gca().transAxes, backgroundcolor='lightgray')
plt.tight_layout()

# if(write_out):
#     df_constant = pd.DataFrame()
#     df_constant['constants'] = ['rope_length', 'u0', 'uc', 'weight']
#     df_constant['values'] = [rope_length,
#                              friction_constant, friction_constant_2, mass_weight]
#     df_constant.set_index('constants', inplace=True)
#     try:
#         os.mkdir(dir)
#         df_sim.to_csv('{}/s'.format(dir))
#         df_constant.to_csv('{}/c'.format(dir))
#     except:
#         df_sim.to_csv('{}/s'.format(dir))
#         df_constant.to_csv('{}/c'.format(dir))
