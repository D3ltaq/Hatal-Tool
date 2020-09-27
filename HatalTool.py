import os
import re
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
functions = 6
waybackList = ""
R = sys.argv[1]
globalExt = "html,htm,js,old,zip,rar,7z,bak,bac,backup,tmp,conf,config,xml,json,class,exe,BAC,BACKUP,BAK,orig,temp,ts,txt"
phpExt = "php,ini,inc,tar.gz,php3,php4.php5,pht,phtm"
javaExt = "Jsp,jspf,jar,war,ear,jsf,do,action,xhtml"
aspExt = "asp,aspx,asmx,dll,cs,csproj,vb,vbproj,axd,ashx,ascx,svc,inc,config,master"
coldfusionExt = "cfm,cfc," + javaExt


def toolRequirements():
    try:
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
        scanTime = (time.strftime("%H:%M-%d.%m.%Y"))  # Get Time-stamp
        outputFile = urlTOtest + "/Nmap-" + urlTOtest + "-" + scanTime + ".txt"  # output file value
        print "[-*-] - Task: Nmap: started on " + urlTOtest
        command = "nmap " + urlTOtest + " -sS -sV -p 80,443 -oN ./" + outputFile
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)  # creating the subprocess with the command
        process.wait()  # wait until the subprocess finishes
        print "[ V ] - Task: Nmap: successfully ended (" + urlTOtest + ") | saving results at --> " + outputFile
    except Exception as e:
        print e


def niktoScan(urlTOtest):
    try:
        scanTime = (time.strftime("%H:%M-%d.%m.%Y"))
        outputFile = urlTOtest + "/Nikto-" + urlTOtest + "-" + scanTime + ".txt"
        print "[-*-] - Task: Nikto: started on " + urlTOtest
        command = "nikto -h " + urlTOtest + " -output " + outputFile
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        print "[ V ] - Task: Nikto: successfully ended (" + urlTOtest + ") | saving results at --> " + outputFile
    except Exception as e:
        print e


def testsslScan(urlTOtest):
    try:
        scanTime = (time.strftime("%H:%M-%d.%m.%Y"))
        outputFile = urlTOtest + "/testssl-" + urlTOtest + "-" + scanTime + ".html"
        print "[-*-] - Task: Testssl: started on " + urlTOtest
        command = "testssl.sh/testssl.sh --htmlfile " + outputFile + " " + urlTOtest
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        print "[ V ] - Task: Testssl: successfully ended (" + urlTOtest + ") | saving results at --> " + outputFile
    except Exception as e:
        print e


def sublist3r(urlTOtest):
    try:
        scanTime = (time.strftime("%H:%M-%d.%m.%Y"))
        outputFile = urlTOtest + "/Sublist3r-" + urlTOtest + "-" + scanTime + ".txt"
        print "[-*-] - Task: Sublist3r: started on " + urlTOtest
        command = "python Sublist3r/sublist3r.py -d " + urlTOtest + " -o " + outputFile
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        results = process.communicate()[0]
        with open(outputFile, 'w') as resultFile:
            resultFile.write(results)
        print "[ V ] - Task: Sublist3r: successfully ended (" + urlTOtest + ") | saving results at --> " + outputFile
    except Exception as e:
        print e


def scyllaLEAKED(urlTOtest):
    pass


