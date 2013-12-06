from SimpleCV import * 
import IPython

cam = VirtualCamera("data/IMG_0776.MOV","video")
disp = Display()
mv = 0
alpha = .2

def maxValue(self,locations=False):
    if(locations):
        val = np.max(self.getGrayNumpy())
        x,y = np.where(self.getGrayNumpy()==val)
        locs = zip(x.tolist(),y.tolist())
        return int(val),locs
    else:
        val = np.max(self.getGrayNumpy())
        return int(val)

img = cam.getImage()
w = int(.2*img.width)
h = int(.2*img.height)
img = img.scale(w,h)
img.show()
down = False
index = 0
while disp.isNotDone():
    if disp.mouseLeft:
        x = disp.mouseRawX
        y = disp.mouseRawY
        print x,y
        img.save("data/output/img_" + str(index) + ".png")
        with open("data/output/pos_" + str(index) + ".txt","w") as f:
            f.write("WIDTH,HEIGHT: " + str(w) + " " + str(h) + "\n")
            f.write(str(x) + " " + str(y) + "\n")
        index += 1
        img = cam.getImage()
        img = img.scale(w,h)
        img.show()

def get_patches(input_video):
    return [None,1]
