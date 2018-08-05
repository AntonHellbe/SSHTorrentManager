
class Torrent():

    def __init__(self, name, seeders = None, leechers = None, magnet_link = None, hash_to_remove = None):
        self.name = name
        self.seeders = seeders
        self.leechers = leechers
        self.magnet_link = magnet_link
        self.hash_to_remove = hash_to_remove

    def describe(self):
        return self.name + " " + str(self.seeders) + " " + str(self.leechers) + " " + str(self.hash_to_remove)
