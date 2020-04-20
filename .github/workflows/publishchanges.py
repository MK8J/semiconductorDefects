#!/usr/bin/python

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--changes', help='a list of changes')


args = parser.parse_args()


changeslist = args.changes.splitlines()

additions = list(filter(lambda chg: chg.startswith("A"), changeslist))
additions = list(map(lambda chg: chg.split()[-1], additions))

modifications = list(filter(lambda chg: chg.startswith("M"), changeslist))
modifications = list(map(lambda chg: chg.split()[-1], additions))

for change in additions:
    print (change)