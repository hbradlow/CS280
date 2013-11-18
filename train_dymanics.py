import numpy as np
import os
import re
import pickle

files = os.listdir("data/output")
files = [a for a in files if "txt" in a]
files = sorted(files,key = lambda x: int(re.match(".*_(\d+)\..*",x).group(1)))

raw_data = []
for filename in files:
    with open("data/output/" + filename) as f:
        w,h = f.readline().split(" ")[1:3]
        x,y = f.readline().split(" ")
        raw_data.append((float(x)/float(w),float(y)/float(h)))

data = np.array(raw_data)
with open("data1.pickle","w") as f:
    pickle.dump(data,f)
