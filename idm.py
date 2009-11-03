#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Install Drupal Module (idm)
# Author : Jonas Björk, jonas@jonasbjork.net
# Date   : 2009-10-22
# License: EUPL v1.1 (http://ec.europa.eu/idabc/eupl) #
# Modified by Marcus Follrud 2009-10-23:
# Added Filtering options for different drupal versions plus developer packages
# Also added a better help :) 

import sys,re,string
#from sys import argv
from optparse import OptionParser #For parsing command line arguments.
from ftplib import FTP

try:
  import sqlite3 as sqlite
  has_sql = True
except ImportError:
  has_sql = False
  print "Could not find SQLite"

# function to print usage of this command
def usage():
  print "Usage: " + sys.argv[0] + " <commands> [module]"

# TODO: This optionparser makes usage-information inconsistent
optParser = OptionParser()
optParser.set_defaults(drupalfilter="all")
optParser.set_defaults(verbose=True)
optParser.add_option("-f","--filter", action="store", type="string", dest="drupalfilter",
                     help="Filter the results in version numbers.", metavar="version")

optParser.add_option("-d", "--dev", action="store_true", dest="devpackages", help="Show developer packages", default=False)

optParser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="Verbose mode", default=False)

optParser.add_option("-q", "--quiet", action="store_false", dest="verbose", help="Turn off output", default=True)

(options, args) = optParser.parse_args()

#drupal filter is in options.drupalfilter

if len(args) < 1:
  usage()
  sys.exit(0)

# SQLite stuff
# initialize the database
if has_sql:
  conn = sqlite.connect("idm.db")
  cur = conn.cursor()
  conn.execute("CREATE TABLE IF NOT EXISTS info(last_seen int)")
  #TODO: create the table with fileinfo

# TODO: This should be fixed! We cant rely on a single server, mirrors maybe? :)
module = args[0]
server = 'ftp.drupal.org'
path = '/pub/drupal/files/projects/'

try: ftp = FTP( server )
except:
  print 'Error: Host '+server+' could not be resolved.'
  sys.exit()
else: pass
try: ftp.login()
except:
  print 'Error: Could not log in.'
  sys.exit()
else: pass

ftp.cwd( path )
fdir = ftp.nlst()
if options.verbose:
  print 'Found a total of ' + str(len(fdir)) + ' files!'

# TODO pupulate the db-table

l = [f for f in fdir if module in f]
l2 = [] #This is the filtered list.
for i in range(0, len(l)):
  #This is where we write out the files found.
  #Also. This is where we do the filtering. 6.x, 5.x, 4.x and dev (for now..)
  if options.drupalfilter == "all":
    l2.append(l[i])
  else:
  #Parse after the version entered.
    if string.find(l[i],options.drupalfilter+".x",0,len(l[i])) > 0:
    #We got a match for the filter.
      if options.devpackages == True:
        if string.find(l[i],"-dev",0,len(l[i])) > 0:
          l2.append(l[i])
      else:
         if string.find(l[i],"-dev",0,len(l[i])) < 0:
           l2.append(l[i])

if (len(l2) > 0): #We got a result
  if options.verbose:
    print "Files containing \""+module+"\""
    print " Based on filter: "+options.drupalfilter
    if options.devpackages == True:
      print "  Showing developer packages"
    else:
      print "  Not showing developer packages"
  for i in range(0,len(l2)):
    print '[' + str(i) + '] '+ l2[i]
else:
  print 'Error: Could not find a module by that name.'
  sys.exit(0)

getids = raw_input("Which module do you want to download? (Separate with comma for more than one)")

id_array = getids.split(",")

for x in id_array:
  if options.verbose:
    print "Downloading: "+l[int(x)]
  lf = open(l[int(x)],'wb')
  ftp.retrbinary('RETR ' + l[int(x)],lf.write)
  lf.close
  
ftp.close()
if options.verbose:
  print "Download complete. Closing…"
