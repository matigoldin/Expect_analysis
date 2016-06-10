# FUNCTIONS TO BUILD PSTHs

# Functions in this file:
"""
get_ep_duration:     gets epduration from a manually generated file. I have to change this to read the actual time in ms in the new Params.txt file

get_stimtimes:       gets the times and stim file, reads them as a list and divides it in an arrays with each line as one element

build_hist_dict:     creates an empty dictionary with all the tree structure to fill it with spiketimes for each different stim, and spike counts

build_dict_stim:     creates a dictionary of stim labels codes for each variable. For ex. rep, isi, etc are arrays of ep x st_per_episode with the label code to tag that time.

readkwikinfo:        reads spiketimes

BuildPSTH:           fills the dictionary created with the previous function hist_dict with the data and using dict_stim

"""

from attrdict import AttrDict
import numpy as np
from phy.io import KwikModel



#---------------------------------------------------------
# GET EPDURATION
#---------------------------------------------------------
def get_ep_duration(eptimefile):
    
    eptimesf = open(eptimefile, 'r')
    eptimes = [float(x)/30 for x in eptimesf.read().split()]
    eptimesf.close()
   
    return eptimes

#---------------------------------------------------------
# GET STIMTIMES
#---------------------------------------------------------
def get_stimtimes(stimfile,timefile):
    
    stims = open(stimfile, 'r')
    times = open(timefile, 'r')
    
    stimdata = stims.read().splitlines()
    timedata = times.read().splitlines()
 
    stims.close()
    times.close()
    
    return stimdata, timedata
#---------------------------------------------------------
# BUILD DICT STIM, reads stims and times of .txt files of experiments
#---------------------------------------------------------
def build_dict_stim(stimfile, timefile, epdurationfile):

    stims, times = get_stimtimes(stimfile,timefile)
    #------------------------------------------
    # count number of episodes
    episodes=1
    stims_ep=0
    for time in times[:-1]:             #last line is blank, we skip it
        if time == '': 
            episodes+=1
        if episodes ==1:
            stims_ep+=1
    print('   Total episodes: ', episodes)        
    print('   Total stims per episode: ', stims_ep)        
    #------------------------------------------
    # get episode duration
    ep_duration = get_ep_duration(epdurationfile)
    ####
    # for the formatting I have now:           #####################X   XXXXXXXXXXXXXXXXXX
    ep_length = ep_duration[6]
    
    ###
    #------------------------------------------
    # starting times of each stimulus
    starts = np.zeros([episodes, stims_ep])
    tot_stims = episodes*stims_ep

    st_count=0
    for t in times[:-1]:
        if t!='':
            st = st_count % stims_ep
            ep = st_count // stims_ep 
            starts[ep,st] = float(t) + ep*ep_length
            st_count+=1
    #------------------------------------------
    # stims        
    st_pad = np.zeros([episodes,stims_ep],dtype=int) # 1 row, 2 arc, 3 pad
    st_types = np.zeros([episodes,stims_ep],dtype=int) # 1 hold, 2 pass, 3 release        
    st_isi = np.zeros([episodes,stims_ep],dtype=int) # 10 , 20, 50
    st_rep = np.zeros([episodes,stims_ep],dtype=int) # 2, 5, 10
    st_ctrl = np.zeros([episodes,stims_ep],dtype=int) # 0, blank, 1 ctrl1, 2 ctrl2, 3 ctrl3, 10 normal 
    # dictionary of stims
    st_logic = {} 
    st_logic['pad'] = {'1' : 'ROW' , '2' : 'ARC'  , '3': 'PAD' }
    st_logic['types'] = { '1':'hold', '2': 'pass'  , '3': 'release'}
    st_logic['ctrl'] = {'0' : 'BLANK', '1' : 'Ctrl1', '2' : 'Ctrl2', '3' : 'Ctrl3', '10' : 'Normal'}

    ep=0
    st=0
    # get stims
    for stim in stims[:-3]:           #last three lines useless
        line = stim.split()
        if line and ep<episodes:

            if line[1]=='BLANK':
                st+=1
                if st%stims_ep==0:
                    st=0
                    ep+=1
            elif len(line)>3:
                if line[1][1:4]=='ROW': st_pad[ep,st]=1
                elif line[1][1:4]=='ARC': st_pad[ep,st]=2
                elif line[1][1:4]=='PAD': st_pad[ep,st]=3

                if line[1][5:-1]=='Hold': st_types[ep,st]=1
                elif line[1][5:-1]=='Pass': st_types[ep,st]=2
                elif line[1][5:-1]=='Release': st_types[ep,st]=3

                if line[3]=='REP_2': st_rep[ep,st]=2
                elif line[3]=='REP_5': st_rep[ep,st]=5
                elif line[3]=='REP_10': st_rep[ep,st]=10

                if line[5]=='ISI_10': st_isi[ep,st]=10
                elif line[5]=='ISI_20': st_isi[ep,st]=20
                elif line[5]=='ISI_50': st_isi[ep,st]=50
                    
                if line[7]=='Normal': st_ctrl[ep,st]=10
                elif line[7][0:5]=='Ctrl1': st_ctrl[ep,st]=1
                elif line[7][0:5]=='Ctrl2': st_ctrl[ep,st]=2
                elif line[7][0:5]=='Ctrl3': st_ctrl[ep,st]=3
                elif line[7][0:5]=='Ctrl4': st_ctrl[ep,st]=4

                st+=1
                if st%stims_ep==0:
                    st=0
                    ep+=1

    Stim_dict = AttrDict({'st_logic':st_logic, 'episodes': episodes  ,'stims_ep':stims_ep  ,'st_times': starts})
    Stim_dict.update({'st_isi':st_isi,'st_rep':st_rep,'st_types':st_types,'st_ctrl': st_ctrl,'st_pad':st_pad})
    
    return Stim_dict

