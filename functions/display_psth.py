# FUNCTIONS SURPRISE FOR single neuron
# Made for plotting in the surprise analysis

import numpy as np
from matplotlib.pyplot import*

#----------------------------------------------------------------------------------------
# DISPLAY PSTH 
#----------------------------------------------------------------------------------------
# Plot a single neuron PSTH, 25 piezos
def display_PSTH(expe, histdata, sigdata,t0, t_before, t_after, fig,inner_grid, n) :
   
    #-------------------------------------------
    # Getting data from pickles    
    PW = sigdata.PW                 # PW for both directions
    Sig = sigdata.Sig               # Responsive whiskers (significant)
    SigTop = sigdata.Sig_top        # Top Significant
    Sig_st = sigdata.Sig_strength   # Response strength
    
    cgreen = '#ccffcc'
    cblue=   '#ccccff'
    cmix =   '#ffcccc' 
    #-------------------------------------------
    # To build histogram values. Here we get number of counts, and get normalization factors
    histlength = t_before + t_after + 1
    numspikesP=0
    numspikesN=0
    nup = np.zeros((25,histlength-1))
    ndown = np.zeros((25,histlength-1))
    fig2 = figure()
    ax = fig2.add_subplot(1,1,1)
    
    for i in range(25) :
        if histdata[i][0].size :
            n1, bins, patches = ax.hist(histdata[i][0]*1000, bins = np.linspace(-t_before,t_after, histlength))
            nup[i,:] = n1
        if histdata[i][1].size :
            n2, bins, patches = ax.hist(histdata[i][1]*1000, bins = np.linspace(-t_before,t_after, histlength))
            ndown[i,:] = n2
    numspikesP = np.sum(nup)
    numspikesN = np.sum(ndown)
    normnum = (1/np.sum(numspikesP+numspikesN))
    height = np.max(np.array([np.max(nup), np.max(ndown)]))/(1/normnum)
    clf() 
    #-------------------------------------------
    # Building a plot for each whisker
    for j in range(25) : #I use a dummy variable to sort whisker problems in exp23, j: indicates position, w: data
        w=j
        ax1 = Subplot(fig, inner_grid[j])  # assign plot location, then reasign whisker
        #-------------------------------------------------------
        #for whisker problems
        #-------------------------------------------------------
        #Only for EXP 23: I shift first row to the left and leave A4 empty
        if expe == 23:
            if j<4: w=j+1
            elif j==4: continue
            elif j>4:w=j
        #-------------------------------------------------------
        #Only for EXP 27: D1 whisker missing
        if expe == 27:     
            if j==16: continue
        #-------------------------------------------------------
        #Only for EXP 22 or less: odd ELPHY piezo assignement
        if expe <= 22:     
            if j==11: w=24
            if j==20: w=11    
            if j>20: w=j-1
                                    
        #-------------------------------------------------------
        # ending whisker problems
        #-------------------------------------------------------        
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
        #-------------------------------------------------------        
        # Drawing thick box around PW whiskers, and painting according to strength                                
        if Sig[w][0] == 1 or Sig[w][1] == 1:
            if Sig[w][0]+Sig[w][1]==2:
                col = cmix
            elif Sig[w][0]==1:
                col = cblue
            else:
                col = cgreen
            ax1.set_axis_bgcolor(col)
              
        if j!=20 and w!=PW[0] and w!= PW[1]:
            ax1.spines['right'].set_visible(False)
            ax1.spines['top'].set_visible(False)
            ax1.spines['left'].set_visible(False)
            ax1.spines['bottom'].set_visible(False)
        #-------------------------------------------------------
        # Plot the histograms
        if np.sum(ndown[w,:])>0:#histdata[w][1].size :
            ax1.hist(histdata[w][1]*1000, bins = np.linspace(-t_before, t_after, histlength), color='g', alpha=1.0, edgecolor='none', histtype='stepfilled', label='Pos', weights=np.repeat(normnum, len(histdata[w][1])))
        if np.sum(nup[w,:])>0:#histdata[w][0].size :
            ax1.hist(histdata[w][0]*1000, bins = np.linspace(-t_before, t_after, histlength), color='b', alpha=0.7, edgecolor='none', histtype='stepfilled', label='Neg', weights=np.repeat(normnum, len(histdata[w][0]))) 
        #-------------------------------------------------------
        # Set limits and plot 0 line
        ax1.set_xlim(-t_before, t_after)
        ax1.axvline(0, color = 'r', linewidth=1)
        ax1.axhline(0, color = 'r', linewidth=2)
        ymax = 1.02 * height
        ax1.set_ylim(0, ymax)
        #-------------------------------------------------------
        # Plot stimulus
        xvals = np.array([0,10,20,30])
        yvals = np.array([0,ymax*0.9,ymax*0.9,0])
        ax1.plot(xvals, yvals, linewidth=0.2,color = (0.75,0.75,0.75))
        #-------------------------------------------------------
        # Annotating the plot

        if w==4: ax1.set_title('ymax =' + str( np.around(height,decimals = 3) ),fontsize=8)
        if w ==1: ax1.set_title('Nrn' + n[12:] + '_Pos' + str(int(numspikesP))+ '_Neg' + str(int(numspikesN)),fontsize=12)
        fig.add_subplot(ax1)
