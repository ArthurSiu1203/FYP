#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from Pm4pyHandling3 import *
from Simulation2 import do_simulate
from event_log import clear_log

import logging


# In[ ]:


resource_changed = str(input("Have you changed the BPMN default file location in resources file? (Y/N) "))
if resource_changed == "Y":
    resource_link = str(input("Please specified the changed location: "))
clear_log()
num_of_sim = int(input("Please specified the number of simulation you want to do. (integer)"))
print("Start simulation procedure. Please wait...")
do_simulate(num_of_sim)
print("Finished Simulation procedure.")
if resource_changed == "Y":
    plot_conformance_graph(bpmn_loc = resource_link)
    plot_precision_graph(bpmn_loc = resource_link)
else:
    plot_conformance_graph()
    plot_precision_graph()

