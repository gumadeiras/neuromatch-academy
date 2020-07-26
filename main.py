#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt

import sys
from functions.plotting import *
from functions.filtering import *
from os.path import join

# load data from steinmetz dir
alldat = np.load('./steinmetz/steinmetz_part0.npz', allow_pickle=True)['dat']
alldat = np.hstack((alldat, np.load('./steinmetz/steinmetz_part1.npz', allow_pickle=True)['dat']))
alldat = np.hstack((alldat, np.load('./steinmetz/steinmetz_part2.npz', allow_pickle=True)['dat']))
print(f"number of recordings: {alldat.shape}")

regions_recorded(alldat)

is_top = True
is_save = True
sigmas = [0.1, 1.0 , 2.0]
cr_top10 = ["ZI", "APN", "MRN", "SCm", "PO", "LD", "SNr", "SSp", "MOp", "MOs"]
cr_others = ["SCs", "MG", "VPM", "VPL", "MD","CP", "PL", "ACA", "RSP", "VISam"]
n_bins = 50
root_folder = join('./psth', ('top10' if is_top else 'others'))

'''
if is_top:
    regions = cr_top10
else:
    regions = cr_others
    
for region in regions:
    rwr = recordings_with_region(alldat, region)
    for recording, __ in rwr:
        dat = alldat[recording]
        neurons = dat['brain_area'] == region
        neurons_spks = dat['spks'][neurons]
        
        ## First plot
        #save_path = join(root_folder, region) + '_spiking_histogram_neurons_all_trials.png'
        #plot_spiking_histogram_neurons_all_trials(neurons_spks, region, bins=n_bins, save_path=save_path, save=is_save)

        ## Second plot
        for sigma in sigmas:
            save_path = join(root_folder, region) + '_average_activity_neurons_all_trials_' + str(sigma) + '.png'
            plot_average_activity_neurons_all_trials(neurons_spks, region, sigma=sigma, save_path=save_path, save=is_save)

'''

if is_top:
    regions = cr_top10
else:
    regions = cr_others

for region in regions:
    for dat in alldat:
        neurons = dat['brain_area'] == region
        neurons_spks = dat['spks'][neurons]
        neurons_count = neurons_spks.shape[0]
        total_neurons_count = dat['spks'].shape[0]
        trials_count = dat['spks'].shape[1]
        save_path = join(root_folder, region) + '_psth.png'
        if neurons_count > 1:
#             plot_average_activity_neurons_all_trials(neurons_spks, region, sigma=2)
            psth(neurons_spks, region, timebin_size=5, save_path=save_path, save=is_save)
