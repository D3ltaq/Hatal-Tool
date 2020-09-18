import os
import sys
import time
import json
import Queue
import threading
import subprocess
import requests
import builtwith


q = Queue.deque()
used = []
functions = 5
programming_lang = ""
waybackList = ""
R = sys.argv[1]


def toolRequirements():
    try:
        os.system("sudo apt install python")
        os.system("sudo apt install python-pip")
        os.system("sudo pip install builtwith")
        os.system("sudo pip install requests")
        os.system("sudo pip install six")
        os.system("git clone https://github.com/maurosoria/dirsearch.git")
        os.system("git clone https://github.com/drwetter/testssl.sh.git")
        os.system("git clone https://github.com/aboul3la/Sublist3r.git")
        os.system("sudo pip install -r Sublist3r/requirements.txt")
        print "Tool requirements successfully installed"
        exit()
    except Exception as e:
        print e


def nmapScan(urlTOtest):
    try:
        scanTime = (time.strftime("%H:%M-%d.%m.%Y"))    # Get Time-stamp
        outputFile = "Nmap-" + urlTOtest + "-" + scanTime + ".txt"  # output file value
        print "-*-Task Nmap: started on " + urlTOtest
        command = "nmap " + urlTOtest + " -sS -sV -Pn -oN ./" + outputFile
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)     # creating the subprocess with the command
        process.wait()  # wait until the subprocess finishes
        print "-V-Task Nmap: successfully ended (" + urlTOtest + ") | saving results at --> " + outputFile
    except Exception as e:
        print e


def niktoScan(urlTOtest):
    try:
        scanTime = (time.strftime("%H:%M-%d.%m.%Y"))
        outputFile = "Nikto-" + urlTOtest + "-" + scanTime + ".txt"
        print "-*-Task Nikto: started on " + urlTOtest
        command = "nikto -h " + urlTOtest + " -output " + outputFile
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        print "-V-Task Nikto: successfully ended (" + urlTOtest + ") | saving results at --> " + outputFile
    except Exception as e:
        print e


def testsslScan(urlTOtest):
    try:
        scanTime = (time.strftime("%H:%M-%d.%m.%Y"))
        outputFile = "testssl-" + urlTOtest + "-" + scanTime + ".html"
        print "-*-Task Testssl: started on " + urlTOtest
        command = "testssl.sh/testssl.sh --htmlfile " + outputFile + " " + urlTOtest
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        print "-V-Task Testssl: successfully ended (" + urlTOtest + ") | saving results at --> " + outputFile
    except Exception as e:
        print e


def sublist3r(urlTOtest):
    try:
        scanTime = (time.strftime("%H:%M-%d.%m.%Y"))
        outputFile = "Sublist3r-" + urlTOtest + "-" + scanTime + ".txt"
        print "-*-Task Sublist3r: started on " + urlTOtest
        command = "python Sublist3r/sublist3r.py -d " + urlTOtest + " -o " + outputFile
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        results = process.communicate()[0]
        with open(outputFile, 'w') as resultFile:
            resultFile.write(results)
        print "-V-Task Sublist3r: successfully ended (" + urlTOtest + ") | saving results at --> " + outputFile
    except Exception as e:
        print e

def scyllaLEAKED(urlTOtest):
    pass


def builtwithScan(urlTOtest):
    try:
        scanTime = (time.strftime("%H:%M-%d.%m.%Y"))
        outputFile = "BuiltWith-" + urlTOtest + "-" + scanTime + ".txt"
        print "-*-Task BuiltWith: Started on " + urlTOtest
        results = builtwith.parse("http://" + urlTOtest)
        with open(outputFile, 'wb') as resultFile:
            json.dump(results, resultFile, sort_keys=True, indent=4)
        try:
            i = results['programming-languages']  # get value by key from json object
            i = json.dumps(i)   # convert to string
            i = i.translate(None, ']["')    # remove unwanted char
            programming_lang = i     # setting the global value
            print "---Task BuiltWith: Programming-language is probably", programming_lang, "--> running dirsearch.py with the relevent extentions"
        except Exception as e:
            print "-x-Task BuiltWith:", e, "not found in results"
        print "-V-Task BuiltWith: Successfully ended (" + urlTOtest + ") | saving results at --> " + outputFile
    except Exception as e:
        print e


