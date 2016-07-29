# FUNCTIONS SURPRISE FOR single neuron

import numpy as np
from numpy import*
from matplotlib.pyplot import*
from scipy import *

#----------------------------------------------------------------------------------------
# DISPLAY LATENCIES
#----------------------------------------------------------------------------------------
def display_latencies(Detect, Latencies,  fig, inner_grid):
    marks=18

    PW = Detect.PW
    St = Detect.Sig_strength    
    # getting latencies 
    Lat0 = Latencies[:,0]
    Lat1 = Latencies[:,1]
    LatPW0 = Latencies[PW[0],0]
    LatPW1 = Latencies[PW[1],1]
    #for scatter separated
    Lat00 = np.append(Lat0[0:PW[0]],Lat0[PW[0]+1:])
    Lat11 = np.append(Lat1[0:PW[1]],Lat1[PW[1]+1:])
    
    Lat00 = Lat00[np.where(Lat00>5)]
    Lat11 = Lat11[np.where(Lat11>5)]
       
    Lat = np.append(Lat00,Lat11)
    #for boxplot all
    Lat0 = Lat0[np.where(Lat0>5)] 
    Lat1 = Lat1[np.where(Lat1>5)] 
    LatPW = np.append(Lat0,Lat1)
    # only do if they exist
    if len(LatPW)>0:   
        ax= Subplot(fig, inner_grid[0])
        ax.set_title('Latencies', fontweight='bold')
        #---------------------------------------------------------------------------------------------
        # Hide the right and top spines
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Only show ticks on the left and bottom spines
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        #---------------------------------------------------------------------------------------------
        # plot Caudal
        if len(Lat0)>0:
            ax.boxplot(Lat0,positions=[0.8])
            x = (rand(len(Lat00))-0.5)/5+0.55
            ax.scatter(x,Lat00,s=marks,facecolor='none', edgecolors='k')
        ax.scatter(0.55,LatPW0, s=marks,c='b', edgecolors='b',alpha=0.5)
        #---------------------------------------------------------------------------------------------
        # plot Rostral
        if len(Lat1)>0:
            ax.boxplot(Lat1,positions=[1.8])
            x = (rand(len(Lat11))-0.5)/5+1.55
            ax.scatter(x,Lat11,s=marks,facecolor='none', edgecolors='k')
        ax.scatter(1.55,LatPW1, s=marks,c='g', edgecolors='g',alpha=0.5)
        #---------------------------------------------------------------------------------------------
        # Plot Both
        if len(Lat)>0:
            ax.boxplot(LatPW,positions=[-.1])
            x = (rand(len(Lat))-0.5)/5-0.45
            ax.scatter(x,Lat,s=marks,facecolor='none', edgecolors='k')
        ax.scatter(-0.45,LatPW1, s=marks,c='g', edgecolors='g', alpha=0.5)
        ax.scatter(-0.45,LatPW0, s=marks,c='b', edgecolors='b',alpha=0.5)
        #---------------------------------------------------------------------------------------------
        # Plot strong-weak latencies
        i=0
        for l in Latencies:
            if l[0]>5 and l[1]>5:
                if PW[0]==PW[1] and PW[0]==i: col = 'ro-'
                elif PW[1]==i: col = 'go-' 
                elif PW[0]==i: col = 'bo-' 
                else: col ='ko-'
                ax.plot([2.7,3.3],l,col, markersize=4, markeredgecolor =col[0])
            i+=1
        #---------------------------------------------------------------------------------------------
        # plot parameters
       
        ax.set_ylabel('Latency (ms)')
        maxlat = max(np.append(np.append(Lat0,Lat1),np.append(LatPW0,LatPW1)))+2
        ax.set_ylim([5,55])
        ax.set_xlim([-1,4])

        ax.set_xticks([-0.2,0.7,1.7,3])   
        ax.set_xticklabels( ['All','Caudal', 'Rostral','Caudal-Rostral'], size = 14 )
        ax.tick_params( labelsize=12)

        fig.add_subplot(ax)
