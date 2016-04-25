# FUNCTIONS TO CREATE THE HISTIMES FOR PSTH OF THE FORWARD STIM FOR 
# Functions in this file:
#	- read_stimulus(expe,meas):
#	- readkwikinfo(kwik, grupete=3):
#	- readVtag(Vtag1,stim,stimtype):
#	- BuildPSTH(stim,stimtype, Spikes, sampling_freq, t_before, t_after,starts,stops,exp,meas) :
#	- PSTH_spikes(stimulation, stimtype, stimtimes, spikes, samp, t_before, t_after, starts, stops):

from phy.io import KwikModel
from attrdict import AttrDict
import numpy as np
from numpy import*

#----------------------------------------------------------------------------------------
# READ STIMULUS
#----------------------------------------------------------------------------------------
# Here we read the binary file with stimulus: 902 of 25 piezos x 1024 samples
# Text file has the type of stimulus: F sparse, C correlated, U uncorrelated
def read_stimulus(expe,meas,binname,textname):
    ## This function reads the stimulus binary file, reads the type of stimulus,
    ## and stores it in a matrix and a row vector
    
    bin_file = open(binname,'rb')
    read_data = np.fromfile(file=bin_file, dtype=np.float32)
    read_data = read_data.reshape((-1,25,10240)) # reshapes data assuming 25 whiskers, 10240 time bins
    txt_data = np.loadtxt(textname, dtype='S8') # Makes sure data type is text decoded
    txt_data = txt_data.view(np.chararray).decode('utf-8') # Makes sure data type is text decoded
    
    length2=0
    
    if expe==22 and meas[0:2] == 'm1':  #measurement 1 composed of two recorded
        length1=902
        length2 =93
        
    if expe == 20 and meas[0:2]=='m3': #there are 46 events in exp2 and 879 in exp3
        length1 = 46 
        length2 = 879
    
    if length2>0:
        txt_data = np.append(txt_data[0:length1], txt_data[0:length2])
        read_data = np.append(read_data[0:length1], read_data[0:length2],0)
        read_data = read_data.reshape((-1,25,10240)) # reshapes data assuming 25 whiskers, 10240 time bins
            
    bin_file.close()
    
    return read_data, txt_data

#----------------------------------------------------------------------------------------
# READKWIKINFO
#----------------------------------------------------------------------------------------
# We read the data of the output from klusterkwik: spike times and cluster-number of each
# cluster-number is in klustaviewa series (can be as high as 130 e.g.)
# Grupete stands for cluster groups! 2: good clusters, 1: multiunits, 0: unsorted, 3: noise
def readkwikinfo(kwik, grupete=3):
    model = KwikModel(kwik) # load kwik model from file
    spiketimes = model.spike_times # extract the absolute spike times
    clusters = model.cluster_groups # extract the cluster names
    sample_rate = model.sample_rate # extract sampling freq
    
    spikedata = {} # initialise dictionary
    for cluster in clusters.keys():
        clustergroup = clusters[cluster]
        if clustergroup==grupete: # only look at specified type of cluster, 0 = noise, 1 = MUA, 2 = GOOD, 3 = unsorted
            spiketimematrix = AttrDict({'spike_times': np.zeros(len(spiketimes[where(model.spike_clusters==cluster)]))})
            spiketimematrix.spike_times = spiketimes[where(model.spike_clusters==cluster)]
            spikedata[cluster] = spiketimematrix # data structure is a dictionary with attribute accessible spiketimes
            # attribute accessible means that spikedata.spike_times works, normal dictionaries would be spikedata[spike_times]
    
    model.close()
    
    return spikedata, sample_rate

#----------------------------------------------------------------------------------------
# READ VTAG
#----------------------------------------------------------------------------------------
def readVtag(Vtag1,stim,stimtype,sampling_freq):
    ## The first task is to find the stimulus onset times for each whisker in each sweep in each direction
    start_and_stops = Vtag1[1:] - Vtag1[:-1]
    starts = (where(start_and_stops==1)[0]-2999)/float(sampling_freq) # time in seconds
    stops = (where(start_and_stops==-1)[0]+4110)/float(sampling_freq) # time in seconds
    
    stim_ret = stim[0:len(stops),:,:]
    stimtype_ret = stimtype[0:len(stops)]
    
    return stim_ret, stimtype_ret, starts, stops