def waybackurls(host, with_subs):
    if with_subs:
        url = 'http://web.archive.org/cdx/search/cdx?url=*.%s/*&output=json&fl=original&collapse=urlkey' % host
    else:
        url = 'http://web.archive.org/cdx/search/cdx?url=%s/*&output=json&fl=original&collapse=urlkey' % host
    r = requests.get(url)
    results = r.json()
    return results


def waybackmachineAPI(urlTOtest):
    try:
        scanTime = (time.strftime("%H:%M-%d.%m.%Y"))
        outputFile = "waybackmachine-" + urlTOtest + "-" + scanTime + ".txt"
        print "-*-Task: waybackmachine started on " + urlTOtest
        with_subs = False
        scanResults = waybackurls(urlTOtest, with_subs)
        scanResults = json.dumps(scanResults)
        scanResults = scanResults.translate(None, '[],"')
        scanResults = scanResults.replace('https://', '\nhttps://')
        scanResults = scanResults.replace('http://', '\nhttp://')
        waybackList = scanResults
        if scanResults:
            with open(outputFile, 'wb') as f:
                f.write(scanResults)
            print "-V-Task Waybackmachine: successfully ended (" + urlTOtest + ") | saving results at --> " + outputFile
        else:
            print("-V-Task Waybackmachine: successfully ended: Found nothing")
    except Exception as e:
        print e


def dirsearchScan(urlTOtest, extention="PHP"):
    try:
        scanTime = (time.strftime("%H:%M-%d.%m.%Y"))
        outputFile = "dirseach-" + urlTOtest + "-" + scanTime + ".txt"
        print "-*-Task dirsearch: started on " + urlTOtest
        globalExt = "html,htm,js,old,zip,rar,7z,bak,bac,backup,tmp,conf,config,xml,json,class,exe,BAC,BACKUP,BAK,orig,temp,ts,txt"
        phpExt = "php,ini,inc,tar.gz,php3,php4.php5,pht,phtm"
        test = "html,shtnl"
        javaExt = "Jsp,jspf,jar,war,ear,jsf,do,action,xhtml"
        aspExt = "asp,aspx,asmx,dll,cs,csproj,vb,vbproj,axd,ashx,ascx,svc,inc,config,master"
        coldfusionExt = "cfm,cfc," + javaExt
        if extention == "php" or "PHP":
            extentions = globalExt + "," +phpExt
        elif extention == "Java":
            extentions = globalExt + "," + javaExt
        elif extention == "ASP" or "ASP.NET" or "ASP.net":
            extentions = globalExt + aspExt
        elif extention == "ColdFusion":
            extentions = globalExt + coldfusionExt
        else:
            extentions = globalExt
        # TO BE CONTINUED
        fuzzList = "dirsearch/db/testlist.txt"
        command = "python3 dirsearch/dirsearch.py -u https://" + urlTOtest + " -e " + extentions + " --threads=5 -w " + fuzzList + " --plain-text-report=" + outputFile
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        results = process.communicate()[0]
        # print results
        print "-V-Task dirsearch: successfully ended (" + urlTOtest + ") | saving results at --> " + outputFile
    except Exception as e:
        print e


def banner():
    print """

                 _        _ _____            _ 
      /\  /\__ _| |_ __ _| /__   \___   ___ | |
     / /_/ / _` | __/ _` | | / /\/ _ \ / _ \| |
    / __  / (_| | || (_| | |/ / | (_) | (_) | |
    \/ /_/ \__,_|\__\__,_|_|\/   \___/ \___/|_|
                                           
    The following.. bla bla bla... is a bla bla bla
                       """


def URLtoTEST():    # demo.testfire.net  Delta9testapp.io    wordpress.com
    urlTOtest = R # raw_input("Enter URI for (ex; google.com ):\n ")#Delta9testapp.io
    return urlTOtest


def goGUYS(urlTOtest):
    # q.append((nmapScan, urlTOtest))
    # q.append((niktoScan, urlTOtest))
    # q.append((testsslScan, urlTOtest))
    # q.append((sublist3r, urlTOtest))
    # q.append((builtwithScan, urlTOtest))
    # q.append((waybackmachineAPI, urlTOtest))
    # q.append((dirsearchScan, urlTOtest))
    pass


def worker():
    for task in q:
        if task not in used:
            used.append(task)
            return task[0](task[1])
        else:
            pass


def main():
    banner()
    if R == "--install":
        toolRequirements()
    urlTOtest = URLtoTEST()
    goGUYS(urlTOtest)
    threads = functions
    for i in range(threads):
        t = threading.Thread(target=worker)
        t.start()


main()
