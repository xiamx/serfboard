#!/usr/bin/env python
import argparse
import os
import sys
import errno
import shutil
import subprocess
import yaml


confd = os.path.join(os.getcwd(), "serf.conf.d")
handlersd = os.path.join(os.getcwd(), 'handlers')


def init(args):
    print "Setting up board for you."

    # first make serf config dir

    if os.path.exists(confd):
        print "Looks like you already run board init on. Nothing to do."
        sys.exit(errno.EEXIST)

    os.mkdir(confd)
    os.mkdir(handlersd)

    templatesd = os.path.join(os.path.dirname(__file__), 'templates')
    shutil.copy(os.path.join(templatesd, 'board.json'), confd)
    shutil.copy(os.path.join(templatesd, 'handle.py'), confd)
    os.chmod(os.path.join(templatesd, 'handle.py'), 0o744)

    print ("Done! You can start serf with -config-dir set to "
           "serf.conf.d that this script just created for you")


def do_github_install(name):
    github_prefix = "https://github.com/"
    github_suffix = ".git"
    repo = github_prefix + name + github_suffix
    localdir = os.path.join(handlersd, name.replace('/', '-'))
    ret = subprocess.call(["git", "clone", repo, localdir])

    if ret == 0:
        print "Installed", name
        with open(os.path.join(localdir, 'manifest.yaml'), 'r') as f:
            mani = yaml.load(f)
            try:
                for plugin, version in mani['dependencies'].iteritems():
                    install(plugin)
            except KeyError:
                pass


def install(args):
    if isinstance(args, basestring):
        print "Installing", args
        do_github_install(args)
    else:
        print "Installing", args.plugin
        do_github_install(args.plugin)

actions = {
    "init": init,
    "install": install
}

parser = argparse.ArgumentParser(
    description='board helps you manage serf plugins')
subparsers = parser.add_subparsers(help='sub-command help')

parser_init = subparsers.add_parser('init', help='init help')
parser_init.set_defaults(func=init)
parser_install = subparsers.add_parser('install', help='init help')
parser_install.add_argument('plugin')
parser_install.set_defaults(func=install)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
