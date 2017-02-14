# Bulletproof Arma Launcher
# Copyright (C) 2016 Sascha Ebert
# Copyright (C) 2016 Lukasz Taczuk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from __future__ import unicode_literals

import os

from torrent_utils import is_complete_quick


class Mod(object):
    """encapsulate data needed for a mod"""
    def __init__(
            self,
            foldername='@noname',
            parent_location=None,
            torrent_url=None,
            torrent_timestamp='',
            full_name='',
            version='0',
            up_to_date=None):
        super(Mod, self).__init__()

        self.parent_location = parent_location  # 'C:\Arma 3\<default_mod_dir>'
        self.torrent_url = torrent_url  # 'https://my.domain/file.torrent'
        self.foldername = foldername  # '@CBA_A3'
        self.torrent_timestamp = torrent_timestamp  # datetime
        self.full_name = full_name  # 'Community Base Addons v.123.4'
        self.version = version  # "0.1-alpha6" (optional)
        self.up_to_date = up_to_date

    def get_full_path(self):
        return os.path.join(self.parent_location, self.foldername)

    def is_complete(self):
        """Return information on whether the mods is fully synchronized and
        ready to use.
        The data is cached so it is fine to call this method repeatedly.
        """

        if self.up_to_date is None:
            self.up_to_date = is_complete_quick(self)

        return self.up_to_date

    def force_completion(self):
        self.up_to_date = True

    @classmethod
    def fromDict(cls, d):
        """Return a new mod instance constructed from a dictionary."""

        torrent_timestamp = d.get('torrent-timestamp', "")
        full_name = d.get('full_name', "Unknown Mod")
        foldername = d.get('foldername', "@Unknown")
        torrent_url = d.get('torrent_url', "")
        version = d.get('version', '0')

        m = Mod(foldername=foldername, torrent_timestamp=torrent_timestamp,
                full_name=full_name, torrent_url=torrent_url, version=version)
        return m

    def __repr__(self):
        s = '[Mod: {} -- utcts: {} -- {} -- durl: {} -- version: {}]'.format(
            self.foldername, self.torrent_timestamp, self.full_name, self.torrent_url,
            self.version)

        return s
