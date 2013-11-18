import numpy as np
import os
import re
import pickle

import Tkinter as tk

import dynamics

p = 100
d = 2

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

windowed_data = np.empty((len(raw_data)-p,p+1,d))

from gui import Visualizer, Point2D, Line2D

root = tk.Tk()
vis = Visualizer(root,400,400)


for i in range(data.shape[0]-p):
    window = data[i:i+p+1]
    windowed_data[i,:,:] = window

model = dynamics.ARModel(p,d)
model.fit(windowed_data)

point = np.array([.5,.5])
test_data = np.empty((p,2))
for i in range(p):
    test_data[i] = point
    point += np.array([0,.02]) 
for i in range(p):
    vis.add_drawable(Point2D(400*test_data[i],fill="red"))
prev = None
for i in range(30):
    point = model.predict(test_data) + np.random.multivariate_normal(np.array([0,0]),model.cov*np.eye(2))
    vis.add_drawable(Point2D(400*point,fill="blue"))
    test_data[0:p-1] = test_data[1:p]
    test_data[p-1] = point  
    if prev is not None:
        vis.add_drawable(Line2D(prev,400*point))
    prev = 400*point

vis.run()
root.mainloop()
