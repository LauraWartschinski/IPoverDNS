#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess as sub
import time

p = sub.Popen(('sudo', 'tcpdump', '-l', 'port 53'), stdout=sub.PIPE)

start_time = time.time()
elapsed_time = start_time
nullcounter = 0
nullcountertime_start = time.time()
warnedNLL = False
warnedFQN = False

suspiciousness = 0
susptime_start = time.time()

amounttime_start = time.time()

fqnlength = 0
fqncounter = 0
fqnnumberdiff = 0

dnstotal = 0
total_len = 0

for row in iter(p.stdout.readline, b''):
    r = row.rstrip()   # process here
#    print r
    elapsed_time = time.time() - start_time
    susptime = time.time()

    dnstotal = dnstotal +1
    total_len = total_len + len(r)
    
    
    #Looking for suspicious domain names
    fqn = r[:r.find(". ")+2]
    fqn = fqn[:fqn.find(" (")]
    while fqn.find(" ") != -1:
      fqn = fqn[fqn.find(" ")+1:]
      
    if len(fqn) > 5:
      fqncounter = fqncounter +1
      fqnlength = fqnlength + len(fqn)
      fqnnumberdiff = fqnnumberdiff + len(set(fqn))
      #print fqn
    #  print suspiciousness
      
      if len(set(fqn)) > 40:
        suspiciousness = suspiciousness+1
        susptime = time.time()
        #print fqn
      
      if len(set(fqn)) > 70:
        suspiciousness = suspiciousness+1          
        susptime = time.time()
        #print fqn
        
      if len(fqn) > 300:
          suspiciousness = suspiciousness+1          
          susptime = time.time()
        #  print fqn
        
      if suspiciousness > 20 and warnedFQN == False:
          print "WARNING: suspicious looking FQNs."
          warnedFQN = True
      
      if susptime - susptime_start > 20:
          suspiciousness = 0
          susptime_start = time.time()
          warnedFQN = False
        #  print "Resolved fqns: " + str(fqncounter)
        #  print "Average amount of different characters: " + str(fqnnumberdiff / fqncounter)
        #  print "Average length: " + str(fqnlength / fqncounter)
          
          fqncounter = 0
          fqnnumberdiff = 0
          fqnlength = 0

    
    #Looking for NULL DNS types
    if "NULL" in r:
      nullcounter = nullcounter +1
      nullcountertime = time.time()
  
      if nullcounter > 500 and warnedNLL != True:
        print "WARNING: many NULL DNS requests. " 
        warnedNLL = True

      if nullcountertime-nullcountertime_start > 30:
 #         print "nullcounter: " + str(nullcounter)
          nullcounter = 0
          nullcountertime_start = time.time()
          warnedNLL = False
      

    
    #counting the amount and length of dns querys
    if time.time() - amounttime_start < 30:
      continue
    else:
      #print "dnstotal: " + str(dnstotal)
      #print "average length: " + str((total_len * 1.0)/dnstotal)

      if dnstotal > 1500:
        print "WARNING: high output of DNS messages."
      
      if (total_len * 1.0) / dnstotal > 190:
        print "WARNING: very long DNS messages are sent."
      
      dnstotal = 0
      total_len = 0
      amounttime_start = time.time()
    
    
    