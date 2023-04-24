#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import pm4py

import matplotlib.pyplot as plt
from pm4py.algo.evaluation.generalization import algorithm as generalization_evaluator
from pm4py.algo.evaluation.simplicity import algorithm as simplicity_evaluator
from pm4py.algo.conformance.alignments.edit_distance import algorithm as logs_alignments
from pm4py.algo.conformance.alignments.decomposed import algorithm as decomp_alignments
import time
import warnings
from pandas.core.common import SettingWithCopyWarning
from matplotlib.ticker import MaxNLocator

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


# In[7]:


"""
Plot the conformance checking graph by comparing a generated simulation event log with a bpmn file

Variables
---------
file_path: str, optional
    the file path of the generated simulation event log
    default: event_log.txt, only accepy .txt file
bpmn_loc: str, optional
    the location of the original bpmn model used for simulation
    default: resources/bpmn.bpmn

"""
def plot_conformance_graph(file_path:str = "event_log.txt", bpmn_loc:str = "resources/bpmn.bpmn"):
    #Get file name
    if file_path[-4:] != ".txt":
        raise Exception("The given file path type is not-valid (Only accept .txt file)")
    else:
        file_name = file_path[:-4]
    
    new_file_path = file_name+".csv"
    #File type transformation
    read_file = pd.read_csv(file_path,sep='\t')
    read_file.to_csv(new_file_path, index=None, sep=';')
    
    dataframe = pd.read_csv(new_file_path, sep=';')
    dataframe = pm4py.format_dataframe(dataframe, case_id='LogID', activity_key='Event', timestamp_key='Time')
    
    bpmn = pm4py.read_bpmn(bpmn_loc)
    net, im, fm = pm4py.convert_to_petri_net(bpmn)
#     pm4py.view_petri_net(net, im, fm)
    trace = pm4py.conformance_diagnostics_token_based_replay(dataframe, net, im, fm)
    
    #Ploting using matplotlib
    data_no_list = list(range(len(trace)+1))
    actual_list = list()
    actual_list.append(0)
    for traces in trace:
        trace_fitness = traces['trace_fitness'] * 100
        actual_list.append(trace_fitness)
    plt.plot(data_no_list, actual_list, label="Conformance fitness")
    plt.xlabel("Number of trace(s)")
    plt.ylabel("Conformance fitness")


# In[11]:


def plot_precision_graph(file_path:str = "event_log.txt", bpmn_loc:str = "resources/bpmn.bpmn", mode:int = 0):
     #Get file name
    if file_path[-4:] != ".txt":
        raise Exception("The given file path type is not-valid (Only accept .txt file)")
    else:
        file_name = file_path[:-4]
    
    new_file_path = file_name+".csv"
    #File type transformation
    read_file = pd.read_csv(file_path,sep='\t')
    read_file.to_csv(new_file_path, index=None, sep=';')
    
    dataframe = pd.read_csv(new_file_path, sep=';')
    #Getting the maximum number of the logs
    maxcolumn = dataframe["LogID"].max()
    bpmn = pm4py.read_bpmn(bpmn_loc)
    net, im, fm = pm4py.convert_to_petri_net(bpmn)
    loop_index = 0
    data_no_list = list(range(maxcolumn+1))
    prec_data = list()
    prec_data.append(0)
    gen_data = list()
    gen_data.append(0)
    while loop_index < maxcolumn:
        dataframe_query = dataframe.query('LogID <= '+str(loop_index+1))
        dataframe_query = pm4py.format_dataframe(dataframe_query, case_id='LogID', activity_key='Event', timestamp_key='Time')
        if mode == 1:
            prec = pm4py.precision_alignments(dataframe_query, net, im, fm)
            prec_data.append(prec*100)
        elif mode == 2:
            gen = generalization_evaluator.apply(dataframe_query, net, im, fm)
            gen_data.append(gen*100)
        elif mode == 0:
            prec = pm4py.precision_alignments(dataframe_query, net, im, fm)
            gen = generalization_evaluator.apply(dataframe_query, net, im, fm)
            prec_data.append(prec*100)
            gen_data.append(gen*100)
        else:
            prec = pm4py.precision_alignments(dataframe_query, net, im, fm)
            gen = generalization_evaluator.apply(dataframe_query, net, im, fm)
            prec_data.append(prec*100)
            gen_data.append(gen*100)
        loop_index = loop_index + 1
    print("Data handling finished")

    if mode == 1:
        plt.plot(data_no_list, prec_data, label="Precision")
    elif mode == 2:
        plt.plot(data_no_list, gen_data, label="Generalization")
    elif mode == 0:
        plt.plot(data_no_list, prec_data, label="Precision")
        plt.plot(data_no_list, gen_data, label="Generalization")
    else:
        plt.plot(data_no_list, prec_data, label="Precision")
        plt.plot(data_no_list, gen_data, label="Generalization")
    plt.xlabel("Number of trace(s)")
#     plt.xticks(data_no_list)
#     plt.axes().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.ylabel("Percentages")
    plt.legend()
    plt.show()

