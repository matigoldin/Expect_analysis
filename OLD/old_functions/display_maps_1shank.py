# DISPLAY MAPS AND LATENCIES FOR 1 SHANK
# Functions in this file are:
#			- display_mapsShank(Surprise, LatenciesAll,  fig, inner_grid,expe,meas):
#			- display_latenciesShank(Surprise, Lat,latlabel,  fig, inner_grid,meas):
#			- display_mapsDirection(Surprise, LatenciesAll,  fig, inner_grid,expe,meas):

from matplotlib.pyplot import*
from numpy import*
#import numpy as np
import pylab as pylab
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colors as colors

#----------------------------------------------------------------------------------------
# DISPLAY MAP
#----------------------------------------------------------------------------------------
def display_mapsShank(Surprise, LatenciesAll, DET,  fig, inner_grid,expe,meas):

    ax= Subplot(fig, inner_grid[0])
    idx = sorted(list(Surprise.keys()))
    St = zeros([25,2])
    Sig = zeros([25,2])
    Latencies = zeros([25,2])
    for n in idx:
        St += DET[n].detection_data.Sig_strength
        Latencies+=LatenciesAll[n]
        Sig += DET[n].detection_data.Sig
    #----------------------------------------    
    # NEED TO REMAP FOR EXPS 20 22 and 23, and 27!!
    if expe<=22:
        aux = copy(St[24])
        aux2 = copy(Sig[24])
        for w in [24,23,22,21]:
            St[w] = copy(St[w-1])
            Sig[w] = copy(Sig[w-1])
        St[20] = copy(St[11])
        St[11] = aux
        Sig[20] = copy(Sig[11])
        Sig[11] = aux2
    if expe == 23:
        for w in [0,1,2,3]:
            St[w] = copy(St[w+1])
            Sig[w] = copy(Sig[w+1])
        St[4] = [0,0]
        Sig[4] = [0,0]
    #if exp == 27:
    #    St[16]== [0,0]
    #---------------------------------------------                        

    Stup = np.reshape(St[:,0],(5,5)) / St.max()
    Stdn = np.reshape(St[:,1],(5,5))/ St.max()        
    Sttot = np.reshape(St[:,0]+St[:,1],(5,5))/ St.max()
    Sigtot = np.reshape(Sig[:,0]+Sig[:,1],(5,5))/ St.max()

    # only do if they exist
    if St.max()>0:

        #im = ax.imshow(Stup,interpolation='none',cmap=pylab.gray())
        #im = ax.imshow(Sttot,interpolation='none',cmap=pylab.gray())

        im = ax.imshow(Sttot,interpolation='bessel',cmap=pylab.gray())

        #im = ax.imshow(Sigtot,interpolation='bessel',cmap=pylab.gray())

        # create an axes on the right side of ax. The width of cax will be 5%
        # of ax and the padding between cax and ax will be fixed at 0.05 inch.
        #divider = make_axes_locatable(ax)
        #cax = divider.append_axes("right", size="10%", pad=0.05)
        #plt.colorbar(im, cax=cax)

        ax.set_xticks([0,1,2,3,4]) # range of values in edges
        ax.set_yticks([0,1,2,3,4]) # range of values in edges
        ax.set_xticklabels(['St','1','2','3','4']) # range of values in edges
        ax.set_yticklabels([' A','B ','C ','D','E ']) # range of values in edges
        ax.tick_params('both', length=0, width=0)        

        ax.set_title(meas)    
        #ax.set_title('Caudal Strength')  
        

        fig.add_subplot(ax)
#         #---------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
# DISPLAY LATENCIES
#----------------------------------------------------------------------------------------
def display_latenciesShank(Surprise, Lat,latlabel,  fig, inner_grid,meas):
    marks=18
    idx = sorted(list(Lat.keys()))
    #ax= Subplot(fig, inner_grid[0],projection='3d')
    ax= fig.gca(projection='3d')
    
    Latencies = Lat
    
    Lat0 = []
    Lat1 = []
    Lat00 = []
    Lat11 = []
    LatPW0 = []
    LatPW1 = []
    LatPW = []
    
    latPW=dict()
    lat = dict()
    latmedian =dict()
    
    for m in arange(4)+1:
        for s in arange(8)+1:
            id = 'm'+str(m)+'s'+str(s)
            lat[id]=[] 
            latPW[id]=[]
            latmedian[id] = []
            
    for n in idx:
        m = latlabel[n][0]
        s = latlabel[n][1]
        id = 'm'+str(m)+'s'+str(s)
        lat5 = Lat[n][where(Lat[n]>5)]
        if len(lat5)>0:
            lat[id].append(min(lat5))
            latmedian[id].append(mean(lat5))
        PW = Surprise[n].PW
        
        
        if PW[0]!=20 or PW[1]!=20:
            if PW[0]==20 and Lat[n][PW[1]][1]>6:
                latPW[id].append( Lat[n][PW[1]][1]  )
                #print(Lat[n][PW[1]][1])
            elif PW[1]==20 and Lat[n][PW[0]][0]:
                latPW[id].append( Lat[n][PW[0]][0])
                #print(Lat[n][PW[0]][0])
            elif Lat[n][PW[0]][0]>6 and Lat[n][PW[1]][1]>6:
                latPW[id].append( min(Lat[n][PW[0]][0],Lat[n][PW[1]][1]))
            elif Lat[n][PW[1]][1]>6:
                latPW[id].append( (Lat[n][PW[1]][1]))
            elif Lat[n][PW[0]][0]>6:
                latPW[id].append( (Lat[n][PW[0]][0]) )
                #print(Lat[n][PW[0]][0])
                #print(Lat[n][PW[1]][1])
    
    latmap = zeros([4,8])
    latmapmedian = zeros([4,8])
    latmapPW = zeros([4,8])
    for pos in lat:
        if pos:
            m=int(pos[1])
            s=int(pos[3])
            latmap[m-1][s-1] = min(lat[pos])
            latmapmedian[m-1] = min(latmedian[pos])
            latmapPW[m-1][s-1] = min(latPW[pos])
    
    print(latmap)
    
    print(latmapPW)
    
    #im = ax.imshow(latmapPW,interpolation='none',cmap=pylab.gray())
    
    #print(latmedian.shape, arange(4).shape,arange(8).shape)
    
    X= arange(8)+1
    Y= arange(4)+1
    X, Y = np.meshgrid(X, Y)
    
    print(X.shape,latmapmedian.shape)
    
    ax.surf = ax.plot_surface(X,Y,latmapPW, rstride=1, cstride=1, cmap=cm.coolwarm,linewidth=0, antialiased=False)
    #ax.surf = ax.plot_surface([0,1],[0,1] , [[1,2],[3,4]], rstride=1, cstride=1, cmap=cm.coolwarm,linewidth=0, antialiased=False)
    
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="10%", pad=0.15)
    #plt.colorbar(im, cax=cax)
    
    #fig.add_subplot(ax)

