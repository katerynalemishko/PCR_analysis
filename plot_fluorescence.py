

# This script takes as input a name of a directory containing experimental data, e.g. 'experiment1'
# It generates a data frame from all the data in the directory corresponding to one particular experiment.

# Note that your working directory should contain a directory 'Experimental Data' containing deirectories corresponding to #different experiments: 'experiment1', 'experiment2', etc. So you can use this script together with the 'Experimental Data'
#on your local machine

#The script generates two .png files containing plots of the data.
# One plot contains all the time series in a single subplot
# The second plot consists of 8 subplots with the data divided in 9 time series per subplot


# Import necessary packages
import glob
import ast

import os

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")


# Take a name of a directory as input from the command line
directory_name = input("Enter name of the directory with experimental data: ")


###############     Define functions        #################



#########   Function to  extract data correscponding to one cycle   ######

def extract_from_file(data,n_wells=72):
    
    """A function that extracts fluorescence data from one pcr cycle"""
    
    cycle=[]
    
    # iterrate over all floorescence values measured for all the wells for each pcr cycle
    for i in range(n_wells):
        cycle.append(data[i][2])# append fluorescence values to a cycle list 
        
    return(cycle)



#####  Function that returns a data structure created out of all the data from an experiment #####

def extract_data(path):
    
    """A function that extracts fluorescence data from all the files from an experiment
     and returns a resulting data structure in the form of list of lists"""
    
    files = glob.glob(path) 
    data_structure=[]

    # Read and extract data from all text files in the directory. The fluorescence data from all the files will be
    #written in the data_structure list of lists
    for name in files:
        with open(name) as f:
    
            data = f.read()
            data=ast.literal_eval(data)
            cycle=(extract_from_file(data))
            data_structure.append(cycle)       
            
    return(data_structure)  



#########   Function to  represent all time series in one plot   ######

def plot_fluorescence(df,n_wells=72):
    """A function that plots all fluorescence data in one plot"""
    
    fig, ax=plt.subplots(figsize=(10,7))
    
    for i in range(n_wells):
        ax.plot(df.index,df.iloc[:,i+1],label=df.columns[i+1])
    
   
    plt.ylabel('Fluorescence',fontsize=16)
    plt.xlabel('Cycle number',fontsize=16)
    plt.title('Fluorescence over a time course during a PCR',fontsize=18)
    plt.legend(ncol=3,bbox_to_anchor=(0.,-0.100, 1.55, 1.15), loc=1,prop={'size': 12})
    plt.savefig(str(directory_name)+'_1_subplot.png',bbox_inches='tight') 


    
#########   Function to split time series in 8 subplotsplot   ######

def subplots_fluorescence(df):
    
     """A function that divides fluorescence data in 8 subplots"""
     
     fig, ax=plt.subplots(4,2, figsize=(25,20))
    
     n=1
    
     for row in range(4):
        for col in range(2):
            
            for i in range(9):
                
                ax[row,col].plot(df.index,df.iloc[:,n+i],label=df.columns[n+i])
        
            n=n+9
            ax[row,col].legend(frameon=False,loc='upper left',fontsize=14)
            ax[row,col].set_xlim([-7, 41])
            ax[row,col].set_ylabel('Fluorescence',fontsize=18)
            ax[row,col].set_xlabel('Cycles',fontsize=18)
            ax[row,col].tick_params(labelsize=15)
            
                            
        plt.suptitle('Fluorescence over a time course during a PCR',fontsize=22,y=0.91)
     plt.savefig(str(directory_name)+'_8_subplots.png')   


    

#####  Create a data structure out of all the data from an experiment #####

# Set a path to the data files
path=os.getcwd().replace('\\','/')+'/Experimental Data/'+str(directory_name)+'/*.txt'


data_structure=extract_data(path)  

# Variables containing number of cycles and number of wells
n_cycles=len(data_structure)
n_dwells=72

#  Generating names for each column containing data from one well
col_names=['well_' + str(i) for i in range(1,n_dwells+1)]

# Generate labels indicationg the number of pcr cycle
index_names=['cycle_' + str(i) for i in range(n_cycles)]


# Create a data frame from the data_stracture. Each column of the data frame contains data for one of the 72 wells
fluorescence_data = pd.DataFrame(data_structure, columns = col_names)

# Insert a column containing labels indication the cycle number
fluorescence_data.insert (0, "cycle_number", index_names)

# Generate plots
plot_fluorescence(fluorescence_data)
subplots_fluorescence(fluorescence_data)
