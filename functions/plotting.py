import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

def plot_spiking_histogram_neurons_all_trials(neurons_spks, region, bins=50, save_path='./data.png', save=False):
    neurons_count = neurons_spks.shape[0]
    spks_per_trial = [np.sum(neurons_spks[neuron]) for neuron in range(neurons_count)]
    plt.hist(spks_per_trial, bins=bins);
    plt.xlabel("total number of spikes")
    plt.ylabel("number of neurons")
    plt.title(f"spiking activity; region: {region}")
    
    if(save):
        plt.draw()
        plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
        plt.close()
    else:
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

def plot_average_activity_neurons_all_trials(neurons_spks, region, sigma=2, sort=True, save_path='./data.png', save=False):
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

    if(save):
        plt.draw()
        plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
        plt.close()
    else:
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