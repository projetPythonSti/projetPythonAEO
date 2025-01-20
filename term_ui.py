import blessed
from models.World import *
import os, sys
import sys
import math
import time
import timeit
import colorsys
import contextlib

def scale_255(val): return int(round(val * 255))

@contextlib.contextmanager
def elapsed_timer():
    """Timer pattern, from https://stackoverflow.com/a/30024601."""
    start = timeit.default_timer()

    def elapser():
        return timeit.default_timer() - start

    # pylint: disable=unnecessary-lambda
    yield lambda: elapser()

def status(term, elapsed):
    right_txt = f'fps: {1 / elapsed:2.2f}'
    with term.location(0, term.height - 1):
        return ('\n' + term.normal +
            term.clear_eol  +
            term.rjust(right_txt, term.width))

#
def show_please_wait(term):
    txt_wait = 'please wait ...'
    outp = term.move_yx(term.height - 1, 0) + term.clear_eol + term.center(txt_wait)
    print(outp, end='')
    sys.stdout.flush()


def show_paused(term):
    txt_paused = 'paused'
    outp = term.move_yx(term.height - 1, int(term.width / 2 - len(txt_paused) / 2))
    outp += txt_paused
    print(outp, end='')
    sys.stdout.flush()



def main(term,world):
    with term.cbreak(), term.hidden_cursor(), term.fullscreen():
        pause, dirty = False, True
        t = time.time()
        while True:
            if dirty or not pause:
                if not pause:
                    t = time.time()
                with elapsed_timer() as elapsed:
                    outp = world.return_world()

                outp += status(term, elapsed())
                print(outp, end='')
                sys.stdout.flush()
                dirty = False

            """
            if pause:
                show_paused(term)

            inp = term.inkey(timeout=None if pause else 0.01)
            if inp == '?':
                assert False, "don't panic"
            elif inp == '\x0c':
                dirty = True

            if inp == ' ':
                pause = not pause
            """


if __name__ == "__main__":
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    term = blessed.Terminal()

    with term.location(0, term.height - 1):
        print('Here is the bottom.')

    print('This is back where I came from.')
    """
    mworld = World(10,10)
    exit(main(blessed.Terminal(),mworld))