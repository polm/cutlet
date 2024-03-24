from cutlet import Cutlet
import fileinput
import sys

if sys.platform != "win32":
    # Don't print an error on SIGPIPE
    from signal import signal, SIGPIPE, SIG_DFL

    signal(SIGPIPE, SIG_DFL)


def main():
    system = sys.argv[1] if len(sys.argv) > 1 else "hepburn"

    katsu = Cutlet(system)

    try:
        for line in fileinput.input([]):
            print(katsu.romaji(line.strip()))
    except KeyboardInterrupt:
        sys.exit(0)
