from pickle import TRUE
import requests
import os
import re
import json
import time
import time
from bs4 import BeautifulSoup
from random import random
import subprocess
import youtube_dl
import csv
# from bs4 import BeautifulSoup

class ChannelScraper:
    
    def __init__(self):
        self.channels = []
        self.processedChannels = []
        self.exportVideoMetadata = open('ytChannelVideosEN.csv', "a")
        pass
        
    def downloadSeachResults(self):
        """
        """
        # German channels: Link to the search results at the channel crawler including the number of result pages
        list_de = [
            ('https://www.channelcrawler.com/deu/results2/383982', 13),
            ('https://www.channelcrawler.com/deu/results2/383985', 5),
            ('https://www.channelcrawler.com/deu/results2/383989', 11),
            ('https://www.channelcrawler.com/deu/results2/383991', 11),
            ('https://www.channelcrawler.com/deu/results2/383997', 13),
            ('https://www.channelcrawler.com/deu/results2/383998', 3),
            ('https://www.channelcrawler.com/deu/results2/384004', 7),
            ('https://www.channelcrawler.com/deu/results2/384009', 8),
            ('https://www.channelcrawler.com/deu/results2/384013', 11),
            ('https://www.channelcrawler.com/deu/results2/384016', 4),
            ('https://www.channelcrawler.com/deu/results2/384017', 6),
            ('https://www.channelcrawler.com/deu/results2/384020', 8),
            ('https://www.channelcrawler.com/deu/results2/384022', 9),
            ('https://www.channelcrawler.com/deu/results2/384025', 7),
            ('https://www.channelcrawler.com/deu/results2/384026', 13),
            ('https://www.channelcrawler.com/deu/results2/384030', 7),
            ('https://www.channelcrawler.com/deu/results2/384032', 13),
            ('https://www.channelcrawler.com/deu/results2/384033', 9),
            ('https://www.channelcrawler.com/deu/results2/384034', 10)
        ]

        # Englisch channels: Link to the search results at the channel crawler including the number of result pages
        list_en = [
            """
            https://channelcrawler.com/eng/results2/731288, 9
            https://channelcrawler.com/eng/results2/731295, 6
            https://channelcrawler.com/eng/results2/731298, 4
            https://channelcrawler.com/eng/results2/731299,10
            https://channelcrawler.com/eng/results2/731305,10
            """
        ]

        list = list_de

        # iterate search results
        j = 0
        for res in list:
            j = j + 1
            print('iterate search no '+ j)
            i = 0
            # iterate pages
            while i <= res[1]:
                i = i + 1
                file_name = "ytData/de-education-" + str(j) + '-' + str(i) + '.html'
                export_file = open(file_name, "w")
                self.getSearchResults(str(res[0])+'/page:'+str(i), export_file)
                time.sleep(random() * 1)
    
    """
    """
    def getSearchResults(self, url, export_file):
        """
        """
        try:
            data = requests.get(url).text
            export_file.write(data)
            
        except requests.exceptions.RequestException as e:
            print("ERROR! url " + url + "\nError Info:\n")

    
    """
    """
    def getChannelURLs(self):
        """
        """
        i = 0
        folder = 'ytData'
        for file in os.listdir(folder):
            html_doc = open(os.path.join(folder,file), "r")
            soup = BeautifulSoup(html_doc, "html.parser")
            for tags in soup.find_all('h4'):
                tag = tags.find('a')
                if tag is None:
                    continue
                print(i, tag.get('href'))
                self.channels.append(tag.get('href') + '/videos')
                i = i + 1
        pass


    """
    Loads a list of channel URLs from a CSV file
    """
    def loadChannelsFromFile(self, filepath):
        with open(os.path.join(filepath), newline='') as csvfile:
            content = csv.reader(csvfile, delimiter=';', quotechar='"')
            for row in content:
                self.channels.append(str(row[1]) + '/videos')
            print('Finished loading channels from file')
        pass
    
    
    """
    skip: in case the process has to be restarted, the previously processed channels can be skipped
    """
    def getChannelVideoData(self, skip=1):
        ydl_opts = {
            #'extract_flat': True,  # --flat-playlist according to options.py
            'dumpjson': True,  # lower -j
            'cookies-from-browser': '/Volumes/DATA0/nise/Library/Application Support/Firefox/Profiles/9sjo69fk.nise',#'/home/abb/.mozilla/firefox/9sjo69fk.default',
            'quiet': True,
            #'dump_single_json': True, ## UPPER -J
        }
        
        i = 0
        for channel in self.channels:
            i = i + 1
            if i < skip:
                continue
            print('\n')
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print('Process channel ',i,'  ', channel)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                try:
                    object = ydl.extract_info(channel, download=False)
                    if 'entries' in object:
                        # Can be a playlist or a list of videos
                        for vid in object['entries']:
                            self.getParam(vid, channel)
                    else:
                        self.getParam(object, channel)
                #except youtube_dl.utils.ExtractorError:
                except youtube_dl.utils.DownloadError:
                    pass


    """
    """
    def getParam(self, vid, channel_url):
        if 'categories' in vid and len(vid['categories']) > 0:
            cat = ",".join(vid['categories']).replace(';', ',') 
        else: 
            cat = ''
        if 'tags' in vid and len(vid['tags']) > 0:
            tags = ",".join(vid['tags']).replace(';', ',') 
        else: 
            tags = ''
        if 'channel' in vid:
            channel_name = vid['channel']
        else:
            channel_name = ''
    
        out = [
            channel_url,
            channel_name.replace(';',','),
            vid['id'],
            vid['title'].replace(';', ','),
            vid['upload_date'],
            vid['duration'],
            vid['view_count'],
            vid['average_rating'],
            cat,
            tags
        ]
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',';'.join(map(str, out)))
        self.exportVideoMetadata.write(';'.join(map(str, out))+'\n')
    
    
if __name__ == "__main__":
    s = ChannelScraper()
    
    # Step 1: Collect YouTube channels from https://www.channelcrawler.com/
    ### s.downloadSeachResults()
    
    # Step 2: Collect to channel URLs for each channel collected in step 1
    #s.getChannelURLs()
    s.loadChannelsFromFile('ytChannelsEN.csv')
    
    # Step 3: Collect meta data for each video in the channels collected in step 2
    s.getChannelVideoData(skip=386)
