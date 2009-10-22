#!/usr/bin/env python
import sys
from ftplib import FTP

if len(sys.argv) == 1:
    print 'Syntax: ' + sys.argv[0] + ' modulename'
    sys.exit(1)

module = sys.argv[1]
server = 'ftp.drupal.org'
path = '/pub/drupal/files/projects/'

try: ftp = FTP( server )
except:
  print 'Host '+server+' could not be resolved.'
  sys.exit()
else: pass
try: ftp.login()
except:
  print 'Could not log in.'
  sys.exit()
else: pass

ftp.cwd( path )
fdir = ftp.nlst()
print 'Found ' + str(len(fdir)) + ' files!'

l = [f for f in fdir if module  in f]
#print l

if len(l) > 0:
  for i in range(0, len(l)):
    print '[' + str(i) + '] ' + l[i]
else:
  print 'Could not find a module by that name.'
  sys.exit(0)

getid = int(raw_input("Which module do you want to download? "))
print 'Ok, lets get ' + l[getid]
lf = open(l[getid],'wb')
ftp.retrbinary('RETR ' + l[getid],lf.write)
lf.close()

ftp.close()