#----------------------------------------------------------------------------------------
# BUILDS PSTH
#----------------------------------------------------------------------------------------
def BuildPSTH(stim,stimtype, Spikes, sampling_freq, t_before, t_after,starts,stops,exp,meas) :
## The first task is to find the stimulus onset times for each whisker in each sweep in each direction
    #stim, stimtype = read_stimulus()
    stim = stim[np.where(stimtype=='F')[0], :, :]
    starts = starts[np.where(stimtype=='F')[0]]
    stops = stops[np.where(stimtype=='F')[0]]
    
    stimtimes = {}
    for w in np.arange(25, dtype='int') :  
        timesUP = []
        timesDOWN = []
        for i in np.arange(len(stim), dtype='int') :
            indsUP = (np.where(stim[i, w, :]==1108.8889)[0]-1)[::2]
            # This finds all time points where the stim = 1108.8889, because each ramp has two 1108.8889 values
            # (on the way up and on the way down) we take every other index using [::2]
            timesUP.append(indsUP)
            indsDOWN = (np.where(stim[i, w, :]==-1108.8889)[0]-1)[::2]
            # This finds all time points where the stim = -1108.8889, because each ramp has two -1108.8889 values
            # (on the way up and on the way down) we take every other index using [::2]
            timesDOWN.append(indsDOWN)
        stimtimes[w] = timesUP, timesDOWN # stimtimes[whisker][0][:]=UP stimtimes[whisker][1][:]=DOWN
    
    # make an 'output dict'
    # the PSTH will be built on -tbefore:tafter
    hist_inds = {}
    PSTH = {}
    psth = dict()
    psth_times = dict()
    
    # Loop each neuron and get the spikes.
    for neuron in list(Spikes.keys()): 
        codename = 'exp'+ str(exp) + '_' + str(meas) + '_c' + str(neuron)
        
        psth = AttrDict({'clusnum': neuron,'exp' : int(exp) , 'meas': int(meas[1]) , 'shank': int(meas[3])})
        
        psth.update(AttrDict({'psth_counts': [] , 'psth_times': [] , 'psth_length': [t_before,t_after] }))
        
        psth['psth_counts'], psth['psth_times'] = PSTH_spikes(stim, stimtype, stimtimes, Spikes[neuron].spike_times, sampling_freq, t_before, t_after, starts, stops)
        
        PSTH[codename] = psth
       
    return PSTH

#----------------------------------------------------------------------------------------

def PSTH_spikes(stimulation, stimtype, stimtimes, spikes, samp, t_before, t_after, starts, stops):
    """
    stimulation   : a list of numpy arrays with a n*t stimulus inside
    stimtimes     : a list of the times the stimulus occurred for each whisker 
    spikes        : an array that contains the spike times (s)
    Vtag1         : synchronises stimulus with spike times
    samp          : sampling rate of the stimulation (Hz)
    t_before      : duration before the stim (positive, s)
    t_after       : duration after the stim (positive, s)
    starts        : the start of the F sweeps
    stops         : the stops of the F sweeps
    """
    
    stim_samp = 1/.0009997575757
    
    PSTH_spike_counts = {}
    for w in np.arange(25, dtype='int') :
        spikecountsup = 0
        spikecountsdown = 0
        for i in np.arange(len(stimulation), dtype='int') : 
            for x in np.arange(len(stimtimes[w][0][i]), dtype='int') :  # we must look at the number of stimulations per whisker per stimulation block and this is no longer 4        
                timesUP = starts[i] + stimtimes[w][0][i][x]/stim_samp # stimtimes is now stimtimes[whisker][0 for UP, 1 for DOWN][stimsweep][trial]
                spikecountsup += len(spikes[(timesUP - t_before < spikes) * (spikes < timesUP + t_after)]) # count spikes that are within PSTH window of stimtimes
            for y in np.arange(len(stimtimes[w][1][i]), dtype='int') : # for the DOWN stimuli we must have a separate loop because they also are now randomly distributed and not 4
                timesDOWN = starts[i] + stimtimes[w][1][i][y]/stim_samp                
                spikecountsdown += len(spikes[(timesDOWN - t_before < spikes) * (spikes < timesDOWN + t_after)])
        PSTH_spike_counts[w] = spikecountsup, spikecountsdown
    
    hist_inds = {} #same changes for this block, each loop will change length depending on how many stimulations fall in a sweep
    for w in np.arange(25, dtype='int') :
        hist_inds[w] = np.zeros(PSTH_spike_counts[w][0]), np.zeros(PSTH_spike_counts[w][1])
        spikecountsup = 0
        spikecountsdown = 0
        for i in np.arange(len(stimulation), dtype='int') : 
            for x in np.arange(len(stimtimes[w][0][i]), dtype='int') :     # dynamic loop depends on how many stims fall in sweep      
                timesUP = starts[i] + stimtimes[w][0][i][x]/stim_samp
                spikecountup = len(spikes[(timesUP - t_before < spikes) * (spikes < timesUP + t_after)])
                spikeidxup = spikes[(timesUP - t_before < spikes) * (spikes < timesUP + t_after)]
                #spikeidxup = ((spikeidxup - starts[i])/float(stops[i] - starts[i])*len(stimulation[i,0]))
                hist_inds[w][0][spikecountsup:(spikecountsup+spikecountup)] = spikeidxup-timesUP#stimtimes[w][0][i][x]/float(stops[i] - starts[i])*len(stimulation[i,0])
                spikecountsup += spikecountup
            
            for y in np.arange(len(stimtimes[w][1][i]), dtype='int') :     # dynamic loop depends on how many stims fall in sweep
                timesDOWN = starts[i] + stimtimes[w][1][i][y]/stim_samp                
                spikecountdown = len(spikes[(timesDOWN - t_before < spikes) * (spikes < timesDOWN + t_after)])
                spikeidxdown = spikes[(timesDOWN - t_before < spikes) * (spikes < timesDOWN + t_after)]
                #spikeidxdown = ((spikeidxdown - starts[i])/float(stops[i] - starts[i])*len(stimulation[i,0]))
                hist_inds[w][1][spikecountsdown:(spikecountsdown+spikecountdown)] = spikeidxdown-timesDOWN#stimtimes[w][1][i][y]/float(stops[i] - starts[i])*len(stimulation[i,0])
                spikecountsdown += spikecountdown
                
    return PSTH_spike_counts, hist_inds

# March 25 we took out the rounding fronm this function, to keep the actual times with respect to stim.
# April modified a little to be more precise with absolute times.