#----------------------------------------------------------------------------------------
# BUILD HIST DICTIONARY
#----------------------------------------------------------------------------------------
import copy as cp

def build_hist_dict():
    isis = [10,20,50]
    reps = [2,5,10]
    pads = ['ARC','ROW','PAD']
    types = ['hold','pass','release']
    
    Isis ={}
    for i in isis:
        Isis[i]= []
    
    Reps ={}
    for r in reps:
        Reps[r] = cp.deepcopy(Isis)
    
    Pads = {}
    for p in pads:
        Pads[p] = cp.deepcopy(Reps)
    
    Types = {}
    for t in types:
        Types[t] = cp.deepcopy(Pads)
    
    Normal = cp.deepcopy(Types)
    Ctrl1 = cp.deepcopy(Types)
    Ctrl2 = cp.deepcopy(Types)
    Ctrl3 = cp.deepcopy(Types)
    Ctrl4 = cp.deepcopy(Types)
    #----------------------------------------
    #for counnts
    Isisc ={}
    for i in isis:
        Isisc[i]= 0
    
    Repsc ={}
    for r in reps:
        Repsc[r] = cp.deepcopy(Isisc)
    
    Padsc = {}
    for p in pads:
        Padsc[p] = cp.deepcopy(Repsc)
    
    Typesc = {}
    for t in types:
        Typesc[t] = cp.deepcopy(Padsc)
        
    Normalc = cp.deepcopy(Typesc)
    
    counts_n = cp.deepcopy(Normalc)
    counts_c1 = cp.deepcopy(Normalc)
    counts_c2 = cp.deepcopy(Normalc)
    counts_c3 = cp.deepcopy(Normalc)
    counts_c4 = cp.deepcopy(Normalc)
    
    Counts ={}
    Counts['Normal'] = counts_n
    Counts['Ctrl1'] = counts_c1
    Counts['Ctrl2'] = counts_c2
    Counts['Ctrl3'] = counts_c3
    Counts['Ctrl4'] = counts_c4
    Counts['BLANK'] = 0
    
    hist_logic = 'Type x Pad x Rep x Isi'
    histo = AttrDict({ 'BLANK' :[],  'Normal': Normal, 'Ctrl1':Ctrl1 , 'Ctrl2':Ctrl2 , 'Ctrl3': Ctrl3, 'Ctrl4': Ctrl4 , 'hist_logic': hist_logic, 'Counts':Counts})

    return histo
    
