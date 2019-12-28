from imdb import IMDb
from bs4 import BeautifulSoup
import re
import requests
import pyperclip


class MovieManager:

    def __init__(self, movieName):
        self.name = movieName
        self.imdb = IMDb()
        self.website = 'https://yts.ws/movie/'

    def GetYearOfProd(self):
        movies = self.imdb.search_movie(self.name)
        # if the year of production is passed with the name of the movie we will get the movie by the year of prod
        # this is useful when there is a sequel (transporter 1, transporter 2 ...)
        year = re.search(' [1-2][0-9]{3}$', self.name)
        if year is None:
            return self.name.replace(' ', '-'), movies[0]['year']
        else:
            for movie in movies:
                if movie['year'] == int(year.group(0)) and movie['kind'] == 'movie':
                    return movie['title'].replace(':', '').replace(' ', '-'), year.group(0)
        return False

    def GetTorrentLink(self):
        title, year = self.GetYearOfProd()
        url = self.website + title + "-" + str(year)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        magnet_link = soup.find_all('a', attrs={'class': 'magnet-download download-torrent magnet'})[0].get('href')
        pyperclip.copy(str(magnet_link))
        print('link copied to the clipboard')
        return magnet_link
