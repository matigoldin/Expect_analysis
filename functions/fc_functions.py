# FC functions

import numpy as np
from matplotlib import *

import matplotlib.pyplot as plt


# You apply this to file random-FC-sequence.txt

def FCsequence(episodes):

    here = os.getcwd()
    textname =  here + '/random-FC-sequence.txt'

    txt_data = np.array(np.loadtxt(textname)[0:50*episodes])

    #txt_out = np.append((txt_data[:,0]-1)*5+txt_data[:,1].T,,axis=1)

    txt_out = np.append(np.array([(txt_data[:,1]-1)*5+txt_data[:,0]-1 ]).T, (np.array([txt_data[:,2]])-1).T, axis=1)

    return txt_out.reshape((episodes,50,2))


#----------------------------------------------------------------------------------------
# FCtimes
#----------------------------------------------------------------------------------------
def FCtimes():

    times=np.array([101.667,
            151.7,
            201.667,
            251.7,
            301.733,
            351.667,
            401.7,
            451.633,
            501.667,
            551.7,
            601.633,
            651.7,
            701.633,
            751.667,
            801.7,
            851.633,
            901.667,
            951.7,
            1001.633,
            1051.667,
            1101.633,
            1151.667,
            1201.7,
            1251.633,
            1301.667,
            1351.6,
            1401.633,
            1451.667,
            1501.6,
            1551.667,
            1601.6,
            1651.633,
            1701.667,
            1751.6,
            1801.633,
            1851.567,
            1901.6,
            1951.633,
            2001.6,
            2051.633,
            2101.567,
            2151.6,
            2201.633,
            2251.567,
            2301.6,
            2351.633,
            2401.567,
            2451.633,
            2501.567,
            2551.6])
    return times


from phy.io import KwikModel
from attrdict import AttrDict

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


#Making the 50 psth time_lists


#starts are FCtimes
#timesUP and timesDOWNS are your FCtimes arranged with FCsequence
#codename: how you label your neuron
#----------------------------------------------------------------------------------------
# BUILDS PSTH
#----------------------------------------------------------------------------------------
def BuildPSTH(Spikes, sampling_freq, t_before, t_after, starts, exp, meas, episodenbr) :
## The first task is to find the stimulus onset times for each whisker in each sweep in each direction

    # make an 'output dict'
    # the PSTH will be built on -tbefore:tafter
    hist_inds = {}
    PSTH = {}
    psth = dict()
    psth_times = dict()
    stimtimes = {w : {0: [], 1 : []} for w in range(25)}
    sequence = FCsequence(episodenbr)
    times = FCtimes()   # in msec
    
     # Getting starts times of stimulations
    for w in range(25):
        for i in range(episodenbr):
            for j in range(50):
                if sequence[i, j, 0] == float(w) and sequence[i, j, 1] == 0.:
                    #stimtimes[w][0].append(times[j]/1000 + i * 3.100)
                    stimtimes[w][0].append(times[j]/1000 + i * 2.700) # changed! August 2

        for i in range(episodenbr):
            for j in range(50):
                if sequence[i, j, 0] == float(w) and sequence[i, j, 1] == 1.:
                    #stimtimes[w][1].append(times[j]/1000 + i * 3.100)
                    stimtimes[w][1].append(times[j]/1000 + i * 2.700) # changed! August 2

    # Loop each neuron and get the spikes.
    for neuron in list(Spikes.keys()):

        codename = 'exp'+ str(exp) + '_' + str(meas) + '_c' + str(neuron)
        print(codename)
        #psth = AttrDict({'clusnum': neuron,'exp' : int(exp) , 'meas': int(meas[1]) , 'shank': int(meas[3])})
        PSTH[codename] =  AttrDict({'clusnum': neuron,'exp' : int(exp) , 'meas': int(meas[1]) , 'shank': int(meas[3])})
        #psth.update(AttrDict({'psth_counts': [] , 'psth_times': [] , 'psth_length': [t_before,t_after] }))
        PSTH[codename].update(AttrDict({'psth_counts': [] , 'psth_times': [] , 'psth_length': [t_before,t_after] }))

        #psth['psth_counts'], psth['psth_times'] = PSTH_spikes(stimtimes, Spikes[neuron].spike_times, sampling_freq, t_before, t_after, starts)
        PSTH[codename]['psth_counts'], PSTH[codename]['psth_times'] = PSTH_spikes(stimtimes, Spikes[neuron].spike_times, sampling_freq, t_before, t_after, starts, episodenbr)
        
        #PSTH[codename] = psth

    return PSTH


#The magic function:

#----------------------------------------------------------------------------------------
# PSTH SPIKES
#----------------------------------------------------------------------------------------

