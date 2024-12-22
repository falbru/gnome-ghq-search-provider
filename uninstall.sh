#!/usr/bin/env bash

set -eu pipefail
cd "$(dirname "$(realpath "${0}")")"

DATADIR=${DATADIR:-/usr/share}
LIBDIR=${LIBDIR:-/usr/lib}

# The actual executable
rm "${LIBDIR}"/ghq-search-provider/ghq-search-provider.py
rmdir "${LIBDIR}"/ghq-search-provider

# Search provider definition
rm "${DATADIR}"/gnome-shell/search-providers/org.gnome.Ghq.SearchProvider.ini

# DBus configuration (no-systemd)
rm "${DATADIR}"/dbus-1/services/org.gnome.Ghq.SearchProvider.service

# DBus configuration (systemd)
rm "${LIBDIR}"/systemd/user/org.gnome.Ghq.SearchProvider.service
