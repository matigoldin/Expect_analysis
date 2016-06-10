def eff():

      import numpy as np
      
      # In this cell you put all the information to make the code portable from computer to computer
      # You have to place all the file names and experiments, then you loop whichever you want to analyse
      #--------------------------------------------------------------------------------
      #Experiment numbers
      ExpeNum = [1,2]
      #--------------------------------------------------------------------------------
      #Folders for measurements and experiments (this is how we separate shanks in folders for individual analyses)
      m164 = ['m1s'+str(s) for s in np.arange(8)+1]
      m264 = ['m2s'+str(s) for s in np.arange(8)+1]
      m364 = ['m3s'+str(s) for s in np.arange(8)+1]
      m464 = ['m4s'+str(s) for s in np.arange(8)+1]
      m564 = ['m5s'+str(s) for s in np.arange(8)+1]
      m664 = ['m6s'+str(s) for s in np.arange(8)+1]
      m764 = ['m7s'+str(s) for s in np.arange(8)+1]
      m864 = ['m8s'+str(s) for s in np.arange(8)+1]
      m964 = ['m9s'+str(s) for s in np.arange(8)+1]
      m1064 = ['m10s'+str(s) for s in np.arange(8)+1]

      M = [m164,m264,m364,m464,m564,m664,m764,m864,m964,m1064]

      shanks = ['_ele01_ele08.kwik',
                '_ele09_ele16.kwik',
                '_ele17_ele24.kwik',
                '_ele25_ele32.kwik',
                '_ele33_ele40.kwik',
                '_ele41_ele48.kwik',
                '_ele49_ele56.kwik',
                '_ele57_ele64.kwik']
      #--------------------------------------------------------------------------------
      #--------------------------------------------------------------------------------
      #Kwik files    
      base = {}
      files = {}
      #--------------------------------------------------------------------------------
      exp = 1
      base[exp] = ['EXPECT-151029-'+str(i) for i in np.arange(10)+1]
      files[exp] ={}
      for reps in np.arange(10):
          files[exp][reps+1] = [ base[exp][reps]+shanks[i] for i in np.arange(8)]
      #--------------------------------------------------------------------------------
      exp = 2
      base[exp] = ['EXPECT-151217-'+str(i) for i in np.arange(10)+1]
      files[exp] ={}
      for reps in np.arange(7):
          files[exp][reps+1] = [ base[exp][reps]+shanks[i] for i in np.arange(8)]

      #--------------------------------------------------------------------------------
      # Here I create my dictionary of experiments
      Expe={}
      for num in ExpeNum: 
          Expe[num] = dict()
      #---------------------------------------
      stimfiles = {}
      timefiles = {}
      eptimefiles = {}

      exp =1
      m=0
      for Meas in M[0:10]:
          i=0
          for meas in Meas:
              Expe[exp][meas] = files[exp][m+1][i]
              i+=1
          m+=1
      exp=2
      m=0
      for Meas in M[0:7]:
          i=0
          for meas in Meas:
              Expe[exp][meas] = files[exp][m+1][i]
              i+=1
          m+=1

      #--------------------------------------------------------------------------------
      #Stim files
      for exp in ExpeNum:
          stimfiles[exp] = [base[exp][rep-1][:-1] + 'stims-' + str(rep) + '.txt' for rep in files[1]]
          timefiles[exp] = [base[exp][rep-1][:-1] + 'times-' + str(rep) + '.txt' for rep in files[1]]
          eptimefiles[exp] = [base[exp][rep-1][:-1] + 'ep_times-' + str(rep) + '.txt' for rep in files[1]] 

      return Expe, stimfiles, timefiles, eptimefiles
