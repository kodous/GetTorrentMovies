import requests
from bs4 import BeautifulSoup
import os


class FirstPageScrapper:

    def __init__(self, series, episode, season, filename="pageContents.html"):
        # initialization
        self.filename = filename
        self.file_path = os.path.join(os.getcwd(), self.filename)
        self.episode = episode
        self.season = season
        self.series_name = series
        self.preferredUploader = ['worldmkv', '720p.WEB', 'WEB-DL']
        self.good_episodes = []
        self.site = "https://www.1337x.am"

    def GetAllNames(self):
        return self.good_episodes

    def CompareNames(self, torrentName):
        if self.series_name in torrentName.lower():
            return True
        elif self.series_name.replace(" ", ".") in torrentName.lower():
            return True
        else:
            return False

    def CompareSizes(self, torrentSize):
        if 200 <= float(torrentSize) <= 500:
            return True
        return False

    def CheckUploader(self, name):
        if self.preferredUploader[0] in name:
            return True
        elif self.preferredUploader[1] in name:
            return True
        elif self.preferredUploader[2] in name:
            return True
        return False

    def CheckSeasonAndEpisode(self, torrentName):
        if (self.season in torrentName) and (self.episode in torrentName):
            return True
        return False

    def SaveHTMLToFile(self, name_to_search, second=False):
        if not os.path.isfile(self.file_path):
            if not second:
                name_to_search.replace(" ", "%20")
                url = "https://www.1337x.am/sort-search/" + name_to_search + "/time/desc/1/"
            else:
                url = self.good_episodes[0]
            r = requests.get(url)

            # write contents to a file
            file_writer = open(self.filename, 'w')
            file_writer.write(str(r.content))
            file_writer.close()

    def HTMLToSoup(self):
        self.SaveHTMLToFile(self.series_name, True)
        file_reader = open(self.filename, 'r')
        web_contents = BeautifulSoup(file_reader.read(), 'html5lib')
        return web_contents

    def ExtractNamesAndLinks(self):
        table_of_all_episodes = self.HTMLToSoup().find('table',
                                                       attrs={
                                                           'class': 'table-list table table-responsive table-striped'})
        different_uploader = []
        # go through all episodes
        for tds in table_of_all_episodes.tbody:
            class_name = tds.find(attrs={'class': "coll-1 name"})
            episode_name = class_name.find_all('a')[1]
            episode_size = tds.find_all('td')[4].text
            episode_size2 = episode_size[0: episode_size.index(" ")]
            if self.CompareNames(str(episode_name.string)) and self.CompareSizes(episode_size2) and \
                    self.CheckSeasonAndEpisode(episode_name.string):

                if self.CheckUploader(episode_name.string):
                    self.good_episodes.append(self.site + episode_name.get('href'))
                else:
                    different_uploader.append(self.site + episode_name.get('href'))

        if len(self.good_episodes) != 0:
            return self.good_episodes[0]
        self.good_episodes = different_uploader
        return different_uploader