#----------------------------------------------------------------------------------------
# DISPLAY MAP Direction
#----------------------------------------------------------------------------------------
def display_mapsDirection(Surprise, LatenciesAll,DET,  fig, inner_grid,expe,meas):

    ax= Subplot(fig, inner_grid[0])
    idx = sorted(list(Surprise.keys()))
    St = zeros([25,2])
    ST = zeros([25,2])
    Sig = zeros([25,2])
    Latencies = zeros([25,2])
    Stdir = zeros([25,2])
    Stdirnorm = zeros([25,2])
    for n in idx:
        St += DET[n].detection_data.Sig_strength
        Latencies+=LatenciesAll[n]
        Sig += DET[n].detection_data.Sig
        st = DET[n].detection_data.Sig_strength
        if max()
        Stdirnorm += (st[:,0]-st[:,0])/(st[:,0]+st[:,0])*np.max(st,axis=0)
        
    #----------------------------------------    
    # NEED TO REMAP FOR EXPS 20 22 and 23, and 27!!
    if expe<=22:
        aux = copy(St[24])
        aux2 = copy(Sig[24])
        for w in [24,23,22,21]:
            St[w] = copy(St[w-1])
            Sig[w] = copy(Sig[w-1])
        St[20] = copy(St[11])
        St[11] = aux
        Sig[20] = copy(Sig[11])
        Sig[11] = aux2
    if expe == 23:
        for w in [0,1,2,3]:
            St[w] = copy(St[w+1])
            Sig[w] = copy(Sig[w+1])
        St[4] = [0,0]
        Sig[4] = [0,0]
    #if exp == 27:
    #    St[16]== [0,0]
    #---------------------------------------------                        

    Stup = np.reshape(St[:,0],(5,5)) / St.max()
    Stdn = np.reshape(St[:,1],(5,5))/ St.max()        
    Sttot = np.reshape(St[:,0]+St[:,1],(5,5))/ St.max()
    Sigtot = np.reshape(Sig[:,0]+Sig[:,1],(5,5))/ St.max()

    Stdir = (Stup-Stdn)/(Stup+Stdn)

    cmap = colors.ListedColormap(['#00cc00','#00aa00','#006600','#003300', 'black','#000066','#000099','#0000cc' ,'blue'])
    bounds=[-1,-0.75,-0.5,-0.25,-0.01,0.01,0.25,0.5,0.75,1]
    norm = colors.BoundaryNorm(bounds, cmap.N)    
    
    # only do if they exist
    if St.max()>0:

        #im = ax.imshow(Stup,interpolation='none',cmap=pylab.gray())
        #im = ax.imshow(Sttot,interpolation='none',cmap=pylab.gray())

        #im = ax.imshow(Stdir,interpolation='bessel',cmap=cmap,norm=norm)
        im = ax.imshow(Stdirnorm,interpolation='bessel',cmap=cmap,norm=norm)

        #im = ax.imshow(Sigtot,interpolation='bessel',cmap=pylab.gray())
        # create an axes on the right side of ax. The width of cax will be 5%
        # of ax and the padding between cax and ax will be fixed at 0.05 inch.
        #divider = make_axes_locatable(ax)
        #cax = divider.append_axes("right", size="10%", pad=0.05)
        #plt.colorbar(im, cax=cax)

        ax.set_xticks([0,1,2,3,4]) # range of values in edges
        ax.set_yticks([0,1,2,3,4]) # range of values in edges
        ax.set_xticklabels(['St','1','2','3','4']) # range of values in edges
        ax.set_yticklabels([' A','B ','C ','D','E ']) # range of values in edges
        ax.tick_params('both', length=0, width=0)        

        ax.set_title(meas)    
        #ax.set_title('Caudal Strength')  
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="10%", pad=0.15)
      
        colorbar(im, cax=cax)


                
        
        fig.add_subplot(ax)
