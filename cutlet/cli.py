from cutlet import Cutlet
import fileinput
import sys

# Don't print an error on SIGPIPE
from signal import signal, SIGPIPE, SIG_DFL

def main():
    signal(SIGPIPE, SIG_DFL) 
    system = sys.argv[1] if len(sys.argv) > 1 else 'hepburn'

    katsu = Cutlet(system)

    try:
        for line in fileinput.input([]):
            print(katsu.romaji(line.strip()))
    except KeyboardInterrupt:
        sys.exit(0)
