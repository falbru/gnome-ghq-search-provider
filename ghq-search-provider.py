#!/usr/bin/env python3

import dbus
import dbus.service
import os
import sys
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

SBN = dict(dbus_interface="org.gnome.Shell.SearchProvider2")

class GhqSearchProvider(dbus.service.Object):
    bus_name = "org.gnome.Ghq.SearchProvider"
    _object_path = "/org/gnome/Ghq/SearchProvider"

    def __init__(self):
        self.results = {}
        self.session_bus = dbus.SessionBus()
        bus_name = dbus.service.BusName(self.bus_name, bus=self.session_bus)
        dbus.service.Object.__init__(self, bus_name, self._object_path)

    @dbus.service.method(in_signature="as", out_signature="as", **SBN)
    def GetInitialResultSet(self, terms):
        if "hello" in terms:
            self.results = {"1": "Hello World"}
            return ["1"]
        return []

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
                    'name': self.results[id],
                    'description': "A simple Hello World result",
                    'gicon': "utilities-terminal"
                })
        return metas

    @dbus.service.method(in_signature="sasu", **SBN)
    def ActivateResult(self, id, terms, timestamp):
        print(f"Activated result: {self.results.get(id, 'Unknown')}")

    @dbus.service.method(in_signature="asu", terms="as", timestamp="u", **SBN)
    def LaunchSearch(self, terms, timestamp):
        print("Search launched with:", terms)

if __name__ == "__main__":
    DBusGMainLoop(set_as_default=True)
    GhqSearchProvider()
    GLib.MainLoop().run()
