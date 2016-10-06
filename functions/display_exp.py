import numpy as np
from matplotlib.pyplot import *


#--------------------------------------------------
# BUILD STIM
#--------------------------------------------------
def build_stim(rep, isi,ylim):
    
    onestim =  np.append(np.arange(10),np.ones(51)*10, axis=0)
    onestim = np.append(onestim,np.arange(9,-1,-1),axis=0)*ylim/10
    ttot = rep*500
    stim = np.zeros(ttot)
    phase = isi*4
    
    shift=0
    
    if isi ==2:
        shift = 72
    elif isi==20:
        shift=0
    
    for p in 500*np.arange(rep-1)+phase+shift:
        stim[p:p+71] = onestim
    
    return stim
#--------------------------------------------------


from matplotlib import gridspec
matplotlib.rcParams.update({'font.size': 12})


#--------------------------------------------------
# PLOTTER
#--------------------------------------------------
def plotter(ps,pad,last,exp,n,types_list,binsize):

    # here I put the data fro the specific time interval I want to plot
    data1=[]


    # this is to plot the stimulus times in the background with different colors
    rainbow = ['blue', 'green', 'yellow', 'orange', 'white']
    rainbow2 = ['blue', 'green', 'yellow', 'orange', 'red']

    idx = sorted(list(ps.keys()))

    #print('Neurons: ',idx)
    
    fig = figure(figsize=(20,8))

    # ISI conunter
    i=0
    for isi in [2,20]:
        i+=1

        # REP counter
        r=0
        for rep in [10]:#[2,5,10]:
            r+=1

            
            rangoticks =np.arange(0, rep*500+1, 500)

            # this shift works with different ISI to plot the start of PW stim at the same place in plot
            shift = [72,0,0]        #this is set for isi = 2 and isi = 20 ms
            

            #---------------------------------------------
            # this tells me how many repetitions to plot 0: all, 2: last two, 1: last
            if last==0:
                ratios = [40,1,1]
                xmin=0
                bins = np.arange(0,500*rep+1,10)+xmin-shift[i-1]
                
            elif last==2:
                ratios = [40,1,1]
                xmin = (rep-last)*500
                bins = np.arange(0,1000+1,4)+xmin-shift[i-1]
            elif last==1: 
                ratios = [20,1,1]
                xmin = (rep-last)*500
                bins= np.arange(0,500+1,binsize)+xmin-shift[i-1]
            #---------------------------------------------
            # put subplot in place
            gs = gridspec.GridSpec(3,3, width_ratios=ratios, hspace = 0.7) 
            ax = subplot(gs[r+(i-1)*3-1])            

            #---------------------------------------------
            # here I plot the stimulus
            for repe in np.arange(rep-1):
                for k in range(5):
                    alpha=0.15
                    linew=1
                    ax.axvspan( (repe)*500 + isi*k + shift[i-1],shift[i-1]+ (repe)*500  + 8*isi+ 70 -isi*k, alpha=alpha, facecolor=rainbow2[k])

            for k in range(5):
                alpha=0.15
                linew=1
                if k==4: 
                    alpha =1
                    linew = 0
                ax.axvspan( (rep-1)*500 + isi*k + shift[i-1],shift[i-1]+ (rep-1)*500  + 8*isi+ 70 -isi*k, alpha=alpha, linewidth =linew, facecolor=rainbow[k])

            faces = ['blue','green']   
            alphas = [0.8,0.5]
            f = 0
            ymax=0
            for types in types_list:
                face = faces[f]
                alpha = alphas[f]

                data1 = []
                data = []
                data1 = np.array(ps[n][types]['hold'][pad][rep][isi])
                data = data1[np.where(data1>xmin-shift[i-1])]+ shift[i-1]
                
                f+=1

                data1 = []
                data = []
                for n in idx:
                    data2 = (np.array(ps[n][types]['hold'][pad][rep][isi])+ shift[i-1])
                    data = data2[np.where(data2>xmin)]
                    data1.extend(data)
                data=data1
                #~ 
                #~ #print(len(data1))
                #~ #print(data1)
                
                               
                if len(data)>1:
                    n1 = ax.hist(data, bins=bins, facecolor =face, alpha = alpha , linewidth =0)
                    ylim = max(n1[0])
                    if ymax<ylim: ymax = ylim
            
                    ylim=ymax
            
            ax.set_title('ISI ' + str(isi) +' - REP ' + str(rep) + '    -Normal=blue Ctrl=green-')
            fig.suptitle('Type: '+ pad + '             Cluster: ' + n , fontsize = 16,y =1.0)
            #fig.suptitle('Type: '+ pad + '             All GOOD' , fontsize = 16,y =1.0)
            
            #ax.set_xlim(xmin+50,xmin +130)# rep*500)
            ax.set_xlim(xmin,rep*500)
            if last==1: 
                ax.set_xlim(xmin,xmin+250)
                rangoticks =np.arange(xmin, xmin+250, 10)
                ax.set_xticklabels('')
                ax.xaxis.set_ticks(rangoticks)
                ax.xaxis.set_tick_params(width=5)
            

            ax.set_ylim(0, ylim*1.1)
            
            stim = build_stim(rep,isi,ylim)
            plot(stim)
    
    Folderpdf = '/media/matias/DATA/WORKSPACE2/OUTPUT/EXP_14/'
    titles =  n + '_'+str(pad) + '_span' + str(last)
    #titles =  '_'+str(pad) + '_span' + str(last)
    print(titles)
    fig.savefig(Folderpdf + titles +  '_hist_.pdf', format='pdf')
    #fig.savefig(Folderpdf + titles +'_All_good_hist_.pdf', format='pdf')



