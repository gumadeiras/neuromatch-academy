import numpy as np
import matplotlib.pyplot as plt

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

def plot_average_activity_neurons_all_trials(neurons_spks, region, sort=True):
    avg_activity = np.mean(neurons_spks, axis=1)
    total_act = np.sum(avg_activity, axis=1)

    fig = plt.figure(dpi=150)

    # sort by total activity
    if sort:
        avg_acitivity_sorted = [x for _,x in sorted(zip(total_act,np.arange(0,avg_activity.shape[0])))]
        plt.imshow(avg_activity[avg_acitivity_sorted], cmap='gray_r', alpha=1);
    else:
        plt.imshow(avg_activity, cmap='gray_r', alpha=1);
#         plt.colorbar()
    plt.title(f"avg activity; region: {region}")
    plt.xlabel("time bin")
    plt.ylabel(f"neuron")
    plt.show()
        
def plot_average_activity_neurons_in_regions(data, regions, sort=True):
    for region in regions:
        neurons = data['brain_area'] == region
        neurons_spks = data['spks'][neurons]

        avg_activity = np.mean(neurons_spks, axis=1)
        total_act = np.sum(avg_activity, axis=1)

        fig = plt.figure(dpi=150)
        
        # sort by total activity
        if sort:
            avg_acitivity_sorted = [x for _,x in sorted(zip(total_act,np.arange(0,avg_activity.shape[0])))]
            plt.imshow(avg_activity[avg_acitivity_sorted], cmap='gray_r', alpha=1);
        else:
            plt.imshow(avg_activity, cmap='gray_r', alpha=1);
#         plt.colorbar()
        plt.title(f"avg activity; region: {region}")
        plt.xlabel("time bin")
        plt.ylabel(f"neuron")
        plt.show()
        
def plot_per_trial_activity(neurons_spks, region):
    neurons_count = neurons_spks.shape[0]
    for neuron in range(neurons_count):
        fig = plt.figure(dpi=150)
        plt.imshow(neurons_spks[neuron], cmap='gray_r', alpha=1);
        plt.colorbar()
        plt.xlabel("time bin")
        plt.ylabel(f"neuron {neuron}; trials")
        plt.title(f"per trial activity; region: {region}")
        plt.show()