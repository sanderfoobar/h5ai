#!/usr/bin/python
import re,sys,os, urllib2, urllib, gzip, glob

results = []
recursive = 2 # hoe diep crawlen?

class result(object):
	def __init__(self, host=None, relpath=None, name=None, section=None, imdb=None):
		self.host = host
		self.relpath = relpath
		self.name = name
		self.section = section
		self.imdb = imdb

if len(sys.argv) <= 2:
	print 'No arguments?????\nHierr!11\n'
	sys.exit(0)

search = ' '.join(sys.argv)[len(sys.argv[0])+len(sys.argv[1])+2:]

if len(search) <= 3:
	print 'Te kort'
	sys.exit(0)

gz_files = glob.glob('/home/disk/users/webdav/windows/webdav/search/py/db/*.gz')

f = open('/home/disk/users/webdav/windows/webdav/search/py/conf/sites.txt')
gz_sites = f.readlines()
f.close()

i = 0
for gz_file in gz_files:
	if not "1.gz" in gz_file and sys.argv[1] == "-l": # only search the first host in conf/sites.txt
		continue
	gz = gzip.open(gz_file)
	gz_filename = gz_file.split('/')
	gz_filename = ''.join(gz_filename[len(gz_filename)-1])
	gz_uri = gz_sites[int(gz_filename.replace(".gz",""))]

	for line in gz:
		if line.startswith("d"):
			relpath = " "
			relpath = relpath.join(line.split(relpath)[4:]).replace('\n','')
			search = search.lower()

			if search in relpath.replace('_',' ').replace('-',' ').replace('.',' ').lower() and relpath.count('/') <= recursive:
				dont_show = ['subtitle','sample','subs','screens','insert','proof']
				lame = False
				for dont in dont_show:
					if '/'+dont in relpath.lower():
						lame = True
				if not lame:
					results.append(result(gz_uri.replace('00INDEX.gz','').split(" ")[0],relpath, relpath[relpath.find('/') + 1:],relpath[:relpath.find('/')],''))
	gz.close()
	i += 1

if len(results) <= 0:
	print 'no results :('

print '<?xml version="1.0"?><data><results>'
for result in results:
	print '<result>'
	print '<host>' + result.host + '</host>'
	print '<name>' + result.name + '</name>'
	#print '<imdb>' + result.imdb + '</imdb>'
	print '<section>' + result.section + '</section>'
	print '<url>' + result.host + urllib.quote(result.relpath) + '</url>'
	print '</result>'

print '</results></data>'

sys.exit(1)
