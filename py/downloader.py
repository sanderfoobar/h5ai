#!/usr/bin/python
import re,sys,os,urllib2, urllib, gzip

#to-do: add https support
scriptpath = os.path.dirname(os.path.abspath(__file__))

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
