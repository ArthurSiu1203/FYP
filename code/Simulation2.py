#!/usr/bin/env python
# coding: utf-8

# In[45]:


from phase_bpmn import bpmnToDict
from event_log import write_log
import logging
from datetime import datetime
import time

import pandas as pd
import pm4py

import random


# In[46]:


"""
Function for finding the start and end event of a given process dictionay

Variables
---------
process_dict: dict
    a transformed dictionay with bpmnToDict()
    
Return
------
start_and_end: list
    start_and_end[0] = start_event
    start_and_end[1] = end_event

"""
def find_start_end_event(process_dict):
    start_and_end = list()
    start_event, end_event = ("","")
    for keys, values in process_dict.items():
        if 'type' in values:
            for value in values.values():
                if value == "startEvent":
                    start_event = keys
                    logging.info("start_event=" + start_event)
                elif value == "endEvent":
                    end_event = keys
                    logging.info("end_event=" + end_event)
    #raise error if startEvent or endEvent not found
    if start_event == "" or end_event == "":
        raise Exception("Your bpmn process must contain a startEvent and endEvent.")
    else:
        start_and_end.append(start_event)
        start_and_end.append(end_event)
        return start_and_end


# In[47]:


"""
Add a given event id into a specific process path

Variables
---------
process_path
    the process main path of current simulation

Return
------
process_path
    appended process path
"""
def addToMainPath(process_path:list(), idstr: str):
    process_path.append(idstr)
    return process_path


# In[48]:


"""
Check the outgoing number of a given event/object

Variables
---------
processDict: dict
    the transformed process dictionary

event_id: str
    the target event_id to check for the number of outgoinh

Return
------
outgoing: int
    number if outgoing

"""
def check_outgoing_number(processDict: dict, event_id:str):
    detail_of_given_id = processDict[event_id]
    try:
        outgoing = detail_of_given_id["outgoing"]
    except:
        outgoing = ""
    return len(outgoing)
# print(check_outgoing_number(process_dict, end_event))


# In[49]:


"""
Check the type of a given event

Variables
---------
processDict: dict
    the transformed process dictionary
    
event_id: int
    the target event_id to check type
    
Return
------
type_of_event: str
    the type of the given event

"""
def checkType(processDict: dict, event_id:str):
    detail_of_given_id = processDict[event_id]
    if  isinstance(detail_of_given_id, list) or isinstance(detail_of_given_id, str):
        type_of_event = "flow"
    else:
        type_of_event = detail_of_given_id["type"]
        
    return type_of_event


# In[50]:


"""
Check if outgoing flow have content, if do, add in main path

Variables
---------
processDict: dict
    the transformed process dictionary

flow_id: str
    the target flow id

process_path: list
    the process main path of current simulation

Return
------
process_path
    appended process path

"""
def checkAndAddFlowToMain(processDict: dict, flow_id: str, process_path: list):
    flow_detail = processDict[flow_id]
    if len(flow_detail) > 0:
        process_path.append(flow_id)
#         print(flow_detail)
        return process_path
    else:
        return process_path


# In[51]:


"""
Use the current id's outgoing find next event/object

Variables
---------
processDict: dict
    the transformed process dictionary

flow_id: str
    the flow id of current object's outgoing

Return
------
target_event_id: str
    Id of the next target object
    -if retunr = "": no next object

"""
def findNextWithOneOutgoing(processDict: dict, flow_id: str):
    target_event_id = ""
    for event in processDict:
        event_detail = processDict[event]
        if isinstance(event_detail, dict):
            if "incoming" in event_detail:
                if flow_id in event_detail["incoming"]:
                    target_event_id = event
    return target_event_id


# In[52]:


def parallelGatewayHandling(process_dict, gateway_id):
    list_of_gateway_path = list()
    outgoings = process_dict[gateway_id]["outgoing"]
    outgoing_set = set()
#     for outgoing_id in outgoings:
#         outgoing_set.add(outgoing_id)
    random.shuffle(outgoings)
#     print(outgoings)
    for outgoing_id in outgoings:
        return_path = parallelGatewayLoop(process_dict, outgoing_id, list_of_gateway_path)
    return return_path        


# In[53]:


