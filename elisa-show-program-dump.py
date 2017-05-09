import re, sys
import cPickle as pickle

def main():
  with open("recording_data.pkl", "rb") as input:
    allrecordings = pickle.load(input)

  totaltime = 0
  for rec in allrecordings:
    totaltime += rec["duration"]
    try:
      kausi = None
      if "Kausi" in rec["description"] or "kausi" in rec["description"]:
        m = re.search("[Kk]ausi ?([0-9]+)", rec["description"])
        if m:
          kausi = m.group(1)
        else:
          m = re.search("([0-9]+)\. ?[kK]ausi", rec["description"])
          if m:
            kausi = m.group(1)
          else:
            m = re.search("([0-9]+)\. ?[tT]uotantokausi", rec["description"])
            if m:
              kausi = m.group(1)

#      if "kauden" in rec["description"]: print rec["description"]
#      if "Kauden" in rec["description"]: print rec["description"]
              
      jakso = None
      if "/" in rec["description"]:
        m = re.search("([0-9]+) ?/([0-9]+)", rec["description"])
        if m:
          if m.group(2)>2:
            jakso = m.group(1)
#          else:
#            print "J " + jakso + " / " + m.group(2)
      if "osa" in rec["description"]:
        m = re.search("osa ([0-9]+)", rec["description"])
        if m:
            jakso = m.group(1)

#      if kausi and not jakso: print rec["description"]
      pv = None
      m = re.search("(\d+)\.(\d+)\.(\d+)", rec["startTime"])
      if m:
          pv = m.group(1)
          kk = m.group(2)
          vvvv = m.group(3)

      filename = rec["name"]
      if kausi and jakso: filename += "_K" + kausi + "J" + jakso.zfill(2)
      if not kausi and jakso: filename += "_J" + jakso.zfill(2) 
      if pv: filename += "_" + vvvv + kk + pv

      filename = re.sub(' ','_',filename)
      filename = re.sub('_+','_',filename)
      
      print filename
    except KeyError:
      continue
    
  print "Total duration " + str(totaltime) + " sec (" + str(totaltime/60) + " min = " + str(totaltime/3600) + " hr)"

if __name__ == "__main__":
  main()
