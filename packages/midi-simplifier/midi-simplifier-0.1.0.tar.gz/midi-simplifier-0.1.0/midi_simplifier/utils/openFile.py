import subprocess
import os
import sys


class FileOpener:
    def __init__(self):
        pass

    def open(self, filepath):
        try:
            os.startfile(filepath)
        except AttributeError:
            subprocess.call(['open', filepath])


def fileExists(directory):
    return os.path.isfile(directory)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        _, file = sys.argv
        if fileExists(file):
            FileOpener().open(file)
