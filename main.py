#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt

import sys
from functions.plotting import *
from functions.filtering import *
from os.path import join
from argument_parser import argument_parser

if __name__ == '__main__':

    # Argument Parser
    args = argument_parser()

    # load data from steinmetz dir
    alldat = np.load('./steinmetz/steinmetz_part0.npz', allow_pickle=True)['dat']
    alldat = np.hstack((alldat, np.load('./steinmetz/steinmetz_part1.npz', allow_pickle=True)['dat']))
    alldat = np.hstack((alldat, np.load('./steinmetz/steinmetz_part2.npz', allow_pickle=True)['dat']))
    print("Number of Recordings: {r_shape}".format(r_shape = alldat.shape))

    is_top = False
    is_save = True
    sigmas = [0.1, 1.0 , 2.0]
    cr_top10 = ["ZI", "APN", "MRN", "SCm", "PO", "LD", "SNr", "SSp", "MOp", "MOs"]
    cr_others = ["SCs", "MG", "VPM", "VPL", "MD","CP", "PL", "ACA", "RSP", "VISam"]
    n_bins = 50
    wheel_to_mm = 0.135
    n_trials_plot = 10
    gaussian_filter_sigma = 3
    root_folder = join('./average_activity_neurons_all_trials', ('top10' if is_top else 'others'))

    
    if is_top:
        regions = cr_top10
    else:
        regions = cr_others

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

    '''
    for region in regions:
        for idx_animal, dat in enumerate(alldat):
            ## PSTH Plot ## 
            # save_path = join(root_folder, region) + '_psth.png'
            # if neurons_count > 1:
            #     psth(neurons_spks, region, timebin_size=5, save_path=save_path, save=is_save)

            # Wheel Movement Plot ##
            # wheel_act = dat['wheel'].squeeze()
            # for idx_trial, trial in enumerate(wheel_act[:n_trials_plot]):
            #     save_path = join(root_folder, region) + '_animal_'+ str(idx_animal) + '_trial_' + str(idx_trial)+ '.png'
            #     plot_wheel_movement(trial, 
            #                         wheel_to_mm=wheel_to_mm, 
            #                         sigma=gaussian_filter_sigma,
            #                         title='wheel position x time Animal: ' + str(idx_animal) + ' Trial: ' + str(idx_trial), 
            #                         save_path=save_path, save=is_save)

    '''