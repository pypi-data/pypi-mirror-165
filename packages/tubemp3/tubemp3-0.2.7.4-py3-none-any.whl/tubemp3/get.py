
'''
get infovideo from only url 
'''

import requests as rq
from youtube_dl import YoutubeDL
import re
import os
import time
#from pydub import AudioSegment as As
import eyed3
from eyed3.id3.frames import ImageFrame


ydl_opts_mp3 = {
       #'outtmpl': f'{path_dir}/{path_music}.%(ext)s',
           'format': 'bestaudio/best',
            'noplaylist':'True',
      #     'postprocessors': [{
      #         'key': 'FFmpegExtractAudio',
      #         'preferredcodec': 'mp3',
      #         'preferredquality': f'{pref_quality}',
      # }],
   }
ydl = YoutubeDL()

class get_from_link(object):
    def __init__(self,url:str) -> None:
        #print('oi')
        
        token_video = url.split('/')[-1]
        
        url = f'https://www.youtube.com/watch?v={token_video}'
        self.url_yt = url
        r = ydl.extract_info(url, download=False)
        self.extract_info(r)
      
    def extract_info(self,res_ytdl):
        r = res_ytdl
        title = r.get('title')
        title = re.sub('[^A-Za-z0-9]+', '', title)
       # print(title)
        self.title = title
        # if any link will do 
        formats_ = [format for format in r['formats']]
        #print(formats_)
        formats = {}
        for format in formats_:
            if format.get('ext')=='mp4':
                formats[f'{format["format_note"]}'] = {'url':format['url'],
                                                       'fps':format['fps']}
            else:
                pass
        
        #self.types = [{format['ext'].split(' ')[0]:{'url':format['url']}} for format in formats]
        types = {}
        for format in formats_:
            types[format['ext'].split(' ')[0]] = {'url':format['url']}
            
        self.types = types
        self.formats = formats
    
    def __download(self,url,format):
        #url = self.types['m4a']['url']
        res = rq.get(url,stream=True)
        res.raise_for_status()
        
        size = int(res.headers.get('content-length'))
        size_mb = size/(1024**2)
        filename=f'{self.title}.{format}'
        bdiv = 1024
        with open(filename,'bw') as file:
            b = 0
            init_time = time.time()
            for byte in res.iter_content(chunk_size=bdiv):
                b=b+1
                file.write(byte)
                time_end = time.time() - init_time
                b_mb = b/bdiv
                down_fast = ((b)/time_end)
                percent = (((b/bdiv)/size_mb)*100)
                eta = ((size/(bdiv))-b)/down_fast
                print(f'[{filename[:7]+"..."}{filename[-7:]}  {percent:.2f}%  {(b_mb):.2f}MB/{size_mb:.2f}MB  {down_fast:.2f}Kb/s  eta:{eta:.0f}s  {time_end:.0f}s ',end='\r',flush=False)
        
        return filename
    
    def download_video(self,width=364):
        # try:
        #     url = self.formats[f'{width}']['url']
        # except:
        #     print(f'ERROR: width ({width}) not founded!')
        #     print(f'you can get the widht"s [{self.formats.keys()}] from it url')
        #     exit()
        print('please, choice a format')
        i = 1
        formats = []
        for format in self.formats.keys():
            #print(f'{i} - {format} - {self.formats[format]["fps"]}fps')
            formats.append(self.formats[format]['url'])
            i+=1
            
        choice = input('enter the number of your choice: ')
        choice = int(choice)-1
        url = formats[choice]
        self.__download(url,'mp4')
        pass
      
    def download_mp3(self):
      yt_m = YoutubeDL(ydl_opts_mp3)
      vd_data = yt_m.extract_info(self.url_yt,download=False)
      exts_list = vd_data.get('ext')
      
      
      self.extract_info(vd_data)
      url_m4a = self.types['m4a']['url']
      track = vd_data.get('track','Unknown')
      channel = vd_data.get('channel',None)
      artist = vd_data.get('artist',channel)
      year = vd_data.get('upload_date',None)[:4]
      album = vd_data.get('album','Unknown')
      duration = vd_data.get('duration')
      id_video = vd_data.get('id')
      title = vd_data.get('title')
      
      time_min = int(duration//60)
      time_sec = int(duration%60)
      time_sec = f'0{time_sec}' if len(str(time_sec)) == 1 else time_sec
      print(f'[music info] \ntitle:{title}\nduration:{time_min}:{time_sec}\nartist:{artist}\nid:{id_video}\nalbum:{album}\nyear:{year}')
      #print(self.title)
      #self.__download(url_m4a,'m4a')
      
      #file_m4a = As.from_file(f'{self.title}.m4a',format='m4a')
      file_mp3 = f'{self.title}'
      #file_m4a.export(file_mp3,format='mp3',bitrate='256k')
      
      ydl_opts = {
       'outtmpl': f'{file_mp3}.%(ext)s',
           'format': 'bestaudio/best',
           'postprocessors': [{
               'key': 'FFmpegExtractAudio',
               'preferredcodec': 'mp3',
               'preferredquality': f'320',
      }],
      }
      file_mp3 = f'{self.title}.mp3'
      if not os.path.isfile(file_mp3):
        with YoutubeDL(ydl_opts) as ydl:
          ydl.download([self.url_yt])

      #getting the mp3 tags
      thumb = vd_data.get('thumbnail')
      
      #saving thumb
      thumb_data = rq.get(thumb).content
      thumb_path = f'{self.title}.png'
      
      with open(thumb_path,'wb') as thumb_file:
        thumb_file.write(thumb_data)
      
      #editing the mp3 tag's
      audiofile = eyed3.load(file_mp3)
    
      mp3 = audiofile.tag
      mp3.artist = artist
      mp3.song = track
      mp3.title = title
      mp3.album = album
      mp3.save()
      #mp3.write()
      # if (audiofile.tag == None):
      #     audiofile.initTag()
      
      audiofile = eyed3.load(file_mp3)
      audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(
      thumb_path, 'rb').read(), 'image/jpeg')
      audiofile.tag.save()
      os.system(f'rm {thumb_path}')
      
      
      
      
      #url_download = self.types['m4a']['url']
      
      #self.__download(url_download,'m4a')