import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

def save_or_plot(save_path, save):
    if(save):
        plt.draw()
        plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
        plt.close()
    else:
        plt.show()

def plot_spiking_histogram_neurons_all_trials(neurons_spks, region, bins=50, save_path='./data.png', save=False):
    neurons_count = neurons_spks.shape[0]
    spks_per_trial = [np.sum(neurons_spks[neuron]) for neuron in range(neurons_count)]
    plt.hist(spks_per_trial, bins=bins);
    plt.xlabel("total number of spikes")
    plt.ylabel("number of neurons")
    plt.title(f"spiking activity; region: {region}")
    save_or_plot(save_path, save)


def plot_spiking_histogram_neurons_in_regions(data, regions, bins=50, save_path='./data.png', save=False):
    for region in regions:
        neurons = data['brain_area'] == region
        neurons_spks = data['spks'][neurons]
        neurons_count = neurons_spks.shape[0]
        spks_per_trial = [np.sum(neurons_spks[neuron]) for neuron in range(neurons_count)]
        plt.hist(spks_per_trial, bins=bins);
        plt.title(f"region: {region}")
        plt.xlabel("total number of spikes")
        plt.ylabel("number of neurons")
        save_or_plot(save_path, save)

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
    save_or_plot(save_path, save)
        
def plot_average_activity_neurons_in_regions(data, regions, sigma=2, sort=True, save_path='./data.png', save=False):
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
        save_or_plot(save_path, save)
        
def plot_per_trial_activity(neurons_spks, region, gocue=None, response_time=None, save_path='./data.png', save=False):
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
        save_or_plot(save_path, save)

def psth(neurons_spks, region, timebin_size=1, func=np.mean, sigma=3, save_path='./data.png', save=False):
    total_activity = func(neurons_spks, axis=1)
    total_activity = np.sum(total_activity, axis=0)
    
    # combine bins according to timebin_size
    tas = total_activity.shape[0]
    total_activity = total_activity.reshape([tas//timebin_size, -1])
    total_activity = np.sum(total_activity, axis=1)
    
    fig = plt.figure(dpi=150)

    plt.step(np.arange(total_activity.shape[0]), gaussian_filter1d(total_activity, sigma))
    plt.axvline(50//timebin_size, color="limegreen", label="stimulus onset")
    plt.title(f"PSTH; region: {region}")
    plt.xlabel("time bin")
    plt.ylabel(f"spike count")
    plt.ylim([np.min(total_activity), np.max(total_activity)*1.25])
    plt.legend()
    save_or_plot(save_path, save)

def psth_combined(alldat, region, timebin_size=1, func=np.mean, sigma=3, save_path='./data.png', save=False):
    fig = plt.figure(dpi=150)
    tas_max = 0
    mmax = 0
    for dat in alldat:
        neurons = dat['brain_area'] == region
        neurons_spks = dat['spks'][neurons]
        neurons_count = neurons_spks.shape[0]
        total_neurons_count = dat['spks'].shape[0]
        trials_count = dat['spks'].shape[1]
        if neurons_count > 1:
            total_activity = func(neurons_spks, axis=1)
            total_activity = np.sum(total_activity, axis=0)
            # combine bins according to timebin_size
            tas = total_activity.shape[0]
            total_activity = total_activity.reshape([tas//timebin_size, -1])
            total_activity = np.sum(total_activity, axis=1)
            tas_max = np.max(total_activity)
            
            plt.step(np.arange(total_activity.shape[0]), gaussian_filter1d(total_activity, sigma), label=dat['mouse_name'])
        mmax = tas_max if tas_max > mmax else mmax
    plt.axvline(50//timebin_size, color="limegreen", label="stimulus onset")
    plt.title(f"PSTH; region: {region}")
    plt.xlabel("time bin")
    plt.ylabel(f"spike count")
    plt.ylim([0, mmax])
    plt.legend()
    save_or_plot(save_path, save)

def plot_wheel_movement(trial, wheel_to_mm=0.135, sigma=3):
    plt.plot(gaussian_filter1d(trial*wheel_to_mm, 3))
    plt.axvline(50, color="limegreen", label="stimulus onset")
    plt.xlabel("time bin")
    plt.ylabel(f"wheel position (mm)")
    plt.title(f"wheel position x time")
    plt.legend()
    plt.show()