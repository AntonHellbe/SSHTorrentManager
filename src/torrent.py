from bs4 import BeautifulSoup
import requests
from piratebay_search import Piratebay
import psutil
import subprocess
from web_api import MyWebApi



#TODO: Start deluge web and make sure the daemon is started and connected
def start_deluge():
    is_running_deluge = False
    for p in psutil.process_iter():
        #print(p.name())
        if p.name() == "deluge-web" or p.name() == "deluge":
            is_running_deluge = True

    if not is_running_deluge:
        subprocess.Popen("deluge-web")

def do_piratebay_search():
    print("Enter what to search for on piratebay")
    while(True):
        search_string = input()

        if search_string == "q":
            return

        if search_string == "":
            print("Empty string not allowed, try again")
            continue

        try:
            p.search_for_torrent(search_string)
            return
        except:
            print("Something went wrong when search for torrent")

def select_torrent_to_download():
    last_index = len(p.search_torrents)
    print("Select a torrent from {} to {} or q to quit".format(0, last_index), end=":")
    selected_torrent = None
    while(True):
        try:
            selected_torrent = input()
            if selected_torrent == "q":
                print("Exiting..")
                return

            selected_torrent = int(selected_torrent)
        except:
            print("Not a valid number")

        if selected_torrent < 0:
            continue
        elif selected_torrent > 29:
            continue
        magnet_link = p.search_torrents[selected_torrent].magnet_link
        result, error = m.add_torrent(magnet_link)
        if result:
            print("Torrent added successfully!")
            return
        else:
            print("Error adding torrent" + "\n" + error)

def print_all_found_torrents():
    if(len(p.search_torrents) == 0):
        print("You need to search first!")
    all_torrents = p.search_torrents
    for index, torrent in enumerate(all_torrents):
        print("{}. {}. \n    Seeders: {}, Leechers: {}".format(index, torrent.name, torrent.seeders, torrent.leechers))
    
    select_torrent_to_download()


def list_all_downloading_torrents():
    all_torrents = m.list_all_torrents()
    for index, torrent in enumerate(all_torrents):
        print("{}. {}".format(index, torrent["name"]))

    

def delete_torrent():
    all_torrents = m.downloading_torrents
    last_index = len(all_torrents)
    for index, torrent in enumerate(all_torrents):
        print("{}. {}".format(index, torrent.name))
    print("Select an index {}-{}".format(0, last_index))
    while(True):
        try:
            selected_index = input()
            if selected_index == "q":
                return
            selected_index = int(selected_index)
            if selected_index < 0 or selected_index > last_index:
                print("Index out of range")
            else:
                print("Remove data? y/n")
                while(True):
                    ye_or_no = input()
                    if ye_or_no == "y":
                        result, error = m.delete_torrent("a5cf0bdcef5cb69090c94e01c420272aa02746b5", remove_data=True)
                        if result:
                            print("Torrent and data delete successfully")
                        else:
                            print("Error deleting torrent and data \n" + error)

                        return
                            
                    elif ye_or_no == "n":
                        result, error = m.delete_torrent(torrent.hash_to_remove)
                        if result:
                            print("Torrent removed succesfully")
                        else:
                            print("Error deleting torrent \n" + error)
                        return
                    elif ye_or_no == "q":
                        return
                    else:
                        print("Invalid input, only yes or no allowed")
        except Exception as e:
            print("Invalid input, needs to be a number" + e)




def print_menu():
    print("1. Show all menu options")
    print("2. Do a piratebay search")
    print("3. List all found torrents")
    print("4. List all currently downloading torrents")
    print("5. Add a torrent by magnet link")
    print("6. Delete a torrent")
    print("Press q to exit any menu")

boot = True

menu = {
    1: print_menu,
    2: do_piratebay_search,
    3: print_all_found_torrents,
    4: list_all_downloading_torrents,
    6: delete_torrent
}

if __name__ == "__main__":
    p = Piratebay(720, 10)
    #start_deluge()
    m = MyWebApi()
    m.login()

    while(True):
        if boot:
            print_menu()
            boot = False
            
        selection = input()

        if selection == "q":
            print("Goodbye!")
            exit(0)
        if selection == "":
            continue
        selection = int(selection)

        if selection in menu:
            menu[selection]()



    






