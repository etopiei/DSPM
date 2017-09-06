import dspm
import sys

args = sys.argv[1:]
if len(args) < 1:
    args = None 

myDSPM = dspm.DSPM()
print("Welcome to DSPM - Dead Simple Password Manager")
while myDSPM.running:
    myDSPM.menu(args)
    args=None

print("Goodbye.")
exit()
