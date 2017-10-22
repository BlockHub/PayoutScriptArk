import pickle
import sys

# Need file arguments
if len(sys.argv) < 2:
    sys.stdout.write("""
Usage: python payoutdisplayer.py FILE(s)
Shows the contents of the payout files.

""")
    sys.exit(1)

for f in sys.argv[1:]:
    with open(f, 'rb') as inf:
        print(f, ':', pickle.load(inf))
        
