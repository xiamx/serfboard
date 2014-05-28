#!/usr/bin/env python
import argparse

def init():
    print "Setting up board for you."


def install():
    pass

actions = {
    'init': init,
    'install': install
}

parser = argparse.ArgumentParser(description='board helps you manage serf plugins')
parser.add_argument('action', choices=actions.keys())

args = parser.parse_args()


if __name__ == '__main__':
    actions[args.action]()
