#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import xml.etree.ElementTree as ET
import logging


# In[ ]:


def bpmnToDict(resource_link: str):
    """
    variables
    ---------
    resource_link: string
        link of the bpmn file
        
    return
    ------
    process_dict
        -data structure being used for storing the imported process
    """
    """
    definition
    ----------
    root
    -the xml root
    -root[0] = bmpn model
    -root[1] = bpmn di (not using)
    """
    tree = ET.parse(resource_link)
    roots = tree.getroot()
    process_dict = dict()
    
    logging.info(roots.tag)
    logging.info(roots[0].tag)
    logging.info(roots[0].attrib)
    
    """
    file_number
        -the number of the bpmn file
    --version_number
    """
    if roots.tag[-11:]!='definitions':
        raise Exception("Your bpmn file must have a definitions tag included")
        file_number = ''
        length_file_number = 0
    else:
        file_number = roots.tag[0:-11]
        length_file_number = len(file_number)
        
    logging.info(file_number)
    
    process_dict['file_number']=file_number
    
    #Create dictionay for storing the process
    count = 0
    for child in roots[0]:
        count+=1
        #print(child.tag, child.attrib)
        process_dict[child.attrib["id"]]=""
        if child.tag == file_number+"sequenceFlow":
            #Handling for flow situation
            if "name" in child.attrib:
                #if name is exist in a flow, save it as the value
                #print(child.attrib["name"])
                process_dict[child.attrib["id"]] = child.attrib["name"]
            else:
                process_dict[child.attrib["id"]]= ""
        else:
            #Create dict store as the value of the base dict
            inner_dict = {}
            if "name" in child.attrib:
                inner_dict["name"] = child.attrib["name"]
            for action in child:
                inner_dict["type"] = child.tag[length_file_number:]
                if action.tag[length_file_number:] in inner_dict:
                    inner_dict[action.tag[length_file_number:]].append(action.text)
                else:
                    inner_dict[action.tag[length_file_number:]] = [action.text]
            process_dict[child.attrib["id"]] = inner_dict
            
            
            
    #     for action in child:
    #         if action == "":
    #             print("Null")
    
    
    logging.info(process_dict)
    logging.info(count)
    logging.info(len(process_dict))
    return process_dict


# In[ ]:


# """
# process_dict
#     -data structure being used for storing the imported process
# root
#     -the xml root
#     -root[0] = bmpn model
#     -root[1] = bpmn di (not using)

# """
# tree = ET.parse('resources/bpmn.bpmn')
# roots = tree.getroot()
# process_dict = dict()


# In[ ]:


# print(roots.tag)


# In[ ]:


# print(roots[0].tag)
# print(roots[0].attrib)


# In[ ]:


# """
# file_number
#     -the number of the bpmn file
# --version_number
# """
# if roots.tag[-11:]!='definitions':
#     raise Exception("Your bpmn file must have a definitions tag included")
#     file_number = ''
# else:
#     file_number = roots.tag[0:-11]
    
# print(file_number)


# In[ ]:


# print(roots[0].findall(f"{file_number}startEvent"))


# In[ ]:


# for exclusiveGateway in roots[0].findall(f"{file_number}startEvent"):
#     print(exclusiveGateway.find(f"{file_number}outgoing"))


# In[ ]:


# #Check number of startEvent
# number_start_event = roots[0].findall(f"{file_number}startEvent")
# # if number_start_event > 1 or number_start_event < 1:
# #     raise Exception("Your bpmn file must contain a single startEvent")
    


# In[ ]:


# #Create dictionay for storing the process
# count = 0
# for child in roots[0]:
#     count+=1
#     #print(child.tag, child.attrib)
#     process_dict[child.attrib["id"]]=""
#     if child.tag == file_number+"sequenceFlow":
#         #Handling for flow situation
#         if "name" in child.attrib:
#             #if name is exist in a flow, save it as the value
#             #print(child.attrib["name"])
#             process_dict[child.attrib["id"]] = child.attrib["name"]
#         else:
#             process_dict[child.attrib["id"]]= ""
#     else:
#         #Create dict store as the value of the base dict
#         inner_dict = {}
#         if "name" in child.attrib:
#             inner_dict["name"] = child.attrib["name"]
#         for action in child:
#             if action.tag in inner_dict:
#                 inner_dict[action.tag].append(action.text)
#             else:
#                 inner_dict[action.tag] = [action.text]
#         process_dict[child.attrib["id"]] = inner_dict
        
        
        
# #     for action in child:
# #         if action == "":
# #             print("Null")
    

# print(process_dict)
# print(count)
# print(len(process_dict))


# In[ ]:


# def tag_transform(tags: str, root:ET.Element):
#     parent = root.findall(tags).attrib['id']
#     #check if it is a sequenceFlow
#     print(parent)
    
# #     for direction in parent:
# #         if process_dict[parent.tag+"_"+parent.attrib["id"]] != None:
            
# #         print(child.text)
# #     print(parent.tag+"_"+parent.attrib["id"])


# In[ ]:


# tag_transform(f"{file_number}sequenceFlow",roots[0])


# In[ ]:


# print(process_dict)


# In[ ]:


# dt = bpmnToDict("resources/bpmn.bpmn")


# In[ ]:


# print(dt)


# In[ ]:




