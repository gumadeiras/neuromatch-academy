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

def filter_contralateral_trials_full_contrast(data, regions):
    cl_trials_data = []
    for dat in data:
        region_filter_idx = np.where([(dat['brain_area'][idx] in regions) for idx, __ in enumerate(dat['brain_area'])])[0]
        if any(region_filter_idx):
            contralateral_trials_idx = np.where((dat['contrast_left']==0) & (dat['contrast_right']==1))[0]
            mouse_name = dat['mouse_name']
            # filter neurons by regions
            mouse_spikes = dat['spks'][region_filter_idx]
            # filter neurons by contralateral trials
            mouse_spikes = mouse_spikes[:,contralateral_trials_idx]
            mouse_regions = dat['brain_area'][region_filter_idx]
            mouse_gocue = dat['gocue'][contralateral_trials_idx]
            mouse_resptime = dat['response_time'][contralateral_trials_idx]
            mouse_wheel = dat['wheel'][0][contralateral_trials_idx]
            mouse_feedback = dat['feedback_time'][contralateral_trials_idx]
            mouse_response = dat['response'][contralateral_trials_idx]
            cl_trials_data.append([mouse_name, mouse_spikes, mouse_regions, mouse_gocue, mouse_resptime, mouse_wheel, mouse_feedback, mouse_response])
    return np.asarray(cl_trials_data)

def filter_contralateral_by_region(data, region):
    combined_data = []
    # iterate recordings
    for recording in data:
        region_idx = np.where((recording[2] == region))[0]
        if any(region_idx):
            mouse_name = recording[0]
            # filter neurons by regions
            mouse_spikes = recording[1]
            # filter neurons by region
            mouse_spikes = mouse_spikes[region_idx]
            mouse_regions = recording[2][region_idx]
            mouse_gocue = recording[3]
            mouse_resptime = recording[4]
            mouse_wheel = recording[5]
            mouse_feedback = recording[6]
            mouse_response = recording[7]
            combined_data.append([mouse_name, mouse_spikes, mouse_regions, mouse_gocue, mouse_resptime, mouse_wheel, mouse_feedback, mouse_response])

    return np.asarray(combined_data)