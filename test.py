
import os
import glob

print ("test func")
cwd = os.getcwd()
print (cwd)
path = cwd+'/files/newShortVideos'
print (path)
videoIndex = 0
videoNum_to_path = {}
for filename in glob.glob(os.path.join(path, '*detailed.txt')):
    videoIndex += 1
    print ("**proccecing:  %s**" % filename)

    video_path=filename[(filename.index("newShortVideos")+15):filename.index("_")] + ".mp4"
    print ("exact filename: %s" %video_path)
    full_video_path= cwd+'/files/Videos/'+video_path
    videoNum_to_path[videoIndex]=full_video_path
    #print ("going to print file context:")
    #print ("printing csv data of video[%0d]" % videoIndex)


for vid in videoNum_to_path:
    print ("%0d:\t%s " % (vid,videoNum_to_path.get(vid)))







