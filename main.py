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

is_top = False
is_save = True
sigmas = [0.1, 1.0 , 2.0]
cr_top10 = ["ZI", "APN", "MRN", "SCm", "PO", "LD", "SNr", "SSp", "MOp", "MOs"]
cr_others = ["SCs", "MG", "VPM", "VPL", "MD","CP", "PL", "ACA", "RSP", "VISam"]
n_bins = 50
root_folder = join('./spiking_histogram_neurons_all_trials', ('top10' if is_top else 'others'))


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
        
        save_path = join(root_folder, region) + '_spiking_histogram_neurons_all_trials.png'
        plot_spiking_histogram_neurons_all_trials(neurons_spks, region, bins=n_bins, save_path=save_path, save=is_save)
        
        #for sigma in sigmas:
        #    plot_average_activity_neurons_all_trials(neurons_spks, region, sigma=sigma)
        #plot_average_activity_neurons_all_trials(neurons_spks, region, sigma=1)
        #plot_average_activity_neurons_all_trials(neurons_spks, region, sigma=2)