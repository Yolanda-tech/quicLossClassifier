# coding = utf-8

from selenium import webdriver
import time
import os
import subprocess
from webDriver_c import visitC
from webDriver_nc import visitNC


#sudo ./tcConfig.sh -a eth0 -l 0 -e 200
def netConfig(adapter, loss, delay):
    cmd = "./tcConfig.sh -a %s -l %s -e %s" %(adapter, str(loss), str(delay))
    print cmd
    result = subprocess.call(cmd, shell=True)        
    #print result

#sudo ./tcConfig.sh -a eth0 -c
def clearConfig(adapter):
    cmd = "./tcConfig.sh -a %s -c" %adapter
    result = subprocess.call(cmd, shell=True)        
    #print result

#sudo ./tcConfig.sh -a eth0 -s
def configStatus(adapter):
    cmd = "./tcConfig.sh -a %s -s" %adapter
    result = subprocess.call(cmd, shell=True)        
    #print result

if __name__ == "__main__":
    type = ["small"]#, "thin"]#, "large"]
    hasDT = 0
    times = 20
    delay = [0, 20, 50, 100, 200]#[0, 50, 100, 200, 500]:RTT
    adapter = "eth0"

    for t in type:
        if t == "small":
            loss = [0, 0.001, 0.05, 0.1, 0.5, 1, 2]#[0, 0.5, 1, 1.5, 2, 2.5, 3]
        else:
            loss = [0, 0.001, 0.05,0.1, 0.5, 1,2]
        for l in loss:
            for d in delay:
                clearConfig(adapter)
                time.sleep(.5)
                netConfig(adapter, l, d)
                #configStatus(adapter)
                time.sleep(.5)
            
                visitC(t, times, hasDT, l, d)
                time.sleep(.5)
                visitNC(t, times, hasDT, l, d)

                clearConfig(adapter)
                #configStatus(adapter)
                time.sleep(.5)

    print "End!!!!!!!!!!!!!"
