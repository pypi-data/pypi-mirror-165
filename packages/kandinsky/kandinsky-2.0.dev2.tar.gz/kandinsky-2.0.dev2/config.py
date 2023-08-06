from os import listdir
from genericpath import isdir

def find_all(path='', exclude=["__pycache__", "publish.bat"]):
    found = []
    for i in listdir(None if path == '' else path):
      if i not in exclude:
        if isdir(path+i): found.extend(find_all(path+i+'/'))
        else: found.append(path+i) 
    return found

with open("src/kandinsky.egg-info/SOURCES.txt", "wt") as f: 
  for i in find_all(): f.write(i+'\n')