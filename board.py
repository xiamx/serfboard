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


def do_github_install(name, version):
    if version != "":
        github_branch_args = ["-b", "rel-" + str(version)]
    else:
        github_branch_args = ""
    github_prefix = "https://github.com/"
    github_suffix = ".git"
    repo = github_prefix + name + github_suffix
    localdir = os.path.join(handlersd, name.replace('/', '-'))
    localmanifest = os.path.join(localdir, 'manifest.yaml')
    github_clone_args = github_branch_args + [repo, localdir]

    with open(os.devnull, 'w') as FUNULL:
        ret = subprocess.call(["git", "clone"] + github_clone_args,
                              stdout=FUNULL,
                              stderr=subprocess.STDOUT)

    if ret == 0:
        print "Installed", name, version
        with open(localmanifest, 'r') as f:
            mani = yaml.load(f)
            try:
                for plugin, version in mani['dependencies'].iteritems():
                    do_install(plugin, version)
            except KeyError:
                pass
    else:
        print "Failed", name, version


def do_board_install(boardyaml):
    with open(boardyaml, 'r') as f:
        boardyaml = yaml.load(f)
        try:
            for plugin, version in boardyaml.iteritems():
                do_install(plugin, version)
        except KeyError:
            pass


def is_plugin_installed(plugin, version):
    plugindir = os.path.join(handlersd, plugin.replace('/', '-'))
    pluginmanifest = os.path.join(plugindir, 'manifest.yaml')
    try:
        with open(pluginmanifest, 'r') as f:
            mani = yaml.load(f)
            installed = mani["version"] == version
        return installed
    except:
        return False


def do_install(plugin, version):
    if is_plugin_installed(plugin, version):
        print "Skipping", plugin, version
    else:
        do_github_install(plugin, version)


def install(args):
    if len(args.plugin) == 0:
        # user did not provide what plugin to install
        # we assume that user wants to install everything
        # prescribed on board.yaml
        boardyaml = os.path.join(os.getcwd(), "board.yaml")
        if os.path.exists(boardyaml):
            print "Installing from board.yaml"
            do_board_install(boardyaml)
        else:
            print "Cannot find board.yaml"
            sys.exit(errno.ENOENT)

    for pluginpack in args.plugin:
        plugin, sep, version = pluginpack.partition("==")
        do_install(plugin, version)

actions = {
    "init": init,
    "install": install
}

parser = argparse.ArgumentParser(
    description='board helps you manage serf plugins')
subparsers = parser.add_subparsers(help='sub-command help')

parser_init = subparsers.add_parser('init', help='init help')
parser_init.set_defaults(func=init)
parser_install = subparsers.add_parser('install', help='install help')
parser_install.add_argument('plugin', nargs='*')
parser_install.set_defaults(func=install)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
