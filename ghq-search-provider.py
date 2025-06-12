#!/usr/bin/env python3

import dbus
import dbus.service
import os
import sys
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

import subprocess

SBN = dict(dbus_interface="org.gnome.Shell.SearchProvider2")

class GhqSearchProvider(dbus.service.Object):
    bus_name = "org.gnome.Ghq.SearchProvider"
    _object_path = "/org/gnome/Ghq/SearchProvider"

    def __init__(self):
        self.results = {}
        self.session_bus = dbus.SessionBus()

        self.ghq_root = subprocess.run(["ghq", "root"], capture_output=True, text=True, check=True).stdout.strip()

        bus_name = dbus.service.BusName(self.bus_name, bus=self.session_bus)
        dbus.service.Object.__init__(self, bus_name, self._object_path)

    @dbus.service.method(in_signature="as", out_signature="as", **SBN)
    def GetInitialResultSet(self, terms):
        output = subprocess.run(["ghq", "list"], capture_output=True, text=True).stdout
        repos = output.split("\n")[:-1]
        filenames = [repo.split('/')[-1] for repo in repos]

        out = []
        self.results = {}
        for i, filename in enumerate(filenames):
            for term in terms:
                if term in filename:
                    id = str(i)
                    self.results[id] = {
                        "name": filename,
                        "repo": repos[i]
                    }
                    out.append(id)
        return out

    @dbus.service.method(in_signature="asas", out_signature="as", **SBN)
    def GetSubsearchResultSet(self, previous_results, new_terms):
        return self.GetInitialResultSet(new_terms)

    @dbus.service.method(in_signature="as", out_signature="aa{sv}", **SBN)
    def GetResultMetas(self, ids):
        metas = []
        for id in ids:
            if id in self.results:
                metas.append({
                    'id': id,
                    'name': self.results[id]["name"],
                    'description': self.results[id]["repo"],
                })
        return metas

    @dbus.service.method(in_signature="sasu", **SBN)
    def ActivateResult(self, id, terms, timestamp):
        project = self.results.get(id)
        work_directory = self.ghq_root + "/" + project["repo"]
        subprocess.Popen(["k"], cwd=work_directory)

    @dbus.service.method(in_signature="asu", terms="as", timestamp="u", **SBN)
    def LaunchSearch(self, terms, timestamp):
        pass

if __name__ == "__main__":
    DBusGMainLoop(set_as_default=True)
    GhqSearchProvider()
    GLib.MainLoop().run()
