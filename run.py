import dspm
import sys

args = sys.argv[1:]

myDSPM = dspm.DSPM()
while myDSPM.running:
    myDSPM.menu(args)
    args=None

print("Goodbye.")
exit()
