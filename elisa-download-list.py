import getopt, sys, getpass, elisaviihde, os, re
import cPickle as pickle
from subprocess import call
from time import sleep

class Downloader(object):
  def __init__(self, command, outfilename)
    self.command = command
    self.process = None
    self.outfilename = outfilename

  def run(self):
    def download_thread(command):
      process = subprocess.Popen(self.command, shell=True)
      process.communicate()

    thread = threading.Thread(target=download_thread)
    try: 
      thread.start()

      oldsize = 0
      while True:
        thread.join(60)

        if not thread.is_alive():
          returncode = self.process.returncode
          if returncode:
            print "WARNING: Possible ffmpeg failure, returncode " + str(returncode)
          break

        newsize = os.path.getsize(self.outfilename)
        if oldsize == newsize:
          print "ERROR: File size not growing, download seems to be stalled, aborting"
          self.proccess.terminate()
          thread.join()
          break
    except KeyboardInterrupt as exp:
      print "Interrupted from keyboard, exiting"
      self.process.terminate()
      thread.join()
      os.remove(outfilename.decode("utf8")+".mkv")
      exit(0)

def login(elisa, username, password):
  for i in range(10):
    try:
      elisa.login(username, password)
      break
    except Exception as exp:
      print "WARNING: Login failed, retrying after one minute"
      sleep(60)
  else:
    print "ERROR: Login failed 10 times in row, exiting"
    sys.exit(1)

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

  datadir = "/home/vkyrki/git/elisaviihde/"
  
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

  with open(datadir + "recording_data.pkl", "rb") as input_data:
    allrecordings = pickle.load(input_data)
   
  # Ask password securely on command line
  password = getpass.getpass('Password: ')
    
  # Init elisa session
  try:
    elisa = elisaviihde.elisaviihde(verbose)
  except Exception as exp:
    print "ERROR: Could not create elisa session"
    sys.exit(1)
    
  for text in input:  

    # Login
    login(elisa, username, password)

    match = re.match('^(\d+)\: (.+)',text)
  
    if not match:
      continue;

    if verbose: print match.group(1) + " " + match.group(2)

    programId = match.group(1)
    outfilename = match.group(2)

    try:
      prog = next(x for x in allrecordings if x["programId"]==int(programId))
    except StopIteration as exp:
      print str(programId) + ": " + outfilename + " not found in database"
      continue

    print "Processing " + programId + ", " + prog["name"]
    deinterlace = "" # "-vf yadif=0 "
    subtitles = ""

    if re.match('Yle', prog["channel"]):
      subtitles = '-filter_complex "[0:v][0:s]overlay" '
      print "From YLE channel " + prog["channel"] + ", overlaying subtitles"
      
    try:
      streamuri = elisa.getstreamuri(programId)
    except Exception as exp:
      print "WARNING: Stream not found, skipping"
      continue

    # input stream and codec options
    callstr = 'ffmpeg -i "' + streamuri + '" ' + subtitles + '-c:v libx264 -preset medium -crf 22 -c:a aac -strict experimental -sn -loglevel fatal '
    # possible deinterlace plus description metadata
    callstr = callstr + deinterlace + '-metadata description="' + prog["description"] + '" '
    # title metadata    
    callstr = callstr + '-metadata title="' + outfilename.decode("utf8") + '" '
    # output filename (&type/Matroska)
    callstr = callstr + '"' + outfilename.decode("utf8") + '.mkv"'

    #print callstr
    print "Starting encoding"
    downloader = Downloader(callstr, outfilename.decode("utf8") + ".mkv")
    downloader.run()
      
    # Close session (new one opened for each file)
    try:
      elisa.close()
    except Exception as exp:
      print "Closing connection failed. Will continue anyway."
      continue
    
    # All files downloaded

if __name__ == "__main__":
  main()

