#!/usr/bin/env bash

set -eu pipefail
cd "$(dirname "$(realpath "${0}")")"

DATADIR=${DATADIR:-/usr/share}
LIBDIR=${LIBDIR:-/usr/lib}

# The actual executable
install -Dm 0755 ghq-search-provider.py "${LIBDIR}"/ghq-search-provider/ghq-search-provider.py

# Search provider definition
install -Dm 0644 conf/org.gnome.Ghq.SearchProvider.ini "${DATADIR}"/gnome-shell/search-providers/org.gnome.Ghq.SearchProvider.ini

# DBus configuration (no-systemd)
install -Dm 0644 conf/org.gnome.Ghq.SearchProvider.service.dbus "${DATADIR}"/dbus-1/services/org.gnome.Ghq.SearchProvider.service

# DBus configuration (systemd)
install -Dm 0644 conf/org.gnome.Ghq.SearchProvider.service.systemd "${LIBDIR}"/systemd/user/org.gnome.Ghq.SearchProvider.service
