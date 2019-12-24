from SeriesResultsPageScrapper import ResultsPageScrapper
from SeriesTorrentPageScrapper import TorrentPageScrapper
import json
episode = "09"
season = "03"
series = "the good doctor"


class JSONManager:

    def __init__(self):
        self.jsonFileName = 'data.txt'
        self.jsonData = {}

    def ReadJSONData(self):

        jsonreader = open(self.jsonFileName, 'r')
        json_data = json.loads(jsonreader.read())
        jsonreader.close()
        self.jsonData = json_data['series']

    def WriteJsonData(self):
        new_json_data = {"series": self.jsonData}
        json_writer = open('data.txt', 'w')
        json_writer.write(json.dumps(new_json_data, indent=4))
        json_writer.close()

    def GetEpisodeNumber(self, seriesName):
        try:
            for serial in self.jsonData:
                if serial['name'] == seriesName:
                    return serial['episode']
            return 'the series you are looking for is not in the system'
        # in case the series is not in the file, an exception will be raised
        except Exception as e:
            print("the series you are looking for is not included in the system", e)

    def GetSeasonNumber(self, seriesName):
        try:
            for serial in self.jsonData:
                if serial['name'] == seriesName:
                    return serial['season']
            return 'the series you are looking for is not in the system'

        except Exception as e:
            print("the series you are looking for is not included in the system", e)

    def GetAllSeries(self):
        return self.jsonData

    def SetSeasonNumber(self, _seriesName, _seasonNumber):
        for serial in self.jsonData:
            if serial['name'] == _seriesName:
                serial['season'] = _seasonNumber
                self.WriteJsonData()
                return True
        return False

    def SetEpisodeNumber(self, _seriesName, _episodeNumber):
        for serial in self.jsonData:
            if serial['name'] == _seriesName:
                serial['episode'] = _episodeNumber
                self.WriteJsonData()
                return True
        return False

    def SeriesExist(self, _seriesName):
        for serial in self.jsonData:
            if serial['name'] == _seriesName:
                return True
        return False

    def AddSeries(self, _seriesName, _seasonNumber="01", _episodeNumber="00"):
        if self.jsonData == {}:
            self.ReadJSONData()

        if not self.SeriesExist(_seriesName):
            new_series_data = {"name": _seriesName, "episode": _episodeNumber, "season": _seasonNumber}
            self.jsonData.append(new_series_data)
            self.WriteJsonData()
            print('series added with success')
        else:
            print("series already exists")


