from ast import arg
import sys

from greyt_signer.utils import get_status, entry


def execute():
    try:
        args = sys.argv
        if len(args) <= 1:
            print("Please provide the option that needs to be performed.")
            print("\tgreyt status: To see the status.")
            print("\tgreyt entry: To Sign in / Sign out.")
        else:
            if args[1] == "status":
                get_status()
            if args[1] == "entry":
                entry()
    except KeyboardInterrupt:
        pass
