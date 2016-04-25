def eff():

      import numpy as np
      
      # In this cell you put all the information to make the code portable from computer to computer
      # You have to place all the file names and experiments, then you loop whichever you want to analyse
      #--------------------------------------------------------------------------------
      #Experiment numbers
      ExpeNum = [20,22,23,24,25,26,27,28,29,30,31,32]

      #--------------------------------------------------------------------------------
      #Folders for measurements and experiments (this is how we separate shanks in folders for individual analyses)
      m164 = ['m1s1','m1s2','m1s3','m1s4','m1s5','m1s6','m1s7','m1s8']
      m264 = ['m2s1','m2s2','m2s3','m2s4','m2s5','m2s6','m2s7','m2s8']
      m364 = ['m3s1','m3s2','m3s3','m3s4','m3s5','m3s6','m3s7','m3s8']
      m464 = ['m4s1','m4s2','m4s3','m4s4','m4s5','m4s6','m4s7','m4s8']

      #--------------------------------------------------------------------------------
      #Kwik files    

      files20 = [ 'MEAS-150707-1_ele01_ele08.kwik',
                  'MEAS-150707-1_ele09_ele16.kwik',
                  'MEAS-150707-1_ele17_ele24.kwik',
                  'MEAS-150707-1_ele25_ele32.kwik',
                  'MEAS-150707-23_ele01_ele08.kwik',
                  'MEAS-150707-23_ele16_ele09.kwik']#,
                  #'MEAS-150707-23_ele17_ele24.kwik',  not in S2
                  #'MEAS-150707-23_ele25_ele32.kwik',] not in S2

      files22 = [ 'MEAS-150716-12_ele01_ele08.kwik',
                  'MEAS-150716-12_ele09_ele16.kwik',
                  'MEAS-150716-12_ele17_ele24.kwik',
                  'MEAS-150716-12_ele25_ele32.kwik',
                  'MEAS-150716-3_ele01_ele08.kwik',
                  'MEAS-150716-3_ele09_ele16.kwik',
                  'MEAS-150716-3_ele17_ele24.kwik',
                  'MEAS-150716-3_ele25_ele32.kwik',]

      files23 = [ 'MEAS-151027-1_ele01_ele08.kwik',
                  'MEAS-151027-1_ele09_ele16.kwik',
                  #'MEAS-151027-1_ele17_ele24.kwik', out of S2
                  #'MEAS-151027-1_ele25_ele32.kwik', out of S2
                  #'MEAS-151027-1_ele33_ele40.kwik', out of S2
                  #'MEAS-151027-1_ele41_ele48.kwik', out of S2
                  #'MEAS-151027-1_ele49_ele56.kwik', out of S2
                  #'MEAS-151027-1_ele57_ele64.kwik', out of S2
                  'MEAS-151027-2_ele01_ele08.kwik',
                  'MEAS-151027-2_ele09_ele16.kwik',
                  'MEAS-151027-2_ele17_ele24.kwik',
                  'MEAS-151027-2_ele25_ele32.kwik',
                  'MEAS-151027-2_ele33_ele40.kwik']#,
                  #'MEAS-151027-2_ele41_ele48.kwik',  out of S2
                  #'MEAS-151027-2_ele49_ele56.kwik',  out of S2
                  #'MEAS-151027-2_ele57_ele64.kwik']  out of S2

      files24 = [#'MEAS-151103-1_EXTRACTED_ele25_ele32.kwik',  no functional responses
                 'MEAS-151103-1_EXTRACTED_ele33_ele40.kwik',  
                 'MEAS-151103-1_EXTRACTED_ele41_ele48.kwik',  
                 'MEAS-151103-1_EXTRACTED_ele49_ele56.kwik',  
                 'MEAS-151103-1_EXTRACTED_ele57_ele64.kwik',
                 #'MEAS-151103-2_ele33_ele40.kwik',   no units
                 'MEAS-151103-2_ele41_ele48.kwik',
                 'MEAS-151103-2_ele49_ele56.kwik',
                 'MEAS-151103-2_ele57_ele64.kwik']

      #OUT OF S2
      files25 = [ 'MEAS-151105-1good_ele01_ele08.kwik',
                  'MEAS-151105-1good_ele09_ele16.kwik',
                  'MEAS-151105-1good_ele17_ele24.kwik',
                  'MEAS-151105-1good_ele25_ele32.kwik',
                  'MEAS-151105-1good_ele33_ele40.kwik',
                  'MEAS-151105-1good_ele41_ele48.kwik',
                  'MEAS-151105-1good_ele49_ele56.kwik',
                  'MEAS-151105-1good_ele57_ele64.kwik',
                  'MEAS-151105-2_ele01_ele08.kwik',
                  'MEAS-151105-2_ele09_ele16.kwik',
                  'MEAS-151105-2_ele17_ele24.kwik',
                  'MEAS-151105-2_ele25_ele32.kwik',
                  'MEAS-151105-2_ele33_ele40.kwik',
                  'MEAS-151105-2_ele41_ele48.kwik',
                  'MEAS-151105-2_ele49_ele56.kwik',
                  'MEAS-151105-2_ele57_ele64.kwik']

      files26 = [ 'MEAS-151110-1_ele01_ele08.kwik',
                  'MEAS-151110-1_ele09_ele16.kwik',
                  'MEAS-151110-1_ele17_ele24.kwik',
                  'MEAS-151110-1_ele25_ele32.kwik',
                  'MEAS-151110-1_ele33_ele40.kwik',
                  'MEAS-151110-1_ele41_ele48.kwik',
                  'MEAS-151110-1_ele49_ele56.kwik',
                  #'MEAS-151110-1_ele57_ele64.kwik', out of S2
                  'MEAS-151110-2_ele01_ele08.kwik',
                  'MEAS-151110-2_ele09_ele16.kwik',
                  'MEAS-151110-2_ele17_ele24.kwik',
                  'MEAS-151110-2_ele25_ele32.kwik']#,
                  #'MEAS-151110-2_ele33_ele40.kwik',  no units
                  #'MEAS-151110-2_ele41_ele48.kwik', out of S2
                  #'MEAS-151110-2_ele49_ele56.kwik', no units
                  #'MEAS-151110-2_ele57_ele64.kwik', no units
                  #'MEAS-151110-3_ele01_ele08.kwik',  out of S2
                  #'MEAS-151110-3_ele09_ele16.kwik',  out of S2
                  #'MEAS-151110-3_ele17_ele24.kwik',  out of S2
                  #'MEAS-151110-3_ele25_ele32.kwik',  out of S2
                  #'MEAS-151110-3_ele33_ele40.kwik',  out of S2
                  #'MEAS-151110-3_ele41_ele48.kwik',  out of S2
                  #'MEAS-151110-3_ele49_ele56.kwik',  no units
                  #'MEAS-151110-3_ele57_ele64.kwik']  no units

      files27  = ['MEAS-151112-1_ele01_ele08.kwik',
                  'MEAS-151112-1_ele09_ele16.kwik',
                  'MEAS-151112-1_ele17_ele24.kwik',
                  'MEAS-151112-1_ele25_ele32.kwik',
                  'MEAS-151112-1_ele33_ele40.kwik',
                  'MEAS-151112-1_ele41_ele48.kwik',
                  'MEAS-151112-1_ele49_ele56.kwik',
                  'MEAS-151112-1_ele57_ele64.kwik',
                  'MEAS-151112-2_ele01_ele08.kwik',
                  'MEAS-151112-2_ele09_ele16.kwik',
                  'MEAS-151112-2_ele17_ele24.kwik',
                  'MEAS-151112-2_ele25_ele32.kwik',
                  'MEAS-151112-2_ele33_ele40.kwik',
                  'MEAS-151112-2_ele41_ele48.kwik',
                  'MEAS-151112-2_ele49_ele56.kwik',
                  'MEAS-151112-2_ele57_ele64.kwik',
                  'MEAS-151112-3_ele01_ele08.kwik',
                  'MEAS-151112-3_ele09_ele16.kwik',
                  'MEAS-151112-3_ele17_ele24.kwik',
                  'MEAS-151112-3_ele25_ele32.kwik',
                  'MEAS-151112-3_ele33_ele40.kwik',
                  'MEAS-151112-3_ele41_ele48.kwik',
                  'MEAS-151112-3_ele49_ele56.kwik',
                  'MEAS-151112-3_ele57_ele64.kwik']

      files28 =  ['MEAS-151116-1_ele01_ele08.kwik',
                  'MEAS-151116-1_ele09_ele16.kwik',
                  'MEAS-151116-1_ele17_ele24.kwik',
                  'MEAS-151116-1_ele25_ele32.kwik',
                  'MEAS-151116-1_ele33_ele40.kwik',
                  'MEAS-151116-1_ele41_ele48.kwik',
                  'MEAS-151116-1_ele49_ele56.kwik',
                  #'MEAS-151116-1_ele57_ele64.kwik',
                  'MEAS-151116-2_ele01_ele08.kwik',
                  'MEAS-151116-2_ele09_ele16.kwik',
                  'MEAS-151116-2_ele17_ele24.kwik',
                  'MEAS-151116-2_ele25_ele32.kwik',
                  'MEAS-151116-2_ele33_ele40.kwik',
                  'MEAS-151116-2_ele41_ele48.kwik',
                  'MEAS-151116-2_ele49_ele56.kwik',
                  'MEAS-151116-2_ele57_ele64.kwik',
                  'MEAS-151116-3_ele01_ele08.kwik',
                  'MEAS-151116-3_ele09_ele16.kwik',
                  'MEAS-151116-3_ele17_ele24.kwik',
                  'MEAS-151116-3_ele25_ele32.kwik',
                  'MEAS-151116-3_ele33_ele40.kwik',
                  'MEAS-151116-3_ele41_ele48.kwik',
                  'MEAS-151116-3_ele49_ele56.kwik',
                  'MEAS-151116-3_ele57_ele64.kwik']

      files29  = ['MEAS-151118-1_ele01_ele08.kwik',
                  'MEAS-151118-1_ele09_ele16.kwik',
                  'MEAS-151118-1_ele17_ele24.kwik',
                  'MEAS-151118-1_ele25_ele32.kwik',
                  'MEAS-151118-1_ele33_ele40.kwik',
                  'MEAS-151118-1_ele41_ele48.kwik',
                  'MEAS-151118-1_ele49_ele56.kwik',
                  'MEAS-151118-1_ele57_ele64.kwik',
                  'MEAS-151118-2_ele01_ele08.kwik',
                  'MEAS-151118-2_ele09_ele16.kwik',
                  'MEAS-151118-2_ele17_ele24.kwik',
                  'MEAS-151118-2_ele25_ele32.kwik',
                  'MEAS-151118-2_ele33_ele40.kwik',
                  'MEAS-151118-2_ele41_ele48.kwik',
                  'MEAS-151118-2_ele49_ele56.kwik',
                  'MEAS-151118-2_ele57_ele64.kwik',
                  'MEAS-151118-3_ele01_ele08.kwik',
                  'MEAS-151118-3_ele09_ele16.kwik',
                  'MEAS-151118-3_ele17_ele24.kwik',
                  'MEAS-151118-3_ele25_ele32.kwik',
                  'MEAS-151118-3_ele33_ele40.kwik',
                  'MEAS-151118-3_ele41_ele48.kwik',
                  'MEAS-151118-3_ele49_ele56.kwik',
                  'MEAS-151118-3_ele57_ele64.kwik']


      files30  = ['MEAS-151208-2_ele01_ele08.kwik',
                  'MEAS-151208-2_ele09_ele16.kwik',
                  'MEAS-151208-2_ele17_ele24.kwik',
                  'MEAS-151208-2_ele25_ele32.kwik',
                  'MEAS-151208-2_ele33_ele40.kwik',
                  'MEAS-151208-2_ele41_ele48.kwik',
                  'MEAS-151208-2_ele49_ele56.kwik',
                  'MEAS-151208-2_ele57_ele64.kwik',
                  'MEAS-151208-3_ele01_ele08.kwik',
                  'MEAS-151208-3_ele09_ele16.kwik',
                  'MEAS-151208-3_ele17_ele24.kwik',
                  'MEAS-151208-3_ele25_ele32.kwik',
                  'MEAS-151208-3_ele33_ele40.kwik',
                  'MEAS-151208-3_ele41_ele48.kwik',
                  'MEAS-151208-3_ele49_ele56.kwik',
                  'MEAS-151208-3_ele57_ele64.kwik',
                  'MEAS-151208-4_ele01_ele08.kwik',
                  'MEAS-151208-4_ele09_ele16.kwik',
                  'MEAS-151208-4_ele17_ele24.kwik',
                  'MEAS-151208-4_ele25_ele32.kwik',
                  'MEAS-151208-4_ele33_ele40.kwik',
                  'MEAS-151208-4_ele41_ele48.kwik',
                  'MEAS-151208-4_ele49_ele56.kwik',
                  'MEAS-151208-4_ele57_ele64.kwik',
                  'MEAS-151208-5_ele01_ele08.kwik',
                  'MEAS-151208-5_ele09_ele16.kwik',
                  'MEAS-151208-5_ele17_ele24.kwik',
                  'MEAS-151208-5_ele25_ele32.kwik',
                  'MEAS-151208-5_ele33_ele40.kwik',
                  'MEAS-151208-5_ele41_ele48.kwik',
                  'MEAS-151208-5_ele49_ele56.kwik',
                  'MEAS-151208-5_ele57_ele64.kwik']


      files31 = [ #'MEAS-151210-1_ele01_ele08.kwik',  no units
                  #'MEAS-151210-1_ele09_ele16.kwik',  no units
                  #'MEAS-151210-1_ele17_ele24.kwik',  no units
                  #'MEAS-151210-1_ele25_ele32.kwik',  no units
                  #'MEAS-151210-1_ele33_ele40.kwik',  no units
                  'MEAS-151210-1_ele41_ele48.kwik',
                  'MEAS-151210-1_ele49_ele56.kwik',
                  'MEAS-151210-1_ele57_ele64.kwik',
                  #'MEAS-151210-2_ele01_ele08.kwik',   out of S2
                  #'MEAS-151210-2_ele09_ele16.kwik',   out of S2
                  #'MEAS-151210-2_ele17_ele24.kwik',   out of S2
                  #'MEAS-151210-2_ele25_ele32.kwik',   out of S2
                  'MEAS-151210-2_ele33_ele40.kwik',
                  'MEAS-151210-2_ele41_ele48.kwik',
                  'MEAS-151210-2_ele49_ele56.kwik',
                  'MEAS-151210-2_ele57_ele64.kwik',
                  #'MEAS-151210-3_ele01_ele08.kwik',   out of S2
                  #'MEAS-151210-3_ele09_ele16.kwik',   no units
                  #'MEAS-151210-3_ele17_ele24.kwik',   no units
                  #'MEAS-151210-3_ele25_ele32.kwik',   out of S2
                  'MEAS-151210-3_ele33_ele40.kwik',
                  'MEAS-151210-3_ele41_ele48.kwik',
                  'MEAS-151210-3_ele49_ele56.kwik',
                  'MEAS-151210-3_ele57_ele64.kwik']

      files32 = [ 'MEAS-151214-1_ele01_ele08.kwik',
                  'MEAS-151214-1_ele09_ele16.kwik',
                  'MEAS-151214-1_ele17_ele24.kwik',
                  'MEAS-151214-1_ele25_ele32.kwik',
                  'MEAS-151214-1_ele33_ele40.kwik',
                  'MEAS-151214-2_ele01_ele08.kwik',
                  'MEAS-151214-2_ele09_ele16.kwik',
                  'MEAS-151214-2_ele17_ele24.kwik',
                  'MEAS-151214-2_ele25_ele32.kwik',
                  'MEAS-151214-2_ele33_ele40.kwik']

      #--------------------------------------------------------------------------------
      #--------------------------------------------------------------------------------
      # Here I create my dictionary of experiments
      Expe={}
      Vtags={}
      Stim={}
      for num in ExpeNum: 
          Expe[num] = dict()
          Vtags[num] = dict()
      #---------------------------------------
      i=0        
      for meas in np.append(m164[0:4],m364[0:2]):
          Expe[20][meas] = files20[i]
          i+=1
      #---------------------------------------
      i=0 
      for meas in np.append(m164[0:4],m364[0:4]):
          Expe[22][meas] = files22[i]
          i+=1
      #---------------------------------------
      i=0 
      for meas in np.append(m164[0:2],m264[0:5]):
          Expe[23][meas] = files23[i]
          i+=1
      #---------------------------------------
      i=0
      for meas in np.append(m164[4:8],m264[5:8]):    
          Expe[24][meas] = files24[i]
          i+=1
      #---------------------------------------
      i=0 
      for meas in np.append(m164,m264):    
          Expe[25][meas] = files25[i]
          i+=1
      #---------------------------------------
      i=0
      for meas in np.append(m164[0:7],m264[0:4]):
          Expe[26][meas] = files26[i]
          i+=1
      #---------------------------------------
      i=0
      for meas in np.append(np.append(m164[0:7],m264),m364):    
          Expe[28][meas] = files28[i]
          i+=1
      #---------------------------------------    
      i=0
      for meas in np.append(np.append(m164,m264),m364):    
          Expe[27][meas] = files27[i]
          Expe[29][meas] = files29[i]
          Expe[30][meas] = files30[i]
          i+=1
      #---------------------------------------    
      for meas in m464:
          Expe[30][meas] = files30[i]
          i+=1
      i=0
      #---------------------------------------    
      i=0
      for meas in np.append(np.append(m164[5:8],m264[4:8]),m364[4:8]):    
          Expe[31][meas] = files31[i]
          i+=1
      i=0
      #---------------------------------------    
      for meas in np.append(m164[0:5],m264[0:5]):
          Expe[32][meas] = files32[i]
          i+=1

      #--------------------------------------------------------------------------------
      #Vtag files 
      Vtags[20] = ['MEAS-150707-1_Vtag1.dat','nada','MEAS-150707-23_Vtag1.dat']
      Vtags[22] = ['MEAS-150716-12_Vtag1.dat','nada','MEAS-150716-3_Vtag1.dat']
      Vtags[23] = ['MEAS-151027-1_Vtag1.dat','MEAS-151027-2_Vtag1.dat']
      Vtags[23] = ['MEAS-151027-1_Vtag1.dat','MEAS-151027-2_Vtag1.dat']
      Vtags[24] = ['MEAS-151103-1_Vtag1.dat','MEAS-151103-2_Vtag1.dat']
      Vtags[25] = ['MEAS-151105-1good_Vtag1.dat','MEAS-151105-2_Vtag1.dat']
      Vtags[26] = ['MEAS-151110-1_Vtag1.dat','MEAS-151110-2_Vtag1.dat','MEAS-151110-3_Vtag1.dat']
      Vtags[27] = ['MEAS-151112-1_Vtag1.dat','MEAS-151112-2_Vtag1.dat','MEAS-151112-3_Vtag1.dat']
      Vtags[28] = ['MEAS-151116-1_Vtag1.dat','MEAS-151116-2_Vtag1.dat','MEAS-151116-3_Vtag1.dat']
      Vtags[29] = ['MEAS-151118-1_Vtag1.dat','MEAS-151118-2_Vtag1.dat','MEAS-151118-3_Vtag1.dat']
      Vtags[30] = ['MEAS-151208-2_Vtag1.dat','MEAS-151208-3_Vtag1.dat','MEAS-151208-4_Vtag1.dat','MEAS-151208-5_Vtag1.dat']
      Vtags[31] = ['MEAS-151210-1_Vtag1.dat','MEAS-151210-2_Vtag1.dat','MEAS-151210-3_Vtag1.dat']
      Vtags[32] = ['MEAS-151214-1_Vtag1.dat','MEAS-151214-2_Vtag1.dat']

      #--------------------------------------------------------------------------------
      #Stimulus type
      for i in range(23,33):
          Stim[i] = 'big_STIM_FC_corrected'
      for i in range(15,23):
          Stim[i] = 'big_STIM'
      for i in range(10,15):
          Stim[i] = 'small_STIM'  
          
      #--------------------------------------------------------------------------------
      #Root folder to work in, such all will be in subfolders 
      #e.g.: "/EXP_23/m1s1/" for data or "/STIM/" for stims
      rootF = '/home/matias/WORKSPACE/'    
      stimFolder = rootF +'STIM/'

      #I have a separate folder for exp 22 and before
      rootF_kwiks = rootF    #uncomment this to work with the other root folder
      #rootF_kwiks = '/media/matias/DATA/WORKSPACE2/'


      return Expe, Vtags, Stim, rootF, stimFolder
