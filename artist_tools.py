import re, os
import xml.etree.ElementTree as ET
import xml_tools, websearch, wikisearch
from tinytag import TinyTag
import eyed3
from mutagen.easyid3 import EasyID3
import time
import concurrent.futures
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC

def find_artist_name(song, file, **kwargs):
    """
    set recommended frame song details
    :param song: song name string
    :param file: tiny tag object
    :return:
    """
    raw_song_name = song
    song = norm(song)
    artist = file.artist
    song_path = kwargs.get("paths")
    song_path = song_path.get("songs_path")
    artist, title, __ = build_song_profile(song_path, raw_song_name)
    """if artist is not None:
        artist, title = artist_exist(file, song, artist)
    else:
        artist, title = non_artist(file, song, **kwargs)
    return norm(remove_forbidden(artist), title=True), norm(remove_forbidden(title), title=True)"""
    xml_tools.add_artist(artist)
    return norm(remove_forbidden(artist), web=True, title=True), norm(remove_forbidden(title), web=True, title=True)


def artist_exist(file, name, artist):
    """
    extract the title name from the file name
    :param name: file name
    :param file: tiny tag object
    :param artist: artist tag of the file
    :return: 
    """
    title = file.title
    if title is None:
        title = name.remove(artist, '')
    return artist, title


def non_artist(file, name, **kwargs):
    """
    search for the artist of the givven file
    :param file: tiny tag object
    :param name: file name
    :return: artist and title of the file
    """
    artist = ""
    title = norm(file.title.lower()) if file.title is not None else None
    if title is None or name.lower() == title:
        artist = xml_tools.find_artist(name, **kwargs)
        if artist is None or artist == "":
            artist = websearch.find_artist(name)
            if artist is None or artist == "":
                artist = wikisearch.find_artist(name)
    else:
        artist = name.replace(title, '')
    if artist is not None:
        artist = artist.lower()
        title = name.replace(artist, '')
    else:
        artist = "unknown"
    return artist, title


def create_artist_list(xml_path, songs_path, songs_array):
    """

    :param xml_path:
    :param songs_path:
    :param songs_array:
    :return:
    """
    counter = 0
    tree = ET.parse(xml_path)
    root = tree.getroot()
    root = tree.find("artists")
    for song in songs_array:
        try:
            file = TinyTag.get(os.path.join(songs_path, song + ".mp3"))
            print(os.path.join(songs_path, song + ".mp3"))
            artist = file.artist
            if artist is not None:  # artist value isn't blank
                artist = norm(artist)
                artist = re.sub("'|\"", '', artist)
                string = ".//artist[@value='{}']".format(artist)
                if root.find(string) is None:
                    ET.SubElement(root, "artist",{"value": artist})
                    tree.write(xml_path, encoding='utf-8')
                """else:
                    print(type(root.find("[@value={}]".format(file.artist))))"""
        except Exception:  # unsupported files
            counter += 1


def norm(string, **kwargs):
    """

    :param string:
    :param kwargs:
    :return:
    """
    p = re.compile('(\n|\r|\t|;$)')  # remove special chars
    string = p.sub('', string)
    if kwargs.get("web") == True:
        string = re.sub('_', ' ', string)
    else:
        string = re.sub('_|-', ' ', string)
    string = re.sub('\s+', ' ', string)  # replace 2 spaces to 1
    string = re.sub("^\s+|\s+$|^-|-$", '', string)  # remove space padding
    string = re.sub("^\s+|\s+$|^-|-$", '', string)  # remove space padding
    if kwargs.get('title'):
        return string.title()
    else:
        return string.lower()


def remove_forbidden(string):
    """
    get a string and remove all prefix and suffix from it
    :param string: callee string
    :return: clean string
    """
    string = string.lower()
    xml_path = os.path.join(os.getcwd(), r"env\Lib\artists_list.xml")
    tree = xml_tools.is_readable_xml(xml_path)
    root = tree.find("words")
    if root is not None:
        for child in root:
            name = child.get('value')
            string = string.replace(name, '')
    return string


def build_song_profile(song_path, song):
    """
    get song file and create is search query
    :param song_path: the path to the song
    :param song: the song name
    :return: the correct song tags
    """
    x = counter()
    x.up()
    x.print_start()
    file_dir = os.path.join(song_path, song + ".mp3")
    try:
        file = TinyTag.get(file_dir)
    except Exception as err:
        x.down()
        x.print_end()
        return
    artist_string = ""
    for string in (song, file.title, file.artist):  # create the query without duplicate
        if string is not None:
            string = remove_forbidden(string)
            string = norm(string)
            if artist_string.find(string) == -1:
                artist_string = artist_string + " " + string
    artist, title = websearch.google_sarch(artist_string)  # call google search to look for the tags
    # websearch.sel_search(artist_string)
    return artist, title, file_dir  # return all the tags and the dir


def set_new_details(song_path, **kwargs):
    """
    change one selected song attribute
    :param song_path: the path
    :param kwargs: wich attribute to change and their next values
    :return:
    """
    if kwargs.get("img") is not None:
        # adding ID3 tag if it is not present
        try:
            audio = MP3(song_path, ID3=ID3)
            audio.add_tags()
            audio.tags.add(APIC(mime='image/jpeg', type=3, desc=u'Cover', data=open(kwargs.get("img"), 'rb').read()))
            # edit ID3 tags to open and read the picture from the path specified and assign it
            audio.save()  # save the current changes
        except:
            audio.tags.add(APIC(mime='image/jpeg', type=3, desc=u'Cover', data=open(kwargs.get("img"), 'rb').read()))
            # edit ID3 tags to open and read the picture from the path specified and assign it
            audio.save()  # save the current changes
            print(audio.keys())
    try:  # if readble file
        file = EasyID3(song_path)
    except eyed3.Error:
        return
    if kwargs.get("title") is not None and kwargs.get("title") != "":
        file['title'] = kwargs.get("title")
    if kwargs.get("artist") is not None and kwargs.get("artist") != "":
        file['artist'] = kwargs.get("artist")
    file.save()


def update_songs_tags(dir_path, songs_array):
    """
    fuction to handle modify all the songs at once
    :param dir_path: the path to the specifc folder
    :param songs_array: the songs in this folder
    :return: nothing
    """
    start = time.time()  # count the time
    x = counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:  # create thread pool
        futures_songs = [executor.submit(build_song_profile, dir_path, song) for song in songs_array]  # call all the thread
        for future in concurrent.futures.as_completed(futures_songs):  # wait for all the thread
            try:
                artist, title, file_dir = future.result()

                # change all the successful threads
                audio = EasyID3(file_dir)
                if title is not None or title != "":
                    audio['title'] = title
                if artist is not None or title != "":
                    audio['artist'] = artist
                audio.save()
            except:
                pass

    end = time.time()  # calc the process time
    print(end-start)

class counter ():
    """
    help to monitrize the thread
    """
    start = 0
    now = 0
    end = 0

    def print_start(self):
        print("start :{} now:{}, ".format(counter.start, counter.now))

    def print_end(self):
        print("finsih :{} now:{}, ".format(counter.end, counter.now))

    def up(self):
        counter.start += 1
        counter.now += 1

    def down(self):
        counter.end += 1
        counter.now -= 1