def parallelGatewayLoop(process_dict, flow_id, list_of_gateway_path):
    next_event_id = findNextWithOneOutgoing(process_dict, flow_id)
    current_type = checkType(process_dict, next_event_id)
    if  current_type != "exclusiveGateway" and current_type != "parallelGateway":
        list_of_gateway_path.append(next_event_id)
        next_outgoing_flow_id = process_dict[next_event_id]['outgoing'][0]
        return_list = parallelGatewayLoop(process_dict, next_outgoing_flow_id, list_of_gateway_path)
    elif current_type == "exclusiveGateway":
        current_outgoing_number = check_outgoing_number(process_dict, next_event_id)
        random_path = random.randint(1,current_outgoing_number)
        random_next_flow = process_dict[next_event_id]["outgoing"][random_path-1]
        return_list = parallelGatewayLoop(process_dict, random_next_flow, list_of_gateway_path)
    elif current_type == "parallelGateway":
        if check_outgoing_number(process_dict,next_event_id)==1:
            logging.info("This path of gateway closed")
            return_list = list()
            return_list.append(list_of_gateway_path)
            return_list.append(next_event_id)
        else:
            next_list = parallelGatewayHandling(process_dict, next_event_id)
            next_list_content = next_list[0]
            list_of_gateway_path.append(next_list_content)
            next_outgoing_flow_id = process_dict[next_list[1]]['outgoing'][0]
            return_list = parallelGatewayLoop(process_dict, next_outgoing_flow_id, list_of_gateway_path)
    return return_list


# In[63]:


"""
Run (number_of_sim) times simulation based on the given bpmn location

Variables
---------
number_of_sim: int
    number of times that run the simulation

bpmn_loc: str, optional
    the file path of the target bpmn file


Return
---------
Void function, generate log location:
    "event_log.txt"

"""
def do_simulate(number_of_sim: int, bpmn_loc: str= "resources/bpmn.bpmn"):
    process_dict = bpmnToDict(bpmn_loc)
    log_id = 0
    start_and_end = find_start_end_event(process_dict)
    start_event = start_and_end[0]
    end_event = start_and_end[1]
    while log_id < number_of_sim:
        log_id = log_id + 1
        #Variables
        process_path = list();
        #for parallel gateway
        current_layer = 0;
        current_In_Layer = 0;
        handled_gateway = []
        
        current_event = start_event
        new_event = ""
        while current_event != end_event:
            current_id = current_event
            current_type = checkType(process_dict, current_id)
            if current_type != "exclusiveGateway" and current_type != "parallelGateway":
                #Normal path
                current_outgoing_number = check_outgoing_number(process_dict, current_id)
                if current_outgoing_number > 1:
                    raise Exception("Non-gateway event can only contain one outgoing path.")
                elif current_outgoing_number == 0:
#                     print(current_outgoing_number)
                    if current_type == "endEvent":
#                         print(current_type)
                        #EndEvent
                        process_path = addToMainPath(process_path,current_id)
                        new_event = end_event
                    else:
                        raise Exception("Event must contain outgoing.")
                elif current_outgoing_number == 1:
                    process_path = addToMainPath(process_path,current_id)
                    process_path = checkAndAddFlowToMain(process_dict, process_dict[current_id]["outgoing"][0],process_path)
                    new_event =  findNextWithOneOutgoing(process_dict, process_dict[current_id]["outgoing"][0])
                else:
                    raise Exception("Events have no outgoing.")
            else:
                if current_type == "exclusiveGateway":
                    #TODO: random generate a number for different path
                    current_outgoing_number = check_outgoing_number(process_dict, current_id)
                    random_path = random.randint(1,current_outgoing_number)
                    random_next_event = process_dict[current_id]["outgoing"][random_path-1]
                    handled_gateway.append(current_id)
                    new_event = findNextWithOneOutgoing(process_dict, random_next_event)
                elif current_type == "parallelGateway":
                    #TODO: parallel gateway path
                    return_path = parallelGatewayHandling(process_dict, current_id)
                    using_path = return_path[0]
                    for ids in using_path:
                        if isinstance(ids,list):
                            list_list = list_handling(ids, list())
                            for list_item in list_list:
                                process_path = addToMainPath(process_path,list_item)
                        else:
                            process_path = addToMainPath(process_path,ids)
                    process_path = checkAndAddFlowToMain(process_dict, process_dict[return_path[1]]["outgoing"][0],process_path)
                    new_event =  findNextWithOneOutgoing(process_dict, process_dict[return_path[1]]["outgoing"][0])
#                     if len(process_dict[current_id]["outgoing"])>1:
#                         new_event =  findNextWithOneOutgoing(process_dict, process_dict[current_id]["outgoing"][1])
#                     else:
#                         new_event =  findNextWithOneOutgoing(process_dict, process_dict[current_id]["outgoing"][0])
                else:
                    raise Exception("Wrong gateway type found")
            current_event = new_event
        #write process
        if process_path != None:
            for event in process_path:
                if checkType(process_dict, event) != "startEvent" and checkType(process_dict, event) != "endEvent":
                    event_name =  process_dict[event]['name']
#                     print(event_name)
                    import_time = datetime.now()
                    write_log(log_id,event_name,import_time)
                    time.sleep(0.5)
        

def list_handling(ids, final_list):
    for list_item in ids:
        if isinstance(list_item,list):
            final_list = list_handling(list_item, final_list)
        else:
            final_list.append(list_item)
    return final_list

