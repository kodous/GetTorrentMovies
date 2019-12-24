from SeriesResultsPageScrapper import ResultsPageScrapper
import pyperclip


class TorrentPageScrapper(ResultsPageScrapper):

    def __init__(self, series, episode, season, torrentLink, filename='secondPageContents.html'):
        ResultsPageScrapper.__init__(self, series, episode, season, filename)
        self.good_episodes.append(torrentLink)
        self.filename = filename

    def ExtractLinkTorrent(self):
        web_contents = self.HTMLToSoup(True)
        first_div = web_contents.find('div', attrs={'class': 'box-info torrent-detail-page vpn-info-wrap'})
        magnet_link = first_div.find_all('div')[1].div.ul.li.a.get('href')
        pyperclip.copy(str(magnet_link))
        print('link copied to the clipboard')



