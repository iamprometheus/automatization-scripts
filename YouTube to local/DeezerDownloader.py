import requests
import json
from youtubesearchpython import VideosSearch
import yt_dlp
import glob
import os 
from mutagen.easyid3 import EasyID3

def request_deezer_music(api_url):
  response_API = requests.get(api_url)
  data = response_API.text
  parse_json = json.loads(data)
  return parse_json["data"]
  songs = []
  for item in parse_json["data"]:
    songs.append("{} - {} lyrics".format(item["title"], item["artist"]["name"]))

def download_audio(yt_url, song_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }
    ydl_opts['outtmpl'] = 'downloaded_music/' + song_name
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])

def add_metadata(title, artist, album):
  audio = EasyID3('./downloaded_music/' + title + '.mp3')
  audio['title'] = title
  audio['artist'] = artist
  audio['album'] = album
  audio.save()

def get_link(query):
  videosSearch = VideosSearch(query, limit = 2)
  return videosSearch.result()["result"][0]["link"]

def main():
  url = 'https://api.deezer.com/user/5571600264/tracks?index=280&limit=100'
  songs = request_deezer_music(url)

  for song in songs: 
    title = song["title"]
    artist = song["artist"]["name"]
    album = song["album"]["title"]
    search_query = "{} - {} lyrics".format(title, artist)
    
    yt_link = get_link(search_query)

    download_audio(yt_link, title)
    try: 
      add_metadata(title, artist, album)
    except:
      print("Coudn't add metadata to song {}".format(title))
    
main()
  