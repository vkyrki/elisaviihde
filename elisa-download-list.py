import getopt, sys, getpass, elisaviihde, os, re
from subprocess import call

def main():
  # Parse command line args
  if len(sys.argv[1:]) < 4:
    print "ERROR: Usage:", sys.argv[0], "[-u username -l listfile]" 
    sys.exit(2)
  try:
    opts, args = getopt.getopt(sys.argv[1:], "u:l:", ["username"])
  except getopt.GetoptError as err:
    print "ERROR:", str(err)
    sys.exit(2) 
  
  # Init args
  username = ""
  listfile = None
  verbose = False
  
  # Read arg data
  for o, a in opts:
    if o == "-l":
      listfile = a
    elif o in ("-u", "--username"):
      username = a
    else:
      assert False, "unhandled option"

  if username=="" or not listfile:
    print "ERROR: username or programId missing"
    sys.exit(2)

  try:
    input = open(listfile,"r")
  except Exception as err:
    print "ERROR: Opening listfile failed, " + err
      
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

  for text in input:  

    match = re.match('^(\d+)\: (.+)',text)
  
    if match:
      print match.group(1) + " " + match.group(2)

    programId = match.group(1)
    outfilename = match.group(2)
    
    streamuri = elisa.getstreamuri(programId)

    print "Found stream uri from recording " + str(programId) + ":"
    print streamuri
  
    callstr = 'ffmpeg -i "' + streamuri + '" -c:v libx264 -preset medium -crf 20 -c:a copy -sn "' + outfilename + '.mkv"'

    print callstr

    # call(callstr, shell=True)
  
  # Close session
  elisa.close()

if __name__ == "__main__":
  main()

