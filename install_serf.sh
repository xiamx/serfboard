#!/bin/sh

tempdir=$(mktemp -d)
cd $tempdir
wget https://dl.bintray.com/mitchellh/serf/0.6.1_linux_amd64.zip
unzip 0.6.1_linux_amd64.zip

sudo cp serf /usr/local/bin/serf

rm -rf $tempdir