#----------------------------------------------------------------------------------------
# READKWIKINFO
#----------------------------------------------------------------------------------------
# We read the data of the output from klusterkwik: spike times and cluster-number of each
# cluster-number is in klustaviewa series (can be as high as 130 e.g.)
# Grupete stands for cluster groups! 2: good clusters, 1: multiunits, 0: unsorted, 3: noise
def readkwikinfo(kwik, grupete=2):
    model = KwikModel(kwik) # load kwik model from file
    spiketimes = model.spike_times # extract the absolute spike times
    clusters = model.cluster_groups # extract the cluster names
    sample_rate = model.sample_rate # extract sampling freq
    
    spikedata = {} # initialise dictionary
    for cluster in clusters.keys():
        clustergroup = clusters[cluster]
        if clustergroup==grupete: # only look at specified type of cluster, 0 = noise, 1 = MUA, 2 = GOOD, 3 = unsorted
            spiketimematrix = AttrDict({'spike_times': np.zeros(len(spiketimes[np.where(model.spike_clusters==cluster)]))})
            spiketimematrix.spike_times = spiketimes[np.where(model.spike_clusters==cluster)]
            spikedata[cluster] = spiketimematrix # data structure is a dictionary with attribute accessible spiketimes
            # attribute accessible means that spikedata.spike_times works, normal dictionaries would be spikedata[spike_times]
    
    model.close()
    
    return spikedata, sample_rate

#----------------------------------------------------------------------------------------
# BUILDS PSTH
#----------------------------------------------------------------------------------------
def BuildPSTH(Stims, Spikes, sampling_freq, exp, meas):
    
    stimtimes = {}
    stim_samp = 1/.0009997575757
    # make an 'output dict'
    # the PSTH will be built on -tbefore:tafter
    PSTH_times = {}
    
    # Loop each neuron and get the spikes.
    for neuron in list(Spikes.keys()): 
        codename = 'exp'+ str(exp) + '_' + str(meas) + '_c' + str(neuron)
        psth = AttrDict({'clusnum': neuron,'exp' : int(exp) , 'meas': int(meas[1]) , 'shank': int(meas[3])})
        psth.update(AttrDict({'psth_counts': [] , 'psth_times': []}))
        
        histo= build_hist_dict()
        spikes = Spikes[neuron].spike_times*1000 #(want them in ms)
        
        #loop episodes and stims_per_episode, and populate the histograms
        for ep in np.arange(Stims.episodes):
            for se in np.arange(Stims.stims_ep):
                
                code = str(int(Stims.st_ctrl[ep][se]))
                c = str(Stims.st_logic.ctrl[code])
                                
                if code=='0':
                    t_after=500
                    if len(spikes[(start <= spikes) * (spikes <= start + t_after)])>0:
                        histo[c].extend(spikes[(start <= spikes) * (spikes <= start + t_after)]-start)
                        histo['Counts'][c] +=  len(spikes[(start <= spikes) * (spikes <= start + t_after)])
                else:
                    code = str(int(Stims.st_types[ep][se]))                                                
                    t = str(Stims.st_logic.types[code])
                
                    code = str(int(Stims.st_pad[ep][se]))
                    p = Stims.st_logic.pad[code]
                    
                    r = Stims.st_rep[ep][se]
                    i = Stims.st_isi[ep][se]
                    start = Stims.st_times[ep][se]
                              
                    t_after = 500*r
                    if len(spikes[(start <= spikes) * (spikes <= start + t_after)])>0:
                        histo[c][t][p][r][i].extend(spikes[(start <= spikes) * (spikes <= start + t_after)]-start)
                        histo['Counts'][c][t][p][r][i]  += len((spikes[(start <= spikes) * (spikes <= start + t_after)]))
                                                       
        PSTH_times[codename] = histo
       
    return PSTH_times
