import numpy as np

def recordings_with_region(data, region):
    # returns recording index that has a region and number of recorded neurons
    recorded_with_region = []
    for idx, dat in enumerate(data):
        regions, count = np.unique(dat['brain_area'], return_counts=True)
        if region in regions:
            pos = np.where(dat['brain_area'] == region)[0]
            recorded_with_region.append([idx, pos.shape[0]])

    return np.vstack(recorded_with_region)

def regions_recorded(data):
    # returns all regions recorded
    recorded_regions = np.array([])
    for idx, dat in enumerate(data):
        # recorded brain regions
        regions, count = np.unique(dat['brain_area'], return_counts=True)
        recorded_regions = np.hstack([regions, recorded_regions])
        
    recorded_regions, animal_count = np.unique(recorded_regions, return_counts=True)
    return list(zip(recorded_regions, animal_count))

def regions_recorded_per_animal(data):
    # returns regions recorded per animal
    recorded_regions = []
    for idx, dat in enumerate(data):
        # recorded brain regions
        regions, count = np.unique(dat['brain_area'], return_counts=True)
        recorded_regions.append([idx, list(zip(regions, count))])

    return np.vstack(recorded_regions)


def get_times_for_neuron(neurons_spks, times, stim_onset=50):
    # generates a neurons_spks-like array with 1 where times happens and 0 everywhere else
    neurons_count = neurons_spks.shape[0]
    trials_count = neurons_spks.shape[1]
    neurons_responses = np.zeros_like(neurons_spks)
    response_time_bins = np.asarray((times*10)+stim_onset).ravel().astype(np.int)
    for neuron in range(neurons_count):
        for trial in range(trials_count):
            neurons_responses[neuron][trial][response_time_bins[trial]] = 1
    return neurons_responses