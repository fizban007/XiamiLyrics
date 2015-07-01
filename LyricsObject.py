import os
import re
import eyed3

class Lyrics:
    def __init__ (self, content):
        self.content = content
        self.stripped = content
        # TODO: Detect if the content is of lrc form
        match = re.search(r'\[(.+?)\]', self.content, re.M)
        if match != None:
            self.isLrc = True
            self.stripped = re.sub(r'\[(.+?)\]', r'', self.content)
        else:
            self.isLrc = False

    def saveToFile (self, filename):
        out_file = filename
        if self.isLrc:
            out_file += ".lrc"
        else:
            out_file += ".txt"
        f = open(out_file, "wt")
        f.write(self.content)
        f.close()
        print("File saved!")

    def printContent (self):
        print(self.content)

    def printStripped (self):
        print(self.stripped)
