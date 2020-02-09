from imdb import IMDb
import datetime
from JSONManager import JSONManager


class IMDBSeries(JSONManager):

    def __init__(self, _seriesName):
        self.name = _seriesName
        self.imdb = IMDb()
        self.months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                       'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
        self.currentSeason = 1
        # this will contain an IMDB episode Object
        self.currentEpisode = ""
        self.airingDate = ""

    def GetNextEpisode(self, _currentSeason, _currentEpisode):
        serial = self.imdb.search_movie(self.name)[0]
        # add episodes field to the dictionary
        self.imdb.update(serial, 'episodes')
        sorted(serial['episodes'].keys())
        self.currentSeason = int(_currentSeason)

        number_of_seasons = len(serial['episodes'])
        number_of_episodes = len(serial['episodes'][self.currentSeason])
        next_episode = int(_currentEpisode) + 1

        if next_episode <= number_of_episodes:
            self.currentEpisode = serial['episodes'][self.currentSeason][next_episode]
            return self.currentSeason, next_episode
        # we pass to the next season
        elif self.currentSeason < number_of_seasons:
            self.currentEpisode = serial['episodes'][self.currentSeason+1][1]
            self.currentSeason = self.currentSeason + 1
            return self.currentSeason, 1
        else:
            print('there is no next episode')
            return 0, 0

    def GetAiringDate(self):
        self.airingDate = self.currentEpisode['original air date'].replace('.', '')
        return self.airingDate

    def IsDatePassed(self):
        self.airingDate = self.airingDate.split(" ")
        formatted_date = datetime.date(int(self.airingDate[2]), self.months[self.airingDate[1]],
                                       int(self.airingDate[0]))
        return formatted_date < datetime.date.today()



