# RUTIFU - Random Utilities That I Find Useful

import syslog
import os
import time
import threading
import traceback
import executor
import json
import socket

################################################################################
# Logging and debugging
################################################################################
sysLogging = True
# optionally import app specific configuration
try:
    from debugConf import *
except ImportError:
    pass
# log a message to syslog or stdout
def log(*args):
    message = ""
    for arg in args:
        message += arg.__str__()+" "
    if sysLogging:
        syslog.syslog(message)
    else:
        print(time.strftime("%b %d %H:%M:%S")+" "+message)
# log the traceback for an exception
def logException(name, ex):
    tracebackLines = traceback.format_exception(None, ex, ex.__traceback__)
    log(name+":")
    for tracebackLine in tracebackLines:
        log(tracebackLine)
# log a debug message conditioned on a specified global variable
def debug(*args):
    if (args[0] in globals()) and globals()[args[0]]:  # only log if the specified debug variable is True
        log(*args[1:])

################################################################################
# Thread and process
################################################################################
# thread object that logs a stack trace if there is an uncaught exception
class LogThread(threading.Thread):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.runTarget = self.run
        self.run = self.logThread
    def logThread(self):
        try:
            self.runTarget()
        except Exception as ex:
            logException("thread "+threading.currentThread().name, ex)
# convenience function to create and start a thread
def startThread(name, target, **kwargs):
    thread = LogThread(name=name, target=target, **kwargs)
    thread.start()
# block a thread indefinitely
def block():
    while True:
        time.sleep(1)
# wait until the network is available
def waitForDns(host):
    wasWaiting = False
    while True:
        try:
            hostAddr = socket.gethostbyname(host)
            if wasWaiting:
                log("DNS is up")
            return
        except:
            log("Waiting for DNS")
            wasWaiting = True
            time.sleep(1)
# execute an external OS command
def osCommand(cmd):
    try:
        executor.execute(cmd)
    except Exception as ex:
        log("osCommand", "Command failed:", str(ex), cmd)

################################################################################
# Manipulation of strings and lists
################################################################################
# transform a string of words into a camel case name
def camelize(words):
    return "".join([words.split()[0].lower()]+[part.capitalize() for part in (words.split()[1:])])
# create a string of words from a camel case name
def labelize(name):
    words = ""
    for char in name:
        if words:
            if words[-1].islower() and (char.isupper() or char.isnumeric()):
                words += " "
        words += char.lower()
    return words.capitalize()
# get the value of a json item from a file
def getValue(fileName, item):
    return json.load(open(fileName))[item]
# turn an item into a list if it is not already
def listize(x):
    return x if isinstance(x, list) else [x]
# truncate or pad a list into a fixed number of items
def fixedList(items, nItems, pad=None):
    return (items+nItems*[pad])[0:nItems]
