from IMDBSeries import IMDBSeries
from JSONManager import JSONManager
from SeriesResultsPageScrapper import ResultsPageScrapper
from SeriesTorrentPageScrapper import TorrentPageScrapper
from MovieManager import MovieManager
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


DeleteHTMLFiles()
jsonMan = JSONManager()
jsonMan.ReadJSONData()

resp = input("to download a movie type m, else, type any key: ").lower()
if resp == "m":
    movie = input("the name of the movie: ")
    mm = MovieManager(movie)
    mm.GetTorrentLink()
else:
    resp = input("to add a tv series, hit a, else hit any key: ")
    if resp == 'a':
        newSerial = input("enter the data formatted this way: name of the tvseries,"
                          "number of episode,number of season: ").split(",")
        serial = newSerial[0].strip()
        currentEpisode = newSerial[1].strip()
        currentSeason = newSerial[2].strip()
        jsonMan.AddSeries(serial, currentSeason, currentEpisode)
    else:
        serial = input("enter the name of serial to download: ").strip()

    while True:
        # get the json Data related to the TVSerial
        currentEpisode = jsonMan.GetEpisodeNumber(serial)
        currentSeason = jsonMan.GetSeasonNumber(serial)
        currentSeason, currentEpisode = SeasonEpisodeNumbersToString(currentSeason, currentEpisode)

        # check the series on IMDB
        imdb = IMDBSeries(serial)
        # we pass the current season and episode numbers, and in return we get the episode and season to download
        nextSeason, nextEpisode = imdb.GetNextEpisode(currentSeason, currentEpisode)
        # if this happens, it means there is no next episode
        if (nextSeason, nextEpisode) == (0, 0):
            print('there is no next episode')
            break

        str_nextSeason, str_nextEpisode = SeasonEpisodeNumbersToString(nextSeason, nextEpisode)
        imdb.GetAiringDate()
        if imdb.IsDatePassed():
            fp = ResultsPageScrapper(serial, str_nextEpisode, str_nextSeason, filename=serial +
                                                           str_nextSeason + str_nextEpisode + '1.html')
            try:
                link = fp.ExtractNamesAndLinks()
            except Exception as e:
                print("Exception happened: ", str(e))
                DeleteHTMLFiles()
                break
            if link == 0:
                DeleteHTMLFiles()
                break
            sp = TorrentPageScrapper(serial, str_nextEpisode, str_nextSeason, link,
                                     filename=serial + str_nextSeason + str_nextEpisode +
                                              "torrent.html")
            sp.ExtractLinkTorrent()
            jsonMan.SetSeasonNumber(serial, str_nextSeason)
            jsonMan.SetEpisodeNumber(serial, str_nextEpisode)
            input("hit any key to download next episode ")
        else:
            print('Episode not Aired yet')
            break
        DeleteHTMLFiles()