def PSTH_spikes(stimtimes, spikes, samp, t_before, t_after, starts, episodenbr):
    """
    stimulation   : a list of numpy arrays with a n*t stimulus inside
    stimtimes     : a list of times the stimulus occurred for each whisker
    spikes        : an array that contains the spike times (s)
    Vtag1         : synchronises stimulus with spike times
    samp          : sampling rate of the stimulation (Hz)
    t_before      : duration before the stim (positive, s)
    t_after       : duration after the stim (positive, s)
    starts        : the start of the F sweeps
    stops         : the stops of the F sweeps
    """
    
    PSTH_spike_counts = {w : {} for w in range(25)}
    
        
    # Counting spikes    
    for w in range(25):  
        spikecountup = 0
        spikecountdown = 0
        spikecountsup = 0
        spikecountsdown = 0
        
        
        for x in stimtimes[w][0]:
            spikecountup = len([ i for i in spikes if ((x - t_before/1000) < i) and ((x + t_after/1000) > i)])
            spikecountsup += spikecountup
        
        for x in stimtimes[w][1]:
            spikecountdown = len([ i for i in spikes if ((x - t_before/1000) < i) and ((x + t_after/1000) > i)])
            spikecountsdown += spikecountdown
            
        PSTH_spike_counts[w] = spikecountsup, spikecountsdown
    
    print('counted ')


    hist_inds = {} #same changes for this block, each loop will change length depending on how many stimulations fall in a sweep
         
    for w in range(25):
        #hist_inds[w] = np.zeros(PSTH_spike_counts[w][0]), np.zeros(PSTH_spike_counts[w][1])
        hist_inds[w] = [], []
        
        spikecountup = 0
        spikecountdown = 0
        spikecountsup = 0
        spikecountsdown = 0
        
        for x in stimtimes[w][0]:
            #spikecountup = len(spikes[np.multiply((x - t_before/1000) < spikes, (x + t_after/1000) > spikes)])
            spikeidxup = spikes[np.multiply((x - t_before/1000) < spikes, (x + t_after/1000) > spikes)]
            hist_inds[w][0].extend(spikeidxup-x)
            #spikecountsup += spikecountup
            
        for x in stimtimes[w][1]:
            #spikecountdown = len(spikes[np.multiply((x - t_before/1000) < spikes, (x + t_after/1000) > spikes)])
            spikeidxdown = spikes[np.multiply((x - t_before/1000) < spikes, (x + t_after/1000) > spikes)]
            hist_inds[w][1].extend(spikeidxdown-x)
            #spikecountdown += spikecountdown
    
    print('got hist data ')
    
    return PSTH_spike_counts, hist_inds

# March 25 we took out the rounding from this function, to keep the actual times with respect to stim.
# April modified a little to be more precise with absolute times.


# FUNCTIONS SURPRISE FOR single neuron
# Made for plotting in the surprise analysis

