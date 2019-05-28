# coding = utf-8

from selenium import webdriver
import time
import os
import subprocess

quicdir = "/home/quic/quicLossExp/quicPLT/PLT0411_nc/"

def writeToFile(path, data):
    with open(path, 'a') as f:
        f.write("%s" %data)

def visitNC(type, times, dt, loss, delay, quicdir=quicdir):

    option = webdriver.ChromeOptions()
    #option.add_argument("--user-data-dir=/tmp/chrome-profile")
    option.add_argument("--no-proxy-server")
    option.add_argument("--enable-quic")
    option.add_argument("--disable-application-cache")
    option.add_argument("--origin-to-force-quic-on=www.example.org:443")
    option.add_argument("--host-resolver-rules=MAP www.example.org:443 yuyj.biz:6121")#default
    option.add_argument("--no-sandbox")            
    option.add_argument("--headless")
    #option.add_argument("--disable-dev-shm-usage")
 
    now = int(time.time())
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S\n", timeArray)

    if dt:
        path = '%s%s_%s_%s_DT.txt' %(quicdir, type, loss, delay)
    else:
        path = '%s%s_%s_%s.txt' %(quicdir, type, loss, delay)
    with open(path,'w') as f:
        f.write("time: "+otherStyleTime)
    
    markTime = ""        
    site = "https://www.example.org/%s.html" %type 
    print "The %s file with site: %s" %(path, site)
    for i in range(times):
        driver = webdriver.Chrome(chrome_options = option)
        #driver.get("https://www.baidu.com")
        time.sleep(.5)

        markTimeTmp = ""
        for j in range(10):
            startTime = time.time()
            #print "The requested site is %s and start at %d..." %(site,startTime)
            driver.get("%s" %site)
            t = int(round((time.time()-startTime)*1000))
            #print "It lasts for %dms!" %t
            markTimeTmp = markTimeTmp + "%s " %t
            time.sleep(.5)

        driver.quit()
        time.sleep(.5)
        #os.system("rm -rf /tmp/chrome-profile/*")
        #os.system("rm -rf /Users/yuyajun/Library/Caches/Google/Chrome/Default/Cache/*")
        
        #print markTimeTmp
        markTime += markTimeTmp+"\n"
    writeToFile(path,markTime)
    print "writing the %s file end!!!!!" %(path)
    time.sleep(.2)

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
    loss = [0, 0.001, 0.05, 0.1, 0.5, 1, 2]
    adapter = "eth0"

    for t in type:
        for l in loss:
            for d in delay:
                clearConfig(adapter)
                time.sleep(.5)
                netConfig(adapter, l, d)
                #configStatus(adapter)
                time.sleep(.5)
            
                visitNC(t, times, hasDT, l, d)
                clearConfig(adapter)
                #configStatus(adapter)
                time.sleep(.5)

    print "End!!!!!!!!!!!!!"
