#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt

import sys
from functions.plotting import *
from functions.filtering import *
from os.path import join
from argument_parser import argument_parser

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

from scipy.ndimage import gaussian_filter1d





if __name__ == '__main__':

    # Argument Parser
    args = argument_parser()

    is_top = args.top_choice
    is_save = args.save
    n_bins = args.n_bins
    n_trials_plot = args.n_trials
    gaussian_filter_sigma = args.sigma
    wheel_to_mm = args.wheel_to_mm
    
    sigmas = [0.1, 1.0 , 2.0]
    
    ## Choice Regions
    cr_top10 = ["ZI", "APN", "MRN", "SCm", "PO", "LD", "SNr", "SSp", "MOp", "MOs"]
    cr_others = ["SCs", "MG", "VPM", "VPL", "MD","CP", "PL", "ACA", "RSP", "VISam"]
    regions = cr_top10 if is_top else cr_others
    root_folder = join('./psth_combined', ('top10' if is_top else 'others'))

    # Load data from Steinmetz dir
    alldat = np.load('./steinmetz/steinmetz_part0.npz', allow_pickle=True)['dat']
    alldat = np.hstack((alldat, np.load('./steinmetz/steinmetz_part1.npz', allow_pickle=True)['dat']))
    alldat = np.hstack((alldat, np.load('./steinmetz/steinmetz_part2.npz', allow_pickle=True)['dat']))
    print("Number of Recordings: {r_shape}".format(r_shape = alldat.shape))
    

    teste = filter_trials_full_contrast(alldat, "VISp") #recordings_with_region( alldat, "VISp") 


    filter_data_visp = filter_trials_full_contrast(alldat, "VISp") #recordings_with_region( alldat, "VISp")
    # [
    # mouse_name,
    # mouse_spikes,
    # mouse_regions,
    # mouse_gocue,
    # mouse_resptime,
    # mouse_wheel,
    # mouse_feedback,
    # mouse_response,
    # ]


    # First define the model
    log_reg = LogisticRegression(penalty="none")
    cross_valid_k = 8 
    topk = 10

    region_neurons = []
    mean_neurons_acc = []
    neuron_choose = []

    for animal_idx in range(filter_data_visp.shape[0]):
        mean_neurons_acc = []
        for neuron_idx in range(filter_data_visp[animal_idx][1].shape[0]):
            
            X = filter_data_visp[animal_idx][1][neuron_idx] # spikes
            y = filter_data_visp[animal_idx][-1] # response
            
            accuracies = cross_val_score(LogisticRegression(penalty='none', max_iter=200), X, y, cv=cross_valid_k) 
            mean_neurons_acc.append(np.mean(accuracies))
            print(f"neuron_idx {neuron_idx}:{filter_data_visp[animal_idx][1].shape[0]}, animal_idx: {animal_idx}:{filter_data_visp.shape[0]}")
        
        
        ####################### DEBUG ACC ########################################
        # print("---------------------------")
        # print(f"animal_idx: {animal_idx}:{filter_data_visp.shape[0]}")
        # a = np.asarray(mean_neurons_acc)
        # for idx in np.argsort(np.asarray(mean_neurons_acc))[-topk:][::-1]:
        #     print(idx, a[idx])
        # neuron_choose.append([np.asarray(mean_neurons_acc).argsort()[-topk:][::-1]])
        # print(neuron_choose)
        # print("---------------------------")


    '''
    for region in regions:
        rwr = recordings_with_region(alldat, region)
        for recording, __ in rwr:
        #for dat in alldat:
            dat = alldat[recording]
            neurons = dat['brain_area'] == region
            neurons_spks = dat['spks'][neurons]
            neurons_count = neurons_spks.shape[0]
            total_neurons_count = dat['spks'].shape[0]
            trials_count = dat['spks'].shape[1]
                
            ## Spiking Histogram Neurons All Trials Plot ## 
            # save_path = join(root_folder, region) + '_spiking_histogram_neurons_all_trials.png'
            # plot_spiking_histogram_neurons_all_trials(neurons_spks, region, bins=n_bins, save_path=save_path, save=is_save)

            ## Average Activity Neurons All Trials Plot ## 
            for sigma in sigmas:
                save_path = join(root_folder, region) + '_average_activity_neurons_all_trials_' + str(sigma) + '.png'
                plot_average_activity_neurons_all_trials(neurons_spks, region, sigma=sigma, save_path=save_path, save=is_save)
    

    
    for region in regions:

        ## PSTH Combined Plot ## 
        save_path = join(root_folder, region) + '_psth_combined.png'
        psth_combined(alldat, region, timebin_size=5, save_path=save_path, save=is_save) 

        # for idx_animal, dat in enumerate(alldat):
        #     ## PSTH Plot ## 
        #     # save_path = join(root_folder, region) + '_psth.png'
        #     # if neurons_count > 1:
        #     #     psth(neurons_spks, region, timebin_size=5, save_path=save_path, save=is_save)
        # 
        #     # Wheel Movement Plot ##
        #     # wheel_act = dat['wheel'].squeeze()
        #     # for idx_trial, trial in enumerate(wheel_act[:n_trials_plot]):
        #     #     save_path = join(root_folder, region) + '_animal_'+ str(idx_animal) + '_trial_' + str(idx_trial)+ '.png'
        #     #     plot_wheel_movement(trial, 
        #     #                         wheel_to_mm=wheel_to_mm, 
        #     #                         sigma=gaussian_filter_sigma,
        #     #                         title='wheel position x time Animal: ' + str(idx_animal) + ' Trial: ' + str(idx_trial), 
        #     #                         save_path=save_path, save=is_save)

    

    '''