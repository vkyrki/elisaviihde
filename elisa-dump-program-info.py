# Elisa Viihde API Python implementation usage demo

import getopt, sys, getpass, elisaviihde, os, re
import cPickle as pickle

from subprocess import call

def main():
  # Parse command line args
  if len(sys.argv[1:]) < 2:
    print "ERROR: Usage:", sys.argv[0], "[-u username]" 
    sys.exit(2)
  try:
    opts, args = getopt.getopt(sys.argv[1:], "u:v", ["username"])
  except getopt.GetoptError as err:
    print "ERROR:", str(err)
    sys.exit(2) 
  
  # Init args
  username = ""
  verbose = False
  
  # Read arg data
  for o, a in opts:
    if o == "-v":
      verbose = True
    elif o in ("-u", "--username"):
      username = a
    else:
      assert False, "unhandled option"
  
  # Ask password securely on command line
  password = getpass.getpass('Password: ')
  
  # Init elisa session
  try:
    elisa = elisaviihde.elisaviihde(verbose)
  except Exception as exp:
    print "ERROR: Could not create elisa session"
    sys.exit(1)
    
  # Login
  try:
    elisa.login(username, password)
  except Exception as exp:
    print "ERROR: Login failed, check username and password"
    sys.exit(1)
    
  allfolders = elisa.getallfolders()
  
  if verbose:
    for folder in allfolders: print folder["name"]
    
  allrecordings = elisa.getallrecordings()
  print str(len(allrecordings)) + " recordings total."

  with open("recording_data.pkl", "wb") as output:
    pickle.dump(allrecordings, output, pickle.HIGHEST_PROTOCOL)
    
  elisa.close()

if __name__ == "__main__":
  main()

