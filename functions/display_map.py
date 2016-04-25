# Functions in this file are:
#			- display_maps(Surprise, Latencies,  fig, inner_grid,expe):

from matplotlib.pyplot import*
from numpy import*
#import numpy as np
import pylab as pylab
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colors as colors


#----------------------------------------------------------------------------------------
# DISPLAY MAP
#----------------------------------------------------------------------------------------
def display_maps(Detect, Latencies,  fig, inner_grid,expe):

    ax= Subplot(fig, inner_grid[0])

    St = Detect.Sig_strength
    #----------------------------------------    
    # NEED TO REMAP FOR EXPS 20 22 and 23, and 27!!
    if expe<=22:
        aux = copy(St[24])
        for w in [24,23,22,21]:
            St[w] = copy(St[w-1])
        St[20] = copy(St[11])
        St[11] = aux
    if expe == 23:
        for w in [0,1,2,3]:
            St[w] = copy(St[w+1])
        St[4] = [0,0]
    #if exp == 27:
    #    St[16]== [0,0]
    #---------------------------------------------                        
    
    Stup = np.reshape(St[:,0],(5,5)) / St.max()
    Stdn = np.reshape(St[:,1],(5,5))/ St.max()        
    
    # only do if they exist
    if St.max()>0:
        
        im = ax.imshow(Stup,interpolation='none',cmap=pylab.gray())

        # create an axes on the right side of ax. The width of cax will be 5%
        # of ax and the padding between cax and ax will be fixed at 0.05 inch.
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="10%", pad=0.15)
        colorbar(im, cax=cax)

        ax.set_xticks([0,1,2,3,4]) # range of values in edges
        ax.set_yticks([0,1,2,3,4]) # range of values in edges
        ax.set_xticklabels(['St','1','2','3','4']) # range of values in edges
        ax.set_yticklabels(['A','B ','C ','D','E ']) # range of values in edges
        ax.tick_params('both', length=0, width=0)        

        ax.set_title('Caudal Strength')    
        fig.add_subplot(ax)
        #---------------------------------------------------------------------------------------------
        ax= Subplot(fig, inner_grid[1])
        
        im =ax.imshow(Stdn,interpolation='none',cmap=pylab.gray())

        ax.set_xticks([0,1,2,3,4]) # range of values in edges
        ax.set_yticks([0,1,2,3,4]) # range of values in edges
        ax.set_xticklabels(['St','1','2','3','4']) # range of values in edges
        ax.set_yticklabels(['A','B ','C ','D','E ']) # range of values in edges
        ax.tick_params('both', length=0, width=0)        

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="10%", pad=0.15)
        colorbar(im, cax=cax)

        ax.set_title('Rostral Strength')    
        fig.add_subplot(ax)
        #---------------------------------------------------------------------------------------------
        ax= Subplot(fig, inner_grid[2])
        
        Stboth = np.nan_to_num((Stup-Stdn)/(Stup+Stdn))
        # make a color map of fixed colors
        cmap = colors.ListedColormap(['#00cc00','#00aa00','#006600','#003300', 'black','#000066','#000099','#0000cc' ,'blue'])
        bounds=[-1,-0.75,-0.5,-0.25,-0.01,0.01,0.25,0.5,0.75,1]
        norm = colors.BoundaryNorm(bounds, cmap.N)    

        im = ax.imshow(Stboth,interpolation='none',cmap=cmap,norm=norm)

        ax.set_xticks([0,1,2,3,4]) # range of values in edges
        ax.set_yticks([0,1,2,3,4]) # range of values in edges
        ax.set_xticklabels(['St','1','2','3','4']) # range of values in edges
        ax.set_yticklabels(['A','B ','C ','D','E ']) # range of values in edges
        ax.tick_params('both', length=0, width=0)        

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="10%", pad=0.15)
        colorbar(im, cax=cax)

        ax.set_title('Directionality')    
        fig.add_subplot(ax)
        #---------------------------------------------------------------------------------------------
        ax= Subplot(fig, inner_grid[3])

        Lat = zeros(25)
        for i in arange(25):
            if Latencies[i,0]>5 and Latencies[i,1]>5:
                Lat[i] = min(Latencies[i,0],Latencies[i,1])
            elif Latencies[i,0]>5:
                Lat[i]= Latencies[i,0]
            elif Latencies[i,1]>5:
                Lat[i]= Latencies[i,1]
        #----------------------------------------    
        # NEED TO REMAP FOR EXPS 20 22 and 23, and 27!!
        if expe<=22:
            aux = copy(Lat[24])
            for w in [24,23,22,21]:
                Lat[w] = copy(Lat[w-1])
            Lat[20] = copy(Lat[11])
            Lat[11] = aux
        if expe == 23:
            for w in [0,1,2,3]:
                Lat[w] = copy(Lat[w+1])
            Lat[4] = 0
        #---------------------------------------------          
                
        Lat = np.reshape(Lat,(5,5))
        im = ax.imshow(Lat,interpolation='none',cmap=pylab.hot())

        ax.set_xticks([0,1,2,3,4]) # range of values in edges
        ax.set_yticks([0,1,2,3,4]) # range of values in edges
        ax.set_xticklabels(['St','1','2','3','4']) # range of values in edges
        ax.set_yticklabels(['A','B ','C ','D','E ']) # range of values in edges
        ax.tick_params('both', length=0, width=0)        

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="10%", pad=0.15)
        colorbar(im, cax=cax)

        ax.set_title('Latency')    
        fig.add_subplot(ax)
