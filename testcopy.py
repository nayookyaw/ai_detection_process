import shutil
import time
import sys

print('Number of arguments: %d arguments' % len(sys.argv))
print('Argument List: %s' % str(sys.argv))

nof = int(sys.argv[1])
wait = int(sys.argv[2])

source = '/home/ubuntu/DSC_0019.jpg'
targetdir = '/home/ubuntu/NAS/Folder_A'

i = 0

def copyfile(i):
	targetpath = "%s/image-%d.jpg" % (targetdir, i)
	print("Copying to %s ..." % targetpath)
	shutil.copy(source, targetpath)
	time.sleep(wait)

while i < nof:
	i += 1
	copyfile(i)
