# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 12:44:58 2023

@author: felipealm97

Here we calculate the psd of the simulated traces for differents NA's 
We also upload the Kullback Lieber (KL) method as a function of NA 


"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from scipy.optimize import curve_fit
import scipy.signal as signal

plt.rcParams.update({'font.size': 14})
plt.rcParams["axes.linewidth"] = 2


def psd(time, sig, dt=1e-5):
    '''Defining PSD funcition. It takes a NxM array (N traces x M time stamps) 
    and returns the frequencies and a list with M entries, each entry has the
    PSD of each trace. It's assumed that all signals have the same time stamps.
    '''

    freq, power = signal.welch(sig, 1/dt, window = 'rectangular', nperseg = int(len(sig/500)))
    return freq, power

def model(f,D,f_c,cst):
    '''Defining the Lorentzian curve used to fit both simulated and 
    experimental data
    '''
    return  (D/(2*np.pi**2))/(f_c**2+f**2)+ cst


#Defining the sampling frequency of the simulations
dt=1e-5
t_max=1
time=np.linspace(0, t_max, int(t_max/dt))


#Uploading the simulated traces of the particle inside OBB for a variety of NAs
f_c_x_mean=[]
f_c_z_mean=[]
f_c_x_std=[]
for i in range(28, 61): 
    NA=i
    f_c_x=[]
    f_c_z=[]
    for experiment in range(1,6):
        filename_positions=r'data/simulations/kl/OBB_positions_NA_%d'%NA + '_exp_%d.txt' %experiment
        data_positions= np.loadtxt(filename_positions, delimiter=',', skiprows=0, dtype=float)
        
        # Calculating PSD for the simulation
        freq_x, psds_x = psd(time[1:], data_positions[0])
        freq_z, psds_z = psd(time[1:], data_positions[2])

        #Fitting the psds in a Lorentzian curve.
        #Reminder: "model" is a function that creates a Lorentzian curve
        fit_x = curve_fit(model,freq_x,psds_x,  p0=[1e-15, 50, 0 ])
        fit_z = curve_fit(model,freq_z,psds_z,  p0=[1e-15, 10, 0 ])


        ans_x, cov_x = fit_x
        ans_z, cov_z = fit_z
        fit_D_x,fit_f_c_x,fit_cst_x = ans_x
        fit_D_z,fit_f_c_z,fit_cst_z = ans_z
        
        
        f_c_x.append(np.abs(fit_f_c_x))
        f_c_z.append(np.abs(fit_f_c_z))
        
    f_c_x_mean.append(np.mean(f_c_x))
    f_c_x_std.append(np.std(f_c_x))
    f_c_z_mean.append(np.mean(f_c_z))


    
#plot results
NA=np.arange(28,61)*0.01

fig1, ax1 = plt.subplots()
ax1.errorbar(NA, f_c_x_mean,yerr=f_c_x_std, linestyle='solid', marker='s', markersize=3, color='C0', ecolor='C0', elinewidth=2, capsize=1)
ax1.set_xlabel(r'$ NA $')
ax1.set_ylabel(r'$ f_{c} (Hz) $')
ax1.grid(alpha=0.4)


# Uploading the KL curve that compares the simulation with the experimental data

data='data/results/kl.csv'
df=pd.read_csv(data)
kl=df['mean']
kl_std=df['std']


fig,ax1=plt.subplots(2, 1, sharex=True)
ax1[0].errorbar(NA, f_c_x_mean,yerr=f_c_x_std, linestyle='solid', marker='s', markersize=3, color='C0', ecolor='C0', elinewidth=2, capsize=1)
ax1[0].set_xlabel(r'$ NA $')
ax1[0].set_ylabel(r'$ f_{c} \rm (Hz) $')
ax1[0].set_xlim([0.40, 0.55])
ax1[0].set_ylim([0, 40])
ax1[0].set_xticks(np.arange(0.2, 0.05, 0.6))
ax1[0].fill_between(np.arange(0.45,0.50,0.01), 0, 300, alpha=0.2)
ax1[0].fill_between(np.arange(0.45,0.48,0.01), 0, 300, color='C1', alpha=0.2)
ax1[0].fill_between(np.arange(0.45, 0.48, 0.01), 0, 300, facecolor="none", hatch="////", edgecolor="k", alpha=0.20)
ax1[0].grid(alpha=0.4)


kl=df['mean']
ax1[1].errorbar(NA, kl, yerr=kl_std, linestyle='solid', marker='s', markersize=3, color='C0')
ax1[1].fill_between(np.arange(0.44,0.48,0.01), 0, 5, color='C1', alpha=0.2)
ax1[1].fill_between(np.arange(0.45, 0.48, 0.01), 0, 300, facecolor="none", hatch="////", edgecolor="k", alpha=0.25)
ax1[1].grid(alpha=0.4)
ax1[1].set_xlim([0.40, 0.55])
ax1[1].set_ylim([0, 3])
ax1[1].set_ylabel(r'$ D\left( \mathcal{P}_{\rm exp} \|| \mathcal{P}_{\rm sim} \right) $')
ax1[1].yaxis.labelpad=20


fig.subplots_adjust(hspace=0)

NA_list=list([0.40,0.45,0.50,0.55])#,0.60])
ax1[1].set(xlabel='NA')
ax1[1].set_xticks(NA_list)

ax1[1].set_yticks(list([0,1,2]))
plt.show()