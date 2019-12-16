from IMDBSeries import IMDBSeries
from JSONManager import JSONManager
from FirstPageScrapper import FirstPageScrapper
from SecondPageScrapper import SecondPageScrapper


def SeasonEpisodeNumbersToString(season, episode):
    if len(str(episode)) == 1:
        episode = '0' + str(episode)
    if len((str(season))) == 1:
        season = '0' + str(season)
    return str(season), str(episode)


serial = 'shameless'
# get the json Data
jsonMan = JSONManager()
jsonMan.ReadJSONData()
currentEpisode = jsonMan.GetEpisodeNumber(serial)
currentSeason = jsonMan.GetSeasonNumber(serial)

currentSeason, currentEpisode = SeasonEpisodeNumbersToString(currentSeason, currentEpisode)

# check the series on IMDB
imdb = IMDBSeries('shameless')
# we pass the current season and episode numbers, and in return we get the episode and season to download
nextSeason, nextEpisode = imdb.GetNextEpisode(currentSeason, currentEpisode)
str_nextSeason, str_nextEpisode = SeasonEpisodeNumbersToString(nextSeason, nextEpisode)

imdb.GetAiringDate()
if imdb.IsDatePassed():
    fp = FirstPageScrapper(serial, str_nextEpisode, str_nextSeason, filename=serial +
                                                                     str_nextSeason + str_nextEpisode + '1.html')
    link = fp.ExtractNamesAndLinks()
    sp = SecondPageScrapper(serial, str_nextEpisode, str_nextSeason, link,
                            filename=serial + str_nextSeason + str_nextEpisode +
                                     "torrent.html")
    sp.ExtractLinkTorrent()
else:
    print('not passed')
