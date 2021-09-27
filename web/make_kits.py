import sys

from hiddenbeauty.kits import prepare_kits
import config

def make_kits(force):
    print("Create exhibits kits")
    try:
        kits = prepare_kits(force)
    except (IOError, KeyError) as err:
        print("Cannot start server, making exhibit kits failed:", str(err))
        sys.exit(-1)

if __name__ == "__main__":
    force = False
    if len(sys.argv) > 1 and sys.argv[1] == '--force':
        force = True
    make_kits(force)
