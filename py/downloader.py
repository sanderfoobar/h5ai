#!/usr/bin/python
import re,sys,os,urllib2, urllib, gzip, glob
import ConfigParser
import functions

scriptpath = os.path.dirname(os.path.abspath(__file__))

config = ConfigParser.ConfigParser()
config.read('%s/config.cfg'%(scriptpath))

def fetch(uri,dest):
    try:
        if len(uri.split(" ")) == 3:
            spluri = uri.split(" ")
            auth_handler = urllib2.HTTPBasicAuthHandler()
            auth_handler.add_password(realm=spluri[1], 
                uri=spluri[0], 
                user=spluri[2].split(":")[0], 
                passwd=spluri[2].split(":")[1])
            opener = urllib2.build_opener(auth_handler)
            urllib2.install_opener(opener)    
        print 'opening:'+uri        
        dfile = urllib2.urlopen(uri)
        output = open(dest,'wb')
        output.write(dfile.read())
        output.close()
    except Exception,ex:
        print ex
        return

f = open(scriptpath+'/conf/sites.txt',"r")
m = f.readlines()
f.close()

i = 0
for site in m:
    if not site.startswith("#"):
        print site
        site = site.replace("\n","")
        fetch(site,scriptpath+'/db/'+str(i)+'.gz')
    i+=1

if config.get('Database', 'enabled') == "1":
    import pymongo
    try:
        connection = pymongo.Connection(config.get('Database', 'host'))
        database = connection[config.get('Database','name')]
    except:
        print('Error: Unable to connect to database.')
        connection = None
    if connection is None:
        print('Some error is here')

    gz_files = glob.glob('%s/db/*.gz'%(scriptpath))
    f = open('%s/conf/sites.txt'%(scriptpath))
    gz_sites = f.readlines()
    f.close()

    i = 0
    for gz_file in gz_files:
        gz = gzip.open(gz_file)
        gz_filename = gz_file.split('/')
        gz_filename = ''.join(gz_filename[len(gz_filename)-1])
        gz_uri = gz_sites[int(gz_filename.replace(".gz",""))]

        for line in gz:
            if line.startswith("f") or line.startswith("d"):
                relpath = " "
                relpath = relpath.join(line.split(relpath)[4:]).rstrip('\n\r')
                timestamp = int(line.split(" ")[1].split(".")[0])
                dont_show = ['subtitle','sample','subs','screens','insert','proof']
                insertdata = {
                    'type':line.split(" ")[0],
                    'host':gz_uri.replace('00INDEX.gz','').split(" ")[0],
                    'path':urllib.quote_plus(relpath),
                    'name':urllib.quote_plus(relpath[relpath.find('/') + 1:]),
                    'section':relpath[:relpath.find('/')],
                    'imdb':'',
                    'timestamp':timestamp,
                    'sourcefile':gz_filename}
                try:
                    database.temp_search.insert(insertdata)
                except:
                    print(insertdata)
        gz.close()
        i += 1 
    database.drop_collection('search')
    database.temp_search.rename('search',dropTarget=True)

