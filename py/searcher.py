#!/usr/bin/python
import re,sys,os, urllib2, urllib, gzip, glob, json
import ConfigParser
import argparse
import functions
import time

parser = argparse.ArgumentParser(description="Search the directory of shares")
group = parser.add_mutually_exclusive_group()
group.add_argument("-l", "--local", help="Search local", action='store_true')
group.add_argument("-a", "--all", help="Search global", action='store_true')
parser.add_argument("-f", "--file", help="Search files", action='store_true')
parser.add_argument("-j", "--json", help="Output data in json format", action='store_true')
parser.add_argument("-t", "--timestamp", help="Search from this timestamp", action='store_true')
parser.add_argument("key", type=str, help="Keyword or Timestamp")

args = parser.parse_args()

scriptpath = os.path.dirname(os.path.abspath(__file__))

config = ConfigParser.ConfigParser()
config.read('%s/config.cfg'%(scriptpath))

results = []
recursive = config.get('General', 'recursive') 

class result(object):
    def __init__(self, host=None, relpath=None, name=None, section=None, imdb=None, modified = None):
        self.host = host.rstrip("\r\n")
        self.relpath = relpath.rstrip("\r\n")
        self.name = name
        self.section = section
        self.imdb = imdb
        self.modified = modified

search = args.key 

if len(search) <= 3:
    print 'Te kort'
    sys.exit(0)

gz_files = glob.glob('%s/db/*.gz'%(scriptpath))

f = open('%s/conf/sites.txt'%(scriptpath))
gz_sites = f.readlines()
f.close()

i = 0
for gz_file in gz_files:
    if not "1.gz" in gz_file and args.local: # only search the first host in conf/sites.txt
        continue
    gz = gzip.open(gz_file)
    gz_filename = gz_file.split('/')
    gz_filename = ''.join(gz_filename[len(gz_filename)-1])
    gz_uri = gz_sites[int(gz_filename.replace(".gz",""))]

    for line in gz:
        if (line.startswith("f") and args.file) or (line.startswith("d") and not args.file):
            relpath = " "
            relpath = relpath.join(line.split(relpath)[4:]).rstrip('\n\r')
            search = search.lower()
            timestamp = int(line.split(" ")[1].split(".")[0])

            if (not args.timestamp and (search in relpath.replace('_',' ').replace('-',' ').replace('.',' ').lower() and relpath.count('/') <= recursive)) or (args.timestamp and timestamp > int(search)):
                dont_show = ['subtitle','sample','subs','screens','insert','proof']
                lame = False
                for dont in dont_show:
                    if '/'+dont in relpath.lower():
                        lame = True
                if not lame:
                    results.append(result(gz_uri.replace('00INDEX.gz','').split(" ")[0],relpath, relpath[relpath.find('/') + 1:],relpath[:relpath.find('/')],'',timestamp))
    gz.close()
    i += 1

if len(results) <= 0:
    print 'no results :('

data = []

for result in results:
    data.append({"host":result.host,"name":result.name,"section":result.section,"url":result.host + urllib.quote(result.relpath),"modified":result.modified,"modified_nice":time.ctime(int(result.modified))})

if len(data) > 1 and args.json:
    print json.dumps(data)

if len(data) > 1 and not args.json:
    titles = [('name',"Name"),('section',"Section"),('url',"URL"),('modified_nice',"Date modified")]
    functions.table_print(data, titles)

sys.exit(1)
