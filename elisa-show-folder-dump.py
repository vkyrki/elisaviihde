import re, sys
import cPickle as pickle

def main():

  with open("folder_data.pkl", "rb") as input:
    allfolders = pickle.load(input)

  for folder in allfolders:
    print str(folder["id"]) + ": " + folder["name"]

if __name__ == "__main__":
  main()