def builtwithScan(urlTOtest):
    try:
        scanTime = (time.strftime("%H:%M-%d.%m.%Y"))
        outputFile = urlTOtest + "/BuiltWith-" + urlTOtest + "-" + scanTime + ".txt"
        print "[-*-] - Task: BuiltWith: Started on " + urlTOtest
        results = builtwith.parse("http://" + urlTOtest)
        with open(outputFile, 'wb') as resultFile:
            json.dump(results, resultFile, sort_keys=True, indent=4)
        try:
            i = results['programming-languages']  # get value by key from json object
            i = json.dumps(i)  # convert to string
            i = i.translate(None, ']["')  # remove unwanted char
            return i  # returning programming language
            print "[---] - Task: BuiltWith: Programming-language is probably", programming_lang, "--> running dirsearch.py with the relevent extentions"
        except Exception as e:
            print "[-X-] - Task BuiltWith:", e, "not found in results"
        print "[ V ] - Task: BuiltWith: Successfully ended (" + urlTOtest + ") | saving results at --> " + outputFile
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
        outputFile = urlTOtest + "/waybackmachine-" + urlTOtest + "-" + scanTime + ".txt"
        print "[-*-] - Task: waybackmachine: started on " + urlTOtest
        with_subs = False
        scanResults = waybackurls(urlTOtest, with_subs)
        scanResults = json.dumps(scanResults)
        scanResults = scanResults.translate(None, '[],"')
        scanResults = scanResults.replace('https://', '\nhttps://')
        scanResults = scanResults.replace('http://', '\nhttp://')
        global waybackList
        waybackList = scanResults
        waybackFilterList(urlTOtest)
        if scanResults:
            with open(outputFile, 'wb') as f:
                f.write(scanResults)
            print "[ V ] - Task: Waybackmachine: successfully ended (" + urlTOtest + ") | saving results at --> " + outputFile
        else:
            print("[ V ] - Task: Waybackmachine: successfully ended: Nothing found")
    except Exception as e:
        print e

 
def waybackFilterList(urlTOtest):
    try:
        # open a file
        scanTime = (time.strftime("%H:%M-%d.%m.%Y"))  # Get Time-stamp
        outputFile = urlTOtest + "/Send URLs from wayback to dirsearch-" + "-" + scanTime + ".txt"
        global waybackList
        # step 1: remove unnecessary links
        print type(waybackList)
        waybackList = waybackList.split('\n')
        for line in waybackList:
            if not re.search('original|.txt|.gif|.jpg|.svg|.swf|.jpeg|.css|.svg|.cs|.doc$', line):
                if re.match('http://', line, re.IGNORECASE):
                    line = line.translate(None, 'http://')
                else:
                    line = line.translate(None, 'https://')
                with open(outputFile, 'a') as resultFile:
                    resultFile.write(line + '\n')
        # step 2:  send the new list to dirsearch
        with open(outputFile, 'r') as resultFile:
            for line in resultFile:
                line = line.translate(None, '\n')
                dirsearchScan(line)
    except Exception as e:
        print e
        

def dirsearchScan(urlTOtest):
    try:
        programming_lang = builtwithScan(urlTOtest)  
        scanTime = (time.strftime("%H:%M-%d.%m.%Y"))
        outputFile = urlTOtest + "/Dirseach-" + urlTOtest + "-" + scanTime + ".txt"
        print "[-*-] - Task: Dirsearch: started on " + urlTOtest
        if re.match(r'(?i)php', programming_lang, re.IGNORECASE):
            extentions = globalExt + "," + phpExt
        elif re.match(r'(?i)java', programming_lang, re.IGNORECASE):
            extentions = globalExt + "," + javaExt
        elif re.match(r'(?i)asp.net', programming_lang, re.IGNORECASE):
            extentions = globalExt + aspExt
        elif re.match(r'(?i)coldfusion', programming_lang, re.IGNORECASE):
            extentions = globalExt + coldfusionExt
        else:
            extentions = globalExt
            print "[-*-] - Task: Dirsearch: uses default extention list"
        fuzzList = "dirsearch/db/dicc.txt"
        command = "python3 dirsearch/dirsearch.py -u http://" + urlTOtest + " -e " + extentions + " -F --threads=1 -w " + fuzzList + " --plain-text-report=" + outputFile
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        results = process.communicate()[0]
        print "[ V ] - Task: dirsearch: successfully ended (" + urlTOtest + ") | saving results at --> " + outputFile
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


def URLtoTEST():  # demo.testfire.net  Delta9testapp.io    wordpress.com
    urlTOtest = R  # raw_input("Enter URI for (ex; google.com ):\n ")#Delta9testapp.io
    try:
        os.mkdir(urlTOtest)
    except Exception:
        pass
    return urlTOtest


def goGUYS(urlTOtest):
    # q.append((builtwithScan, urlTOtest)) \\ Running through diesreach function deu to dependency on programming_lang
    q.append((nmapScan, urlTOtest))
    q.append((niktoScan, urlTOtest))
    q.append((testsslScan, urlTOtest))
    q.append((sublist3r, urlTOtest))
    q.append((waybackmachineAPI, urlTOtest))
    q.append((dirsearchScan, urlTOtest))
    q.append(filterList)
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
