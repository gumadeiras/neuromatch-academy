import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

def plot_spiking_histogram_neurons_all_trials(neurons_spks, region, bins=50):
    neurons_count = neurons_spks.shape[0]
    spks_per_trial = [np.sum(neurons_spks[neuron]) for neuron in range(neurons_count)]
    plt.hist(spks_per_trial, bins=bins);
    plt.xlabel("total number of spikes")
    plt.ylabel("number of neurons")
    plt.title(f"spiking activity; region: {region}")
    plt.show()

def plot_spiking_histogram_neurons_in_regions(data, regions, bins=50):
    for region in regions:
        neurons = data['brain_area'] == region
        neurons_spks = data['spks'][neurons]
        neurons_count = neurons_spks.shape[0]
        spks_per_trial = [np.sum(neurons_spks[neuron]) for neuron in range(neurons_count)]
        plt.hist(spks_per_trial, bins=bins);
        plt.title(f"region: {region}")
        plt.xlabel("total number of spikes")
        plt.ylabel("number of neurons")
        plt.show()

def plot_average_activity_neurons_all_trials(neurons_spks, region, sigma=2, sort=True):
    avg_activity = np.mean(neurons_spks, axis=1)
    total_act = np.sum(avg_activity, axis=1)

    fig = plt.figure(dpi=150)

    # sort by total activity
    if sort:
        avg_acitivity_sorted = [x for _,x in sorted(zip(total_act,np.arange(0,avg_activity.shape[0])))]
        plt.imshow(gaussian_filter1d(avg_activity[avg_acitivity_sorted], sigma, axis=1), cmap='gray_r', alpha=1);
    else:
        plt.imshow(avg_activity, cmap='gray_r', alpha=1);
#         plt.colorbar()
    plt.axvline(50, color="limegreen", label="stimulus onset")
    plt.title(f"avg activity; region: {region}")
    plt.xlabel("time bin")
    plt.ylabel(f"neuron")
    plt.legend()
    plt.show()
        
def plot_average_activity_neurons_in_regions(data, regions, sigma=2, sort=True):
    for region in regions:
        neurons = data['brain_area'] == region
        neurons_spks = data['spks'][neurons]

        avg_activity = np.mean(neurons_spks, axis=1)
        total_act = np.sum(avg_activity, axis=1)

        fig = plt.figure(dpi=150)
        
        # sort by total activity
        if sort:
            avg_acitivity_sorted = [x for _,x in sorted(zip(total_act,np.arange(0,avg_activity.shape[0])))]
            plt.imshow(gaussian_filter1d(avg_activity[avg_acitivity_sorted], sigma, axis=1), cmap='gray_r', alpha=1);
        else:
            plt.imshow(gaussian_filter1d(avg_activity, sigma, axis=1), cmap='gray_r', alpha=1);
#         plt.colorbar()
        plt.axvline(50, color="limegreen", label="stimulus onset")
        plt.title(f"avg activity; region: {region}")
        plt.xlabel("time bin")
        plt.ylabel(f"neuron")
        plt.legend()
        plt.show()
        
def plot_per_trial_activity(neurons_spks, region, gocue=None, response_time=None):
    neurons_count = neurons_spks.shape[0]
    for neuron in range(neurons_count):
        fig = plt.figure(dpi=150)
        plt.imshow(neurons_spks[neuron], cmap='gray_r', alpha=1);
        plt.colorbar()
        if gocue is not None:
            plt.imshow(gocue[neuron], cmap='magma', alpha=0.25);
        if response_time is not None:
            plt.imshow(response_time[neuron], cmap='magma', alpha=0.25);
        plt.axvline(50, color="limegreen", label="stimulus onset")
        plt.xlabel("time bin")
        plt.ylabel(f"neuron {neuron}; trials")
        plt.title(f"per trial activity; region: {region}")
        plt.legend()
        plt.show()
        
def psth(neurons_spks, region, timebin_size=1):
    total_activity = np.sum(neurons_spks, axis=1)
    total_activity = np.sum(total_activity, axis=0)
    
    # combine bins according to timebin_size
    tas = total_activity.shape[0]
    total_activity = total_activity.reshape([tas//timebin_size, -1])
    total_activity = np.sum(total_activity, axis=1)
    
    fig = plt.figure(dpi=150)

    plt.bar(np.arange(total_activity.shape[0]), total_activity)
    plt.axvline(50//timebin_size, color="limegreen", label="stimulus onset")
    plt.title(f"PSTH; region: {region}")
    plt.xlabel("time bin")
    plt.ylabel(f"spike count")
    plt.ylim([np.min(total_activity), np.max(total_activity)*1.25])
    plt.legend()
    plt.show()