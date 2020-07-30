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
    neurons_topk = np.asarray([[ 54,  85,   0,  35,  50,  81,  61, 163, 161,  77], [79, 94, 74, 96, 52, 23, 29, 12, 32, 56], [33,  5, 16, 32,  4, 13, 34, 26, 31,  6], [17, 46, 24, 43, 35, 41, 45, 22, 14, 37], [104,  46,  84,  95,  99,  55,  98,  25,  19,  38], [56, 55, 34, 61, 54,  8, 39, 24, 10, 48], [40, 23, 22, 17,  4,  8, 41, 24,  1, 11], [116,  35, 110,  57,  90, 115,  31,  55, 105,  46], [ 63, 124,   8, 111, 128,  29, 121,  80,   5,  85], [74, 86, 52, 80, 10, 57, 17, 45, 37,  7], [  9,  83, 122, 136,  48,  92, 153, 111,  47, 112], [ 1, 10, 13,  7, 14,  3,  6,  2,  4, 12]])

    # Load data from Steinmetz dir
    alldat = np.load('./steinmetz/steinmetz_part0.npz', allow_pickle=True)['dat']
    alldat = np.hstack((alldat, np.load('./steinmetz/steinmetz_part1.npz', allow_pickle=True)['dat']))
    alldat = np.hstack((alldat, np.load('./steinmetz/steinmetz_part2.npz', allow_pickle=True)['dat']))
    print("Number of Recordings: {r_shape}".format(r_shape = alldat.shape))
    

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

    region_neurons = []
    mean_neurons_acc = []
    neuron_choose = []


    for animal_idx in range(neurons_topk.shape[0]):
        #filter_data_visp[animal_idx][1][neuron_idx] # spikes
        #filter_data_visp[animal_idx][-1] # response
        spks = []

        for idx in neurons_topk[animal_idx]:
            print(filter_data_visp[animal_idx][1][idx].shape)
            spks.append(filter_data_visp[animal_idx][1][idx])
        plot_per_trial_activity(np.asarray(spks), "debug")
        # 
        # print(filter_data_visp[animal_idx][1].shape)
        # neurons_topk[animal_idx], "vspi")