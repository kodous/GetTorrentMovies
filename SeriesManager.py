import requests
from bs4 import BeautifulSoup
import os


class ResultsPageScrapper:

    def __init__(self, series, episode, season, filename="pageContents.html"):
        # initialization
        self.filename = filename
        self.file_path = os.path.join(os.getcwd(), self.filename)
        self.episode = episode
        self.season = season
        self.series_name = series
        self.preferredUploader = ['worldmkv', '720p.WEB', 'WEB-DL']
        self.good_episodes = []
        self.actualResultsPage = 1
        self.site = "https://www.1377x.to"

    def GetAllNames(self):
        return self.good_episodes

    def CheckName(self, torrentName):
        if self.series_name in torrentName.lower():
            return True
        elif self.series_name.replace(" ", ".") in torrentName.lower():
            return True
        else:
            return False

    def CheckSize(self, torrentSize):
        try:
            if 200 <= float(torrentSize) <= 500:
                return True
            return False
        except Exception as e:
            return False

    def CheckUploader(self, name):
        if self.preferredUploader[0] in name or self.preferredUploader[1] in name or self.preferredUploader[2] in name:
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
                url = "https://www.1377x.to/sort-search/" + name_to_search + "/time/desc/" + \
                      str(self.actualResultsPage) + "/"
            else:
                url = self.good_episodes[0]
            r = requests.get(url)

            # write contents to a file
            file_writer = open(self.filename, 'w')
            file_writer.write(str(r.content))
            file_writer.close()

    def HTMLToSoup(self, second=False):
        self.SaveHTMLToFile(self.series_name, second)
        file_reader = open(self.filename, 'r')
        web_contents = BeautifulSoup(file_reader.read(), 'html5lib')
        return web_contents

    def ExtractNamesAndLinks(self):
        # TODO Compare last episode number on the page with the episode we are looking for
        different_uploader = []
        link_found = False

        while (len(self.good_episodes) == 0 and len(different_uploader) == 0) and self.actualResultsPage < 10:
            table_of_all_episodes = self.HTMLToSoup().find('table',
                                                           attrs={
                                                               'class': 'table-list table table-responsive table-striped'})
            # go through all episodes
            for tds in table_of_all_episodes.tbody:
                # etract name and size of the episode
                class_name = tds.find(attrs={'class': "coll-1 name"})
                episode_name = class_name.find_all('a')[1]
                episode_size_object = tds.find_all('td')[4].text
                episode_size = episode_size_object[0: episode_size_object.index(" ")]
                # check the size and name of the episode
                if self.CheckName(str(episode_name.string)) and self.CheckSize(episode_size) and self.CheckSeasonAndEpisode(episode_name.string):

                    link_found = True
                    # if we got a good episode, we stop, else we continue
                    if self.CheckUploader(episode_name.string):
                        self.good_episodes.append(self.site + episode_name.get('href'))
                        break
                    else:
                        different_uploader.append(self.site + episode_name.get('href'))
            # go to the next result page
            if not link_found:
                self.actualResultsPage += 1
                self.filename = 'pageresult' + str(self.actualResultsPage) + '.html'
                self.file_path = os.path.join(os.getcwd(), self.filename)

        if len(self.good_episodes) != 0:
            return self.good_episodes[0]
        elif len(different_uploader) != 0:
            self.good_episodes = different_uploader
            return different_uploader[0]
        else:
            return 0

    # TODO Sort returned links by number of seeders and leechers
