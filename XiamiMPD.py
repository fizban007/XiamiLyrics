#!/usr/bin/python

from mpd import MPDClient
import requests
import re
import os
import LyricsObject
import Xiami
from mutagen.id3 import ID3

client = MPDClient()
client.idletimeout = None
client.connect("localhost", 6600)

current_title = client.currentsong()['title']
current_artist = client.currentsong()['artist']

print(current_title)
print(current_artist)

lo = Xiami.fetch_lyrics(current_title, current_artist)
if lo != None:
    lo.printContent()
# if lo.isLrc:
    lo.saveToFile(os.path.expanduser("~/.lyrics/") + current_artist + " - " + current_title);
# else:
#     f = client.currentsong()['file']
#     song = ID3(os.path.expanduser("~/Music/") + f)
#     print(song)

# lo.saveToTag()
