# GNOME GHQ Search Provider

A GNOME Shell search provider that opens code repositories in [Kakoune Qt](https://github.com/falbru/kakoune-qt).

## Installation

```sh
git clone https://github.com/falbru/gnome-ghq-search-provider
cd gnome-ghq-search-provider
sudo ./install.sh
```

## Debugging

Stop the systemd/dbus service while keeping the search provider installed, then run:

```sh
python3 ./ghq-search-provider.py
```
