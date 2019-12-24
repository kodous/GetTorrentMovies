from imdb import IMDb
from bs4 import BeautifulSoup
import requests
import pyperclip


class MovieManager:

    def __init__(self, movieName):
        self.name = movieName
        self.imdb = IMDb()
        self.website = 'https://yts.ws/movie/'

    def GetYearOfProd(self):
        movie = self.imdb.search_movie(self.name)
        return movie[0]['year']

    def GetTorrentLink(self):
        year = self.GetYearOfProd()
        url = self.website + self.name.replace(" ", "-") + "-" + str(year)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        # magnet_link = soup.body.section.div.div.div.div.contents[3].div
        magnet_link = soup.find_all('a', attrs={'class': 'magnet-download download-torrent magnet'})[0].get('href')
        pyperclip.copy(str(magnet_link))
        print('link copied to the clipboard')
        return magnet_link