from matplotlib.pyplot import *
#----------------------------------------------------------------------------------------
# DISPLAY PSTH 
#----------------------------------------------------------------------------------------
def display_all_PSTHs_of_recording(expe, histdata, counts, pdf_files_directory, t_before, t_after, grupete, titles) :
    
    fig = plt.figure(figsize=(12,16.5))
    nrns = len(histdata.keys())
    if nrns <16: 
        layout = [5,3]
    else: layout = [nrns//3+(nrns%3!=0),3]
    outer_grid = gridspec.GridSpec(layout[0], layout[1], wspace=0.1, hspace=0.2)
    
    ii=0
    orderneurons = np.sort(list(histdata.keys()))
    for neuron in orderneurons:
        totalup = 0
        totaldown = 0
        for i in np.arange(25, dtype='int') :
            totalup+=counts[neuron][i][0]
            totaldown+=counts[neuron][i][1]
        
  
        inner_grid = gridspec.GridSpecFromSubplotSpec(5,5,subplot_spec=outer_grid[ii], wspace=0.1, hspace=0.1)
               
        numspikesP= totalup                  
        numspikesN= totaldown
        
        Sig = numpy.zeros(25, dtype=bool)
        PW = 20
        
        
        print('looping neurons: ', neuron)
        display_PSTH(expe, histdata[neuron], counts[neuron], t_before, t_after, fig, inner_grid, neuron)                               
        
        if grupete ==1:
            fig.suptitle(titles + '_multiunits',fontsize=16)
        elif grupete ==3:
            fig.suptitle(titles + '_responsiveMULTIUNITS',fontsize=16)
        else:
            fig.suptitle(titles ,fontsize=16)
        
        ii+=1
    if grupete ==1:                  
        fig.savefig(pdf_files_directory + titles + '_hist_multi.pdf', format='pdf')
    elif grupete==3:
        fig.savefig(pdf_files_directory + titles + '_hist_respMULTI.pdf', format='pdf')
    else:     
        print('printing')
        fig.savefig(pdf_files_directory + titles + '_hist.pdf', format='pdf')


# FUNCTIONS SURPRISE FOR single neuron
# Made for plotting in the surprise analysis

#----------------------------------------------------------------------------------------
# DISPLAY PSTH 
#----------------------------------------------------------------------------------------
# Plot a single neuron PSTH, 25 piezos
def display_PSTH(expe, histdata, counts, t_before, t_after, fig, inner_grid, n) :
   
    #-------------------------------------------
    # Getting data from pickles    
    #PW = sigdata.PW                 # PW for both directions
    #Sig = sigdata.Sig               # Responsive whiskers (significant)
    #SigTop = sigdata.Sig_top        # Top Significant
    #Sig_st = sigdata.Sig_strength   # Response strength
    
    #cgreen = '#ccffcc'
    #cblue=   '#ccccff'
    #cmix =   '#ffcccc' 
    #-------------------------------------------
    # To build histogram values. Here we get number of counts, and get normalization factors
    histlength = (t_before + t_after)*1000 + 1
    
    print(histlength , 'histlength')
    
    numspikesP=0
    numspikesN=0
    nup = np.zeros((25,histlength-1))
    ndown = np.zeros((25,histlength-1))
    fig2 = plt.figure()
    ax = fig2.add_subplot(1,1,1)
    
   
    for i in range(25) :
        if counts[i][0]>0:
            n1, bins, patches = ax.hist(histdata[i][0], bins = np.linspace(-t_before,t_after, histlength))
            nup[i,:] = n1
        if counts[i][1]>0 :
            n2, bins, patches = ax.hist(histdata[i][1], bins = np.linspace(-t_before,t_after, histlength))
            ndown[i,:] = n2
    numspikesP = np.sum(nup)
    numspikesN = np.sum(ndown)
    
    print(numspikesP, numspikesN)
    
    normnum = (1/np.sum(numspikesP+numspikesN))
    height = np.max(np.array([np.max(nup), np.max(ndown)]))/(1/normnum)
    plt.clf() 
    #-------------------------------------------
    # Building a plot for each whisker
    print('looping whiskers')
    for j in range(25) : #I use a dummy variable to sort whisker problems in exp23, j: indicates position, w: data
        w=j
        ax1 = Subplot(fig, inner_grid[j])  # assign plot location, then reasign whisker
        
       
        if j == 0 :       #generate the first axe to share scales
            ax1 = Subplot(fig, inner_grid[j],sharex=ax1,sharey=ax1)     
            ax1.set_xticks([])
            ax1.set_yticks([])
        elif j==20 :  # for the blank whisker we draw a thin box
            ax1 = Subplot(fig,inner_grid[j],sharex=ax1,sharey=ax1)
            ax1.spines['right'].set_linewidth(0.3)
            ax1.spines['top'].set_linewidth(0.3)
            ax1.spines['left'].set_linewidth(0.3)
            ax1.spines['bottom'].set_linewidth(0.3)
            ax1.set_xticks([])
            ax1.set_yticks([])
        else :
            ax1 = Subplot(fig,inner_grid[j],sharex=ax1,sharey=ax1)
            ax1.set_xticks([])
            ax1.set_yticks([])
        
              
        if j!=20:
            ax1.spines['right'].set_visible(False)
            ax1.spines['top'].set_visible(False)
            ax1.spines['left'].set_visible(False)
            ax1.spines['bottom'].set_visible(False)
        #-------------------------------------------------------
        # Plot the histograms
        if np.sum(ndown[w,:])>0:#histdata[w][1].size :
            ax1.hist(histdata[w][1], bins = np.linspace(-t_before, t_after, histlength), color='g', alpha=1.0, edgecolor='none', histtype='stepfilled', label='Pos', weights=np.repeat(normnum, len(histdata[w][1])))
            #ax1.hist(histdata[w][1], bins = np.linspace(-t_before, t_after, histlength), color='g', alpha=1.0, edgecolor='none', histtype='stepfilled', label='Pos')
        if np.sum(nup[w,:])>0:#histdata[w][0].size :
            ax1.hist(histdata[w][0], bins = np.linspace(-t_before, t_after, histlength), color='b', alpha=0.7, edgecolor='none', histtype='stepfilled', label='Neg', weights=np.repeat(normnum, len(histdata[w][0]))) 
            #ax1.hist(histdata[w][0], bins = np.linspace(-t_before, t_after, histlength), color='b', alpha=0.7, edgecolor='none', histtype='stepfilled', label='Neg') 
        #-------------------------------------------------------
        # Set limits and plot 0 line
        ax1.set_xlim(-t_before, t_after)
        ax1.axvline(0, color = 'r', linewidth=1)
        ax1.axhline(0, color = 'r', linewidth=2)
        ymax = 1.02 * height
        ax1.set_ylim(0, ymax)
        #-------------------------------------------------------
        # Plot stimulus
        xvals = np.array([0,0.010,0.020,0.030])
        yvals = np.array([0,ymax*0.9,ymax*0.9,0])
        ax1.plot(xvals, yvals, linewidth=0.2,color = (0.75,0.75,0.75))
        #-------------------------------------------------------
        # Annotating the plot

        if w==4: ax1.set_title('ymax =' + str( np.around(height,decimals = 3) ),fontsize=8)
        if w ==1: ax1.set_title('Nrn' + n + '_Pos' + str(int(numspikesP))+ '_Neg' + str(int(numspikesN)),fontsize=12)
        fig.add_subplot(ax1)


