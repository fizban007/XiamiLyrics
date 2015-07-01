import requests
import re
import LyricsObject

xiami_search_prefix = "http://www.xiami.com/search?key="
xiami_song_prefix = "http://www.xiami.com/song/"
xiami_detail_prefix = "http://www.xiami.com/song/playlist/id/"
headers = {"user-agent" : "Gecko/20100101 Firefox/36.0"}

def fetch_lyrics (title, artist):
   r = requests.get(xiami_search_prefix + title + ' ' + artist, headers=headers)
   r.encoding = 'UTF-8'
   match = re.search(r'/song/(\d+)', r.text, re.M)
   if match == None:
       print("Song not found!!")
       return None
   else:
       song_id = match.groups()[0]

       # First search for lrc file
       song_detail_url = xiami_detail_prefix + song_id
       page = requests.get(song_detail_url, headers = headers)
       page.encoding = 'UTF-8'
       match = re.search(r'<lyric>(.+?)</lyric>', page.text, re.M | re.S)
       if match != None:
           lyrics_url = match.groups()[0]
           lyrics_content = requests.get(lyrics_url, headers = headers)
           lyrics_content.encoding = 'UTF-8'
           return LyricsObject.Lyrics(lyrics_content.text)
       else: # No lrc file found, try to find the lyrics in the song page directly
           song_url = xiami_song_prefix + song_id
           page = requests.get(song_url, headers = headers)
           page.encoding = 'UTF-8'
           match = re.search(r'<div class="lrc_main">(.+?)</div>', page.text, re.M | re.S)
           if match != None:
               lyrics_text = match.groups()[0]
               lyrics_text = re.sub(r'<.+?>', '', lyrics_text)
               lyrics_text = re.sub(r'(?:\r?\n)', '\n', lyrics_text)
               lyrics_text = re.sub(r"\\'", "'", lyrics_text)
               lyrics_text = '\n'.join([i.strip()
                                        for i in lyrics_text.split('\n')]).strip()
               return LyricsObject.Lyrics(lyrics_text)
           else:
               return None
 


