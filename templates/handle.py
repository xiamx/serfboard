#!/usr/bin/env python

import os
import yaml
import subprocess
handlersd = os.path.abspath("handlers")
plugins = os.listdir(handlersd)

if os.environ["SERF_EVENT"] == "user":
    EVENT = "user:" + os.environ["SERF_USER_EVENT"]
else:
    EVENT = os.environ["SERF_EVENT"]

for plugin in plugins:
    plugin_abs_d = os.path.join(handlersd, plugin)
    plugin_manifest = os.path.join(plugin_abs_d, "manifest.yaml")
    with open(plugin_manifest, 'r') as f:
        mani = yaml.load(f)
        try:
            for handler in mani["handlers"]:
                if handler["event"] != EVENT:
                    continue

                script = os.path.join(plugin_abs_d,
                                      handler["script"])
                args = [script]
                print "Spawning", plugin, "handler for", EVENT
                sub = subprocess.Popen(args, env=os.environ.copy())
                exitcode = sub.wait()

                if (exitcode != 0):
                    raise PluginExecuteError(plugin, EVENT, exitcode)
        except KeyError:
            pass


class PluginExecuteError(Exception):
    def __init__(self, plugin, event, exitcode):
        self.plugin = plugin
        self.event = event
        self.exitcode = exitcode
