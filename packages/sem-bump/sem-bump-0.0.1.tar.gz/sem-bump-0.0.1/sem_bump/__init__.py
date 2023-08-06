#!/usr/bin/env python

from semantic_version import Version
from argparse import ArgumentParser
from select import select
from sys import stdin, stdout


def main():
  parser = ArgumentParser()
  parser.add_argument("component", type=str, choices=[
                      "major", "minor", "patch"], help="Component of the version to bump")
  parser.add_argument("-v", "--version", type=str,
                      help="Version string to bump", default=None)
  parser.add_argument("-f", "--version-file", type=str,
                      help="Read from and/or write to --version-file", default=None)
  parser.add_argument("-i", "--increment", type=int,
                      help="The amount to increment by", default=1)

  args = parser.parse_args()

  if select([stdin, ], [], [], 0.0)[0]:
    version_str = stdin.read()
  elif args.version:
    version_str = args.version
  elif args.version_file:
    try:
      with open(args.version_file, "r") as f:
        version_str = f.read()
    except Exception as e:
      print(f"Could not read {args.version_file}: {e}")
      exit(1)
  else:
    print("Must supply one of --version-file, or --version")
    parser.print_help()
    exit(1)

  try:
    version = Version(version_str)
  except Exception as e:
    print(f"Invalid version string {version_str}")
    exit(1)

  def bump_version(version, component):
    updaters = {
        "major": version.next_major,
        "minor": version.next_minor,
        "patch": version.next_patch
    }
    return updaters[component]()

  for _ in range(args.increment):
    version = bump_version(version, args.component)

  if args.version_file:
    try:
      with open(args.version_file, "w") as f:
        f.write(str(version))
    except Exception as e:
      print(f"Could not write to file {args.version_file}: {e}")
      exit(1)
  else:
    print(str(version), file=stdout)

if __name__ == "__main__":
  main()