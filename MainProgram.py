from IMDBSeries import IMDBSeries
from JSONManager import JSONManager
from ResultsPageScrapper import ResultsPageScrapper
from TorrentPageScrapper import TorrentPageScrapper
import os


def DeleteHTMLFiles():
    for file in os.listdir(os.getcwd()):
        if file.endswith(".html"):
            os.remove(file)


def SeasonEpisodeNumbersToString(season, episode):
    if len(str(episode)) == 1:
        episode = '0' + str(episode)
    if len((str(season))) == 1:
        season = '0' + str(season)
    return str(season), str(episode)


jsonMan = JSONManager()
jsonMan.ReadJSONData()

resp = input("to add a tv Series, type a, else: hit any key").lower()
if resp == 'a':
    newSerial = input("enter the data formatted this way: name of the tvseries,number of episode,number of season").\
        split(",")
    serial = newSerial[0].strip()
    currentEpisode = newSerial[1].strip()
    currentSeason = newSerial[2].strip()
    jsonMan.AddSeries(serial, currentSeason, currentEpisode)
else:
    serial = input("enter the name of serial to download").strip()
# get the json Data
currentEpisode = jsonMan.GetEpisodeNumber(serial)
currentSeason = jsonMan.GetSeasonNumber(serial)

currentSeason, currentEpisode = SeasonEpisodeNumbersToString(currentSeason, currentEpisode)

# check the series on IMDB
imdb = IMDBSeries(serial)
# we pass the current season and episode numbers, and in return we get the episode and season to download
nextSeason, nextEpisode = imdb.GetNextEpisode(currentSeason, currentEpisode)
str_nextSeason, str_nextEpisode = SeasonEpisodeNumbersToString(nextSeason, nextEpisode)

imdb.GetAiringDate()
if imdb.IsDatePassed():
    fp = ResultsPageScrapper(serial, str_nextEpisode, str_nextSeason, filename=serial +
                                                                               str_nextSeason + str_nextEpisode + '1.html')
    link = fp.ExtractNamesAndLinks()
    sp = TorrentPageScrapper(serial, str_nextEpisode, str_nextSeason, link,
                             filename=serial + str_nextSeason + str_nextEpisode +
                                     "torrent.html")
    sp.ExtractLinkTorrent()
    jsonMan.SetSeasonNumber(serial, str_nextSeason)
    jsonMan.SetEpisodeNumber(serial, str_nextEpisode)
else:
    print('not passed')
DeleteHTMLFiles()
