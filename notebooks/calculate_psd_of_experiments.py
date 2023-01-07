# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 15:50:06 2023

@author: felipealm97

Here we calculate the psd of the experimental data using probe beam

"""
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks


plt.rcParams.update({'font.size': 14})
plt.rcParams["axes.linewidth"] = 2



d = 'Oct-27-2022' #data que a coleta foi feita
#names of the root folder, main folder and file where the traces are saved
root_folder = r'Scripts/probe beam_PSD'
file_name = 'traces_CH2-CH3-CH4.npz'

#Define the time array based on the sampling frequency choosen in the experiment
experiment=str(70)
folder_name = 'exp_'+experiment+'_'+d
data = np.load(root_folder+'/'+folder_name+'/'+file_name)
# Extracting compressed data variables
traces_CH2 = data['arr_0']
traces_CH2 = np.array(traces_CH2)   
time = traces_CH2[0][0] 


first_exp=56
last_exp=70



def psd(time, sig):
    dt = time[1]-time[0]
    p_den = []
    for i in range(len(sig)):
        freq, power = signal.welch(sig[i,:], 1/dt, window = 'rectangular', nperseg = len(sig[i]))
        p_den.append(power)
    return freq, p_den

def mean_list(lista):
    array_soma = lista[0]
    for i in range(len(lista)-1):
        array_soma += lista[i+1]
    media = array_soma/len(lista)
    return media

def model(f,D,f_c,cst):
    return  (D/(2*np.pi**2))/(f_c**2+f**2)+ cst


def mean_list_and_std_of_points(lista):
    lista = np.array(lista)
    
    N_freq = len(lista[0])                                                      # Number of frequencies sampled for each realization
    
    array_mean = np.zeros(N_freq)                                               # Mean PSD at each frequency
    array_std  = np.zeros(N_freq)                                               # Std PSD at each frequency
    
    for i in range(N_freq):
        array_mean[i] = np.mean( lista[:, i] )                                  # For each frequency, take the PSDs for all realizations and find their mean value
        array_std[i]  = np.std ( lista[:, i] )                                  # For each frequency, take the PSDs for all realizations and find their mean value
   
    return array_mean, array_std

def mean_list_and_var_of_points(lista):
    lista = np.array(lista)
    
    N_freq = len(lista[0])                                                      # Number of frequencies sampled for each realization
    
    array_mean = np.zeros(N_freq)                                               # Mean PSD at each frequency
    array_var  = np.zeros(N_freq)                                               # Std PSD at each frequency
    
    for i in range(N_freq):
        array_mean[i] = np.mean( lista[:, i] )                                  # For each frequency, take the PSDs for all realizations and find their mean value
        array_var[i]  = np.var ( lista[:, i] )                                  # For each frequency, take the PSDs for all realizations and find their mean value
   
    return array_mean, array_var

#This function receives a list of lists, and return a list in which the i-th element is the average value of the t-th elements of each list
def media_e_std_de_listas(lista_de_listas):
    numero_de_listas = len(lista_de_listas)
    numero_de_elementos_por_lista = len(lista_de_listas[0])
    
    lista_media = np.zeros(numero_de_elementos_por_lista)
    lista_std = np.zeros(numero_de_elementos_por_lista)
    
    for i in range(numero_de_elementos_por_lista):
        elements_i = []
        for j in range(numero_de_listas):
            elements_i.append(lista_de_listas[j][i])
            
        lista_media[i]=np.mean(elements_i)
        lista_std[i]=np.std(elements_i)
        
    return lista_media, lista_std

def mean_psd (root_folder, file_name ,first_exp, last_exp): #calcula a media entre um intervalo de realizações
    mean_psd_x=np.zeros(1251)
    mean_psd_y=np.zeros(1251)
    mean_psd_z=np.zeros(1251)
    
    Pxx_traces = []
    Pyy_traces = []
    Pzz_traces = []
    
    
    
    for i in range(first_exp,last_exp+1):                                       # For each experiment
        
        # Open folder
        experiment=str(i)
        folder_name = 'exp_'+experiment+'_'+d
        data = np.load(root_folder+'/'+folder_name+'/'+file_name)
        
        # Extracting compressed data variables
        traces_CH2 = data['arr_0']
        traces_CH3 = data['arr_1']
        traces_CH4 = data['arr_2']

        traces_CH2 = np.array(traces_CH2)                                       # Get the traces for x-signal
        traces_CH3 = np.array(traces_CH3)                                       # Get the traces for y-signal
        traces_CH4 = np.array(traces_CH4)                                       # Get the traces for z-signal
        
        #time = traces_CH2[0][0] #array with time stamps
        signal_x_norm = traces_CH2[:,1,:]/traces_CH4[:,1,:]                     # Normalized signal x
        signal_y_norm = traces_CH3[:,1,:]#/traces_CH4[:,1,:]                     # Normalized signal y
        signal_z = traces_CH4[:,1,:]
        
        #calculate psds
        freq_x, psds_x = psd(time, signal_x_norm)                               # PSD for each realization oneach experiment for x-signal
        freq_y, psds_y = psd(time, signal_y_norm)                               # PSD for each realization oneach experiment for y-signal
        freq_z, psds_z = psd(time, signal_z)                                    # PSD for each realization oneach experiment for z-signal
        
        
        psds_x = np.array(psds_x)                                               # Transform into np.ndarray
        psds_y = np.array(psds_y)                                               # Transform into np.ndarray
        psds_z = np.array(psds_z)                                               # Transform into np.ndarray
        
        # For all these realizations, calculate the mean PSD for this experiment
        mean_psd_x, _ = mean_list_and_var_of_points(psds_x)                     # Get mean values of the PSD for this experiment of x-signal
        mean_psd_y, _ = mean_list_and_var_of_points(psds_y)                     # Get mean values of the PSD for this experiment of y-signal
        mean_psd_z, _ = mean_list_and_var_of_points(psds_z)                     # Get mean values of the PSD for this experiment of z-signal
        
        # Add these mean into a huge list of mean experiments
        Pxx_traces.append(mean_psd_x.tolist())                                  # Create list with the mean of each experiment for x-signal
        Pyy_traces.append(mean_psd_y.tolist())                                  # Create list with the mean of each experiment for y-signal
        Pzz_traces.append(mean_psd_z.tolist())                                  # Create list with the mean of each experiment for z-signal
    
    # Find the mean of the experiments and associated standard deviations (bar errors)
    mean_psd_x, mean_std_x = media_e_std_de_listas(Pxx_traces)
    mean_psd_y, mean_std_y = media_e_std_de_listas(Pyy_traces)
    mean_psd_z, mean_std_z = media_e_std_de_listas(Pzz_traces)
    

    
    ############### To delete the modulation induced by the SLM ##################    
    SLM_modulation_idx = np.array([24,48,72,120])
    
    freq_x = np.delete(freq_x, SLM_modulation_idx)
    mean_psd_x = np.delete(mean_psd_x, SLM_modulation_idx)
    mean_psd_y = np.delete(mean_psd_y, SLM_modulation_idx)
    mean_psd_z = np.delete(mean_psd_z, SLM_modulation_idx)
    
    mean_psd_x = np.delete(mean_psd_x, SLM_modulation_idx)
    mean_psd_y = np.delete(mean_psd_y, SLM_modulation_idx)
    mean_psd_z = np.delete(mean_psd_z, SLM_modulation_idx)
    
    
    mean_std_x = np.delete(mean_std_x, SLM_modulation_idx)
    mean_std_y = np.delete(mean_std_y, SLM_modulation_idx)
    mean_std_z = np.delete(mean_std_z, SLM_modulation_idx)
    #############################################################################
    
    std_vector= np.zeros((3,len(mean_std_x)))
    std_vector[0]=mean_std_x
    std_vector[1]=mean_std_y
    std_vector[2]=mean_std_z
    
    
    lmin=2
    lmax=71

    mean_psd_x=mean_psd_x[lmin:lmax]
    mean_psd_y=mean_psd_y[lmin:lmax]
    mean_psd_z=mean_psd_z[lmin:lmax]
    freq_x=freq_x[lmin:lmax]
    
    fit_x = curve_fit(model,freq_x,mean_psd_x)
    fit_y = curve_fit(model,freq_x,mean_psd_y)
    fit_z = curve_fit(model,freq_x,mean_psd_z)
    
    ans_x, cov_x = fit_x
    ans_y, cov_y = fit_y
    ans_z, cov_z = fit_z
    fit_D_x,fit_f_c_x,fit_cst_x = ans_x
    fit_D_y,fit_f_c_y,fit_cst_y = ans_y
    fit_D_z,fit_f_c_z,fit_cst_z = ans_z
    
    perr_x = np.sqrt(np.diag(cov_x))        #It provides the standard deviation of the parameter estimated. 
    perr_y = np.sqrt(np.diag(cov_y))        #It provides the standard deviation of the parameter estimated.     
    perr_z = np.sqrt(np.diag(cov_z))        #It provides the standard deviation of the parameter estimated.     
   
    
    print("F_c_x_mean = "+str(fit_f_c_x)+" +-"+str(perr_x[1])+" Hz")
    print("F_c_y_mean = "+str(fit_f_c_y)+" +-"+str(perr_y[1])+" Hz")
    print("F_c_z_mean = "+str(fit_f_c_z)+" +-"+str(perr_z[1])+" Hz")
    
    
    psd_fit_x = np.zeros(len(freq_x))
    psd_fit_y = np.zeros(len(freq_x))
    psd_fit_z = np.zeros(len(freq_x))
    

    for i in range(len(freq_x)):
        psd_fit_x[i] = model(freq_x[i],fit_D_x,fit_f_c_x,fit_cst_x)
        psd_fit_y[i] = model(freq_x[i],fit_D_y,fit_f_c_y,fit_cst_y)
        psd_fit_z[i] = model(freq_x[i],fit_D_z,fit_f_c_z,fit_cst_z)
    
    plt.close('all')
    
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig3, ax3 = plt.subplots()
    

    ax1.errorbar(freq_x, mean_psd_x,yerr=mean_std_x[lmin:lmax], fmt='o', markersize=1, color='red', ecolor='red', elinewidth=0.5, capsize=0)
    ax1.plot(freq_x,psd_fit_x, color='blue')
    ax1.set_xscale("log", nonposx='clip')
    ax1.set_yscale("log", nonposy='clip')
    ax1.set_title("Aliased Lorentzian - x axis")
    #fig1.savefig(root_folder+'/'+folder_name+'/'+'psd_x_loglog.png')


    ax2.errorbar(freq_x, mean_psd_y,yerr=mean_std_y[lmin:lmax], fmt='o', markersize=1, color='red', ecolor='red', elinewidth=0.5, capsize=0)
    ax2.loglog(freq_x,psd_fit_y, color='blue')
    ax2.set_title("Aliased Lorentzian - y axis")
    #fig2.savefig(root_folder+'/'+folder_name+'/'+'psd_y_loglog.png')
       
    
    ax3.errorbar(freq_x, mean_psd_z,yerr=mean_std_z[lmin:lmax], fmt='o', markersize=1, color='red', ecolor='red', elinewidth=0.5, capsize=0)
    ax3.loglog(freq_x,psd_fit_z, color='blue')
    ax3.set_title("Aliased Lorentzian - z axis")
    
    return freq_x, mean_psd_x, mean_psd_y, mean_psd_z, std_vector


freq_x, mean_psd_x, mean_psd_y, mean_psd_z, std_vector = mean_psd(root_folder, file_name,first_exp, last_exp)




