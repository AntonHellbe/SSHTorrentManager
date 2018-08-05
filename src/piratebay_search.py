from bs4 import BeautifulSoup
import requests
import urllib
import math
from torrent_data import Torrent

SEARCH_URL = "https://thepiratebay.org/search/"


class Piratebay():

    def __init__(self, quality, seeder_lim):
        self.quality = quality
        self.seeder_lim = seeder_lim
        self.search_torrents = []

    def search_for_torrent(self, search_string):

        encoded_string = urllib.parse.quote(search_string)
        search_content = requests.get(SEARCH_URL + encoded_string)
        soup_content = BeautifulSoup(search_content.content, "html.parser")
        #print(soup_content)
        names = soup_content.find_all(class_ = 'detName')
        seeders_and_leechers = soup_content.find_all(align = "right")
        links = soup_content.find_all(title="Download this torrent using magnet")
        
        self.collect_all_torrents(names, seeders_and_leechers, links)
    
    def collect_all_torrents(self, torrents_names, seeders_and_leechers, links):
        all_torrent_names = self.parse_torrents_names(torrents_names)
        all_torrent_seeders_and_leechers = self.parse_seeders_and_leechers(seeders_and_leechers)
        all_links = self.parse_magnet_links(links)
        
        min_len = min(len(all_links), len(all_torrent_names), len(all_torrent_seeders_and_leechers))

        for i in range(0, min_len):
            torrent = Torrent(all_torrent_names[i], all_torrent_seeders_and_leechers[i][0], 
            all_torrent_seeders_and_leechers[i][1], all_links[i])
            self.search_torrents.append(torrent)

        #for torrent in self.search_torrents:
            #print(torrent.describe())
        
        

    def parse_torrents_names(self, all_torrents):
        all_torrent_names = list()
        for index, torrent in enumerate(all_torrents):
            torrent_name = ''.join(torrent.a["title"].split(" ")[2:])
            all_torrent_names.append(torrent_name)

        return all_torrent_names

    def parse_seeders_and_leechers(self, all_torrents):
        all_seeders_and_leechers = list()
        for i in range(0, len(all_torrents), 2):
            all_seeders_and_leechers.append((int(all_torrents[i].getText()), int(all_torrents[i + 1].getText())))

        return all_seeders_and_leechers

    def parse_magnet_links(self, all_links):
        all_magnet_links = list()
        for link in all_links:
            all_magnet_links.append(link["href"])
        
        #print(all_magnet_links)
        return all_magnet_links
    
    def find_best_torrent(self):
        return None
