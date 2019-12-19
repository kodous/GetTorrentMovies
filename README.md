# GetTorrentMovies
this is a python package that downloads torrent links from the internet
i uses python 3.6 and windows10
for the moment it only downloads torrent links for episodes of tv series from https://1377x.am, it's a work in progress
 and many comments and functions are missing.

ResultsPageScrapper: it's a class that analyzes the page of the results sorted by the added date
TorrentPageScrapper: it inherits from ResultPageScrapper and and analyzes the page of the torrent page in order to get the link
                     of the magnet torrent
IMDBSeries: it looks for the next tv episode to download on the IMDB server if the airing date had passed
JSONManager: it saves, updates and reads a json file, where the tv series are saved, this way, the next time you want to download an 
             episode, it looks directly for the next episode compared to the one in the JSON file.
MainProgram is the main program. if all goes well, the link of the magnet torrent will be copied to the clipboard automatically

the architecture of the program is as follows:
  1- read JSON file and extract the Episode and season number written on the file
  2- create an IMDBSeries object which will check if there is a next episode or not, and whether is has been aired or not yet
    (in the sake of the tutorial, we will suppose it had been aired)
  3- pass the episode and season number to the ResultsPageScrapper as arguments, so it will return later a link to the page
    of the selected episode ( the chosen episode will have a size between 200 and 500 Mo and it is preferable to be 720p or downloaded
    by some uploaders )
  4- the link of the episode page will then be passed as an argument to a TorrentPageScrapper object who will eventually copy the
    magnet link torrent to the clipboard
    
in order for this to work on your computer you have to import certain modules:
beautifulSoup: it is used to scrap web pages
  pip install beautifulsoup4
pyperclip: it is used to manage the clipboard
  pip install clipboard
IMDB: it used to communicate with the imdb servers (look up this doc: https://imdbpy.readthedocs.io/en/latest/usage/series.html)
  pip install IMDbPY
  
