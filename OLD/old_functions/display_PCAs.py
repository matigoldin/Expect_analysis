# FUNCTIONS SURPRISE FOR single neuron

from matplotlib.pyplot import*

#----------------------------------------------------------------------------------------
# DISPLAY PCA
#----------------------------------------------------------------------------------------
def display_PCA(PCA,cl,PCAn, fig, inner_grid): 
    
    ax= Subplot(fig, inner_grid[0])
    #------------------------------------
    #plot clusters
    ax.scatter(-PCA[0][cl[0]],PCA[1][cl[0]],color ='g', label = 'Fast Spiker', s = 1)
    ax.scatter(-PCA[0][cl[1]],PCA[1][cl[1]],color='b', label = 'Regular Spiker',s = 1)

    ax.set_xlabel('-PCA1',size=8)
    ax.set_ylabel('PCA2',size=8)

    
    ax.plot(-PCAn[6],PCAn[5],'ro',  markeredgecolor = 'k', markersize = 4)

    
    #ax.set_xlim([0,35])
    ax.set_ylim([0,30])
    ax.set_xlim([10,65])
    
    ax.legend(loc='upper left', numpoints=1, ncol=1,fontsize=4, bbox_to_anchor=(0, 1.))

    ax.tick_params( labelsize=8)

    ax.set_title('Waveform Clusters', size = 12, fontweight='bold')

    
    fig.add_subplot(ax)
