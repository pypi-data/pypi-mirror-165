"""
Main entrypoint for qwilprobe.
"""

import argparse

import qwilprobe


def main():
    parser = argparse.ArgumentParser(
                        prog="Qwilprobe",
                        description="Probe microservice library for Qwilfish")

    parser.add_argument("-V",
                        "--version",
                        action="store_true",
                        help="print package version")

    args = parser.parse_args()

    if args.version:
        print("qwilprobe " +
              qwilprobe.__version__)
    else:
        parser.print_help()
