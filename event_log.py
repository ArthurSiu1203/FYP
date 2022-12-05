#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os.path
import logging
from datetime import datetime


# In[41]:


def write_log(log_id: int,log_text: str, time: datetime = datetime.now()):
    """
    variables
    ---------
    log_id: integer
        ID of the process
    log_text: string
        Text to be shown in the log
    time: datetime, optional
        datetime of the log, default as current timestamp
    
    """
    log_id = str(log_id)
    if os.path.exists('event_log.txt'):
        with open('event_log.txt','a') as event_log:
            event_log.write('\n'+log_id+'\t'+log_text+'\t'+str(time))
        logging.info('write log at '+str(time))
    else:
        write_text = log_id+'\t'+log_text+'\t'+str(time)
        with open('event_log.txt','w') as event_log:
            event_log.write(write_text)
        logging.info('write log at '+str(time))


# In[42]:


def clear_log():
    if os.path.exists('event_log.txt'):
        os.remove("event_log.txt")

